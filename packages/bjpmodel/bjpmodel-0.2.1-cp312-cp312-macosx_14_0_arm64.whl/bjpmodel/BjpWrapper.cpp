#include "BjpWrapper.h"


namespace bjp {


    BjpWrapper::BjpWrapper(int numVars, int burnIn, int chainLength, int randomSeed)

        {

        m_numVars = numVars;
        m_numSamplesToBurn = burnIn;
        m_chainLength = chainLength;
        m_numSamplesToKeep = chainLength - burnIn;
        m_randomSeed = randomSeed;

        m_bjpModelPtr = make_shared<BjpG>(m_numVars, m_numSamplesToBurn, m_chainLength, m_randomSeed);

        }



    int BjpWrapper::index_3d_row_major(int i, int j, int k, int d3, int d2) {

            return (i * d3 * d2) + (j * d2) + k;
    }



    int BjpWrapper::getIndexOf2dArrayInRowMajor(int i, int j, int d2) {

            return (i * d2) + j;

    }



     MatrixXd BjpWrapper::row_major_to_matrixXd(double *a, int d1, int d2) {

        MatrixXd m = MatrixXd(d1, d2);
        int i, j;

        for (i = 0; i < d1; i++) {
            for (j = 0; j < d2; j++) {

                m(i,j) = a[getIndexOf2dArrayInRowMajor(i,j,d2)];
            }
        }

        return m;
    }



     MatrixXi BjpWrapper::row_major_to_matrixXi(int *a, int d1, int d2) {

        MatrixXi m = MatrixXi(d1, d2);
        int i, j;

        for (i = 0; i < d1; i++) {
            for (j = 0; j < d2; j++) {
                m(i,j) = a[getIndexOf2dArrayInRowMajor(i,j,d2)];
            }
        }

        return m;
    }



    void BjpWrapper::copyCovarianceParamsIntoArray(const VectorMatD& source, double* target) {

        int numSamples = source.size();
        int numVars = source[0].rows();
        int numParams = numVars+numVars*(numVars-1)/2;

        for (int k = 0; k < numSamples; k++)
        {
            int m = 0;
            for (int i = 0; i < numVars; i++)
            {
                for (int j = i; j < numVars; j++)
                {

                    target[getIndexOf2dArrayInRowMajor(k,m,numParams)] = source[k](i,j);
                    m++;
                }
            }
        }
    }



    MatrixXd BjpWrapper::copyArrayToEigenMatrix(double* source) {

        MatrixXd target = MatrixXd(m_numVars,1);
        for (int i = 0; i < m_numVars; i++) {
            target(i,0) = source[i];
       }

       return target;

    }



    MatrixXi BjpWrapper::copyArrayToEigenMatrix(int* source) {

        MatrixXi target = MatrixXi(m_numVars,1);
        for (int i = 0; i < m_numVars; i++) {
            target(i,0) = source[i];
       }

       return target;

    }



    void BjpWrapper::copyMuParamsIntoArray(const VectorVecD& source, double* target) {

        int numSamples = source.size();
        int numVars = source[0].rows();

        if (numSamples != m_numSamplesToKeep || numVars != m_numVars) {
            cout << "Problem in wrapper. Dimensions do not match target array. Exiting.." << endl;
            exit(EXIT_FAILURE);
        }

        for (int i = 0; i < numSamples; i++) {
            for (int j = 0; j < numVars; j++) {

                target[getIndexOf2dArrayInRowMajor(i,j,numVars)] = source[i](j);
            }
        }
    }



    int BjpWrapper::sampleParamsAndForecast(double* obs, int* cm, int nobs, double* predictors, \
                            int* predictorFlags, double* leftCensorThresholds, double* rightCensorThresholds, double* muParameters, double* covarianceParameters, double* forecasts) {


        MatrixXd matD = row_major_to_matrixXd(obs, m_numVars, nobs);
        MatrixXi matD_mark = row_major_to_matrixXi(cm, m_numVars, nobs);

        MatrixXd leftCensorsMatrix = copyArrayToEigenMatrix(leftCensorThresholds);
        MatrixXd rightCensorsMatrix = copyArrayToEigenMatrix(rightCensorThresholds);
        // Sampling
        m_bjpModelPtr->setChainLength(m_chainLength);
		m_bjpModelPtr->sample(matD, matD_mark, leftCensorsMatrix, rightCensorsMatrix);

		VectorVecD bjpMu = m_bjpModelPtr->getMu();
        VectorMatD bjpV = m_bjpModelPtr->getV();

        copyMuParamsIntoArray(bjpMu, muParameters);
        copyCovarianceParamsIntoArray(bjpV, covarianceParameters);

       // Forecasting
        MatrixXd predictorsMatrix = copyArrayToEigenMatrix(predictors);
        MatrixXi predictorFlagsMatrix = copyArrayToEigenMatrix(predictorFlags);

        m_bjpModelPtr->setChainLength(m_numSamplesToKeep);

        MatrixXd bjp_forecasts = m_bjpModelPtr->predict(predictorsMatrix, predictorFlagsMatrix, leftCensorsMatrix, rightCensorsMatrix);

        int numForecastSamples = m_numSamplesToKeep - m_numSamplesToBurn;
        for (int i = 0; i < numForecastSamples; i++) {
            for (int j = 0; j < m_bjpModelPtr->getNumVars(); j++) {
                forecasts[getIndexOf2dArrayInRowMajor(i,j,m_numVars)] = bjp_forecasts(j,i);
            }
        }

    return 0;

    }



