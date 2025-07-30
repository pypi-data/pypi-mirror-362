import os, sys, shutil
from datetime import datetime

import numpy as np

from normtransform import pytrans
from bjpmodel import pybjp

class BayesianModel:

    OBSERVED_DATA_CODE = 1
    LCENSORED_DATA_CODE = 2
    MISSING_DATA_CODE = 3
    RCENSORED_DATA_CODE = 4
    MISSING_DATA_VALUE = -9999.0

    FIXED_RANDOM_SEED = 5

    NO_LCENS_THRESH = -9999999.0
    NO_RCENS_THRESH = 9999999.0
    ZERO_CENS_THRESH = 0.0

    def __init__(self, num_vars, burn=3000, chainlength=7000, seed='random', trans_optimiser='SCE'):

        self.num_vars = num_vars
        self.burn = burn
        self.chainlength = chainlength
        self.trans_optimiser = trans_optimiser

        assert (seed == 'random' or seed == 'fixed')
        if seed == 'fixed':
            np.random.seed(self.FIXED_RANDOM_SEED)
            self.seed = self.FIXED_RANDOM_SEED
        else:
            self.seed = np.random.randint(0, 100000)

        self.bjp_wrapper = None
        self.bjp_fitting_data = None

    def prepare_bjp_data(self, fit_data, transformer_type, lcensor, rcensor):

        fit_data = np.array(fit_data, copy=True)

        # Set the censored and missing data flags and adjust data accordingly
        flags = np.ones(fit_data.shape, dtype='intc', order='C') * self.OBSERVED_DATA_CODE

        # print(f"Censoring threshold: {censor}")
        censor_idx = fit_data <= lcensor
        flags[censor_idx] = self.LCENSORED_DATA_CODE

        censor_idx = fit_data >= rcensor
        flags[censor_idx] = self.RCENSORED_DATA_CODE

        # Treat both -9999.0 and np.nan as missing values in the input data
        missing_idx = np.abs(fit_data - self.MISSING_DATA_VALUE) < 1E-6
        flags[missing_idx] = self.MISSING_DATA_CODE

        missing_idx2 = np.isnan(fit_data)
        flags[missing_idx2] = self.MISSING_DATA_CODE

        # set NaNs to missing data value
        fit_data[np.isnan(fit_data)] = self.MISSING_DATA_VALUE

        # remove missing values before estimating transformation parameters
        fit_data_for_trans = np.array(fit_data, copy=True)
        fit_data_for_trans = fit_data_for_trans[flags != self.MISSING_DATA_CODE]

        if transformer_type.lower() == 'logsinh':
            trformer = pytrans.PyLogSinh(scale=5.0 / np.max(fit_data_for_trans))
        elif transformer_type.lower() == 'yjt':
            trformer = pytrans.PyYJT(scale=1.0 / np.std(fit_data_for_trans), shift=-1.0 * np.mean(fit_data_for_trans))
        elif transformer_type.lower() == 'sinhasinh':
            trformer = pytrans.PySinhAsinh(scale=1.0 / np.std(fit_data_for_trans), shift=-1.0 * np.mean(fit_data_for_trans))
        elif transformer_type.lower() == 'none':
            trformer = None
        else:
            print('Transformation group code not recognised. Exiting.')
            sys.exit()
            
        if trformer is None:
            
            # restore some dummy values for missing data
            fit_data[np.isnan(fit_data)] = self.MISSING_DATA_VALUE

            tr_data = fit_data
            tr_lcensor = lcensor
            tr_rcensor = rcensor

            bjp_data = {}
            bjp_data['trformer'] = None
            bjp_data['tr_data'] = tr_data
            bjp_data['lcensor'] = lcensor
            bjp_data['tr_lcensor'] = tr_lcensor
            bjp_data['rcensor'] = rcensor
            bjp_data['tr_rcensor'] = tr_rcensor
            bjp_data['flags'] = flags
            
            
        else:

            if self.trans_optimiser.lower() == 'sce':
                trformer.optim_paramsSCE(fit_data_for_trans, lcensor, rcensor, do_rescale=True, is_map=True)
            elif self.trans_optimiser.lower() == 'de':
                trformer.optim_paramsDE(fit_data_for_trans, lcensor, rcensor, do_rescale=True, is_map=True)
            elif self.trans_optimiser.lower() == 'simplex':
                trformer.optim_params(fit_data_for_trans, lcensor, rcensor, do_rescale=True, is_map=True)

            # restore some dummy values for missing data
            fit_data[np.isnan(fit_data)] = self.MISSING_DATA_VALUE

            rs_data = trformer.rescale_many(fit_data)
            tr_data = trformer.transform_many(rs_data)

            rs_lcensor = trformer.rescale_one(lcensor)
            tr_lcensor = trformer.transform_one(rs_lcensor)

            rs_rcensor = trformer.rescale_one(rcensor)
            tr_rcensor = trformer.transform_one(rs_rcensor)

            bjp_data = {}
            bjp_data['trformer'] = trformer
            bjp_data['tr_data'] = tr_data
            bjp_data['lcensor'] = lcensor
            bjp_data['tr_lcensor'] = tr_lcensor
            bjp_data['rcensor'] = rcensor
            bjp_data['tr_rcensor'] = tr_rcensor
            bjp_data['flags'] = flags

        return bjp_data

    def prepare_fc_data(self, predictor_values, bjp_fitting_data):

        if np.any(np.isnan(predictor_values)) or np.any(predictor_values == self.MISSING_DATA_VALUE):
            print("Warning: Predictor is NaN or missing")
            predictor_values[np.isnan(predictor_values)] = -9999.0

        # should we limit extreme new predictor values ???
        # print(self.num_vars)
        bjp_data_new = {}
        bjp_data_new['tr_data'] = np.array([self.MISSING_DATA_VALUE] * self.num_vars)
        bjp_data_new['flags'] = np.array([self.MISSING_DATA_CODE] * self.num_vars, dtype='intc')

        bjp_data_new['lcensor'] = np.array([bjp_fitting_data['lcensor'][i] for i in range(self.num_vars)])
        bjp_data_new['tr_lcensor'] = np.array([bjp_fitting_data['tr_lcensor'][i] for i in range(self.num_vars)])

        bjp_data_new['rcensor'] = np.array([bjp_fitting_data['rcensor'][i] for i in range(self.num_vars)])
        bjp_data_new['tr_rcensor'] = np.array([bjp_fitting_data['tr_rcensor'][i] for i in range(self.num_vars)])

        for i in range(len(predictor_values)):

            if np.abs(predictor_values[i] - self.MISSING_DATA_VALUE) < 1E-6:
                bjp_data_new['flags'][i] = self.MISSING_DATA_CODE
            elif predictor_values[i] <= bjp_data_new['lcensor'][i]:
                bjp_data_new['flags'][i] = self.LCENSORED_DATA_CODE
            elif predictor_values[i] >= bjp_data_new['rcensor'][i]:
                bjp_data_new['flags'][i] = self.RCENSORED_DATA_CODE
            else:
                bjp_data_new['flags'][i] = self.OBSERVED_DATA_CODE

            trformer = bjp_fitting_data['trformer'][i]
            if trformer is not None:
                rs_pred = trformer.rescale_one(predictor_values[i])
                tr_pred = trformer.transform_one(rs_pred)
            else:
                tr_pred = predictor_values[i]

            bjp_data_new['tr_data'][i] = tr_pred

        return bjp_data_new

    def join_ptor_ptand_data(self, bjp_fitting_data):

        joined_data = {'trformer': [], 'tr_data': [], 'lcensor': [], 'tr_lcensor': [],
                       'rcensor': [], 'tr_rcensor': [], 'flags': []}

        for i in range(len(bjp_fitting_data)):
            joined_data['trformer'].append(bjp_fitting_data[i]['trformer'])
            joined_data['tr_data'].append(bjp_fitting_data[i]['tr_data'])
            joined_data['lcensor'].append(bjp_fitting_data[i]['lcensor'])
            joined_data['tr_lcensor'].append(bjp_fitting_data[i]['tr_lcensor'])
            joined_data['rcensor'].append(bjp_fitting_data[i]['rcensor'])
            joined_data['tr_rcensor'].append(bjp_fitting_data[i]['tr_rcensor'])
            joined_data['flags'].append(bjp_fitting_data[i]['flags'])

        joined_data['tr_data'] = np.array(joined_data['tr_data'], order='C')
        joined_data['lcensor'] = np.array(joined_data['lcensor'], order='C')
        joined_data['tr_lcensor'] = np.array(joined_data['tr_lcensor'], order='C')
        joined_data['rcensor'] = np.array(joined_data['rcensor'], order='C')
        joined_data['tr_rcensor'] = np.array(joined_data['tr_rcensor'], order='C')
        joined_data['flags'] = np.array(joined_data['flags'], order='C')

        return joined_data

    def inv_transform(self, data, trformer):

        
        inv_tr_data = trformer.inv_transform_many(data)
        inv_rs_data = trformer.inv_rescale_many(inv_tr_data)

        return inv_rs_data

    def sample(self, obs, transformers, left_censors, right_censors):

        # obs has dimensions num_vars x num_time_periods
        bjp_fitting_data = []

        for i in range(self.num_vars):
            bjp_fitting_data.append(self.prepare_bjp_data(obs[i], transformers[i], left_censors[i], right_censors[i]))

        bjp_fitting_data = self.join_ptor_ptand_data(bjp_fitting_data)

        bjp_wrapper = pybjp.PyBJP(self.num_vars, self.burn, self.chainlength, self.seed)


        mu, mu_sigma = bjp_wrapper.sample(bjp_fitting_data['tr_data'], bjp_fitting_data['flags'],
                                          bjp_fitting_data['tr_lcensor'], bjp_fitting_data['tr_rcensor'])

        self.bjp_wrapper = bjp_wrapper
        self.bjp_fitting_data = bjp_fitting_data

        return bjp_fitting_data

    def forecast(self, predictor_values, gen_climatology=False, convert_cens=True):

        bjp_fc_data = self.prepare_fc_data(predictor_values, self.bjp_fitting_data)
        forecasts = self.bjp_wrapper.forecast(bjp_fc_data['tr_data'], bjp_fc_data['flags'],
                                              bjp_fc_data['tr_lcensor'], bjp_fc_data['tr_rcensor'])

        for i in range(self.num_vars):
            trformer = self.bjp_fitting_data['trformer'][i]
            
            if trformer is not None:
                forecasts[:, i] = self.inv_transform(forecasts[:, i], trformer)

            if convert_cens:
                lcens = bjp_fc_data['lcensor'][i]
                forecasts[:, i][forecasts[:, i] < lcens] = lcens

                rcens = bjp_fc_data['rcensor'][i]
                forecasts[:, i][forecasts[:, i] > rcens] = rcens

        res = {}

        res['forecast'] = forecasts

        if gen_climatology:

            bjp_clims = self.bjp_wrapper.gen_climatology()

            clim = np.empty(forecasts.shape) * np.nan

            for i in range(self.num_vars):
                trformer = self.bjp_fitting_data['trformer'][i]
                clim[:, i] = self.inv_transform(bjp_clims[:, i], trformer)

                if convert_cens:                    
                    lcens = bjp_fc_data['lcensor'][i]
                    clim[:, i][forecasts[:, i] < lcens] = lcens

                    rcens = bjp_fc_data['rcensor'][i]
                    clim[:, i][forecasts[:, i] > rcens] = rcens

            res['clim'] = clim

        return res