    int BjpWrapper::sampleParams(double* obs, int* cm, int nobs, double* leftCensorThresholds, double* rightCensorThresholds, double* muParameters, double* covarianceParameters) {


        MatrixXd matD = row_major_to_matrixXd(obs, m_numVars, nobs);
        MatrixXi matD_mark = row_major_to_matrixXi(cm, m_numVars, nobs);

        MatrixXd leftCensorsMatrix = copyArrayToEigenMatrix(leftCensorThresholds);
        MatrixXd rightCensorsMatrix = copyArrayToEigenMatrix(rightCensorThresholds);
        // Sampling
        m_bjpModelPtr->setChainLength(m_chainLength);

		m_bjpModelPtr->sample(matD, matD_mark, leftCensorsMatrix, rightCensorsMatrix);

		VectorVecD bjpMu = m_bjpModelPtr->getMu();
        VectorMatD bjpV = m_bjpModelPtr->getV();

        copyMuParamsIntoArray(bjpMu, muParameters);
        copyCovarianceParamsIntoArray(bjpV, covarianceParameters);

    return 0;

}



    int BjpWrapper::forecast(double* predictors, int* predictorFlags, double* leftCensorThresholds, double* rightCensorThresholds, double* forecasts) {


        // Forecasting
        MatrixXd predictorsMatrix = copyArrayToEigenMatrix(predictors);
        MatrixXi predictorFlagsMatrix = copyArrayToEigenMatrix(predictorFlags);

        MatrixXd leftCensorsMatrix = copyArrayToEigenMatrix(leftCensorThresholds);
        MatrixXd rightCensorsMatrix = copyArrayToEigenMatrix(rightCensorThresholds);

        m_bjpModelPtr->setChainLength(m_numSamplesToKeep);

        MatrixXd bjp_forecasts = m_bjpModelPtr->predict(predictorsMatrix, predictorFlagsMatrix, leftCensorsMatrix, rightCensorsMatrix);

        int numForecastSamples = m_numSamplesToKeep - m_numSamplesToBurn;

        for (int i = 0; i < numForecastSamples; i++) {
            for (int j = 0; j < m_bjpModelPtr->getNumVars(); j++) {
                forecasts[getIndexOf2dArrayInRowMajor(i,j,m_numVars)] = bjp_forecasts(j,i);
            }
        }

        return 0;

    }



    int BjpWrapper::calcDensitiesOnePredictand(double* obs, int* flags, int nobs, double* leftCensorThresholds, double* rightCensorThresholds, int pos, double* logDensities) {


        MatrixXd obsMatrix = row_major_to_matrixXd(obs, m_numVars, nobs);

        bjp::DistributionFactory distFactory;

        VectorVecD bjpMu = m_bjpModelPtr->getMu();
        VectorMatD bjpV = m_bjpModelPtr->getV();

         for (int i=0; i != m_numVars; i++) {
            if (flags[i] == 3) {
                cout << "Densities for cases with missing predictors is not implemented yet. Exiting." << endl;
                exit(0);
            }
         }


        for (int i=0; i != nobs; i++) {

            double density = 0;

            for (int j=0; j != m_numSamplesToKeep; j++) {

                if (j>=m_numSamplesToBurn) {

                    VectorXd mu = bjpMu[j];
                    MatrixXd cov = bjpV[j];

                    MatrixXd cov_inv = cov.inverse();
                    double condStdev = sqrt(1.0/cov_inv(pos,pos));

                    double condMean = m_bjpModelPtr->conditionalMean(pos, cov, mu, obsMatrix.col(i));

                    if (flags[pos] == 2) {
                        density += distFactory.normalCdf( (leftCensorThresholds[pos]-condMean)/condStdev);
                    } else if (flags[pos] == 4) {
                        density += distFactory.normalCdf(1 - (rightCensorThresholds[pos]-condMean)/condStdev);
                    } else {
                        density += 1.0/condStdev*distFactory.normalPdf( (obsMatrix(pos,i)-condMean)/condStdev);
                    }
            }

        }

        logDensities[i] = log(density) - log(m_numSamplesToKeep-m_numSamplesToBurn);

    }

    return 0;

    }



    int BjpWrapper::genClimatology(double* climatologies) {

        bjp::DistributionFactory distFactory;

        VectorVecD bjpMu = m_bjpModelPtr->getMu();
        VectorMatD bjpV = m_bjpModelPtr->getV();

        int numForecastSamples = m_numSamplesToKeep - m_numSamplesToBurn;

        for (int i=0; i != numForecastSamples; i++) {

            VectorXd climSample = distFactory.randMultivariateNormal(bjpMu[i], bjpV[i]);

             for (int j = 0; j < m_numVars; j++) {
                climatologies[getIndexOf2dArrayInRowMajor(i,j,m_numVars)] = climSample(j);
                }
        }


        return 0;

    }

}