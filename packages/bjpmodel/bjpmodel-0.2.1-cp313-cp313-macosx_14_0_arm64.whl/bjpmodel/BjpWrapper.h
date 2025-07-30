#pragma once

#include <vector>
#include <cmath>
#include <memory>

#include <Eigen/Dense>
using namespace Eigen;

#include "BjpG.h"
#include "VectorMat.h"

namespace bjp {

    class BjpWrapper {

    public:

        BjpWrapper() {};
        BjpWrapper(int numVars, int burnIn, int chainLength, int randomSeed);
        ~BjpWrapper() {};

        int getIndexOf2dArrayInRowMajor(int i, int j, int d2);
        int index_3d_row_major(int i, int j, int k, int d3, int d2);
        Eigen::MatrixXd row_major_to_matrixXd(double *a, int d1, int d2);
        Eigen::MatrixXi row_major_to_matrixXi(int *a, int d1, int d2);


        void copyCovarianceParamsIntoArray(const VectorMatD& source, double* target);
        void copyMuParamsIntoArray(const VectorVecD& source, double* target);

        MatrixXd copyArrayToEigenMatrix(double* source);
        MatrixXi copyArrayToEigenMatrix(int* source);


        int sampleParamsAndForecast(double* obs, int* cm, int nobs, double* predictors, \
                        int* pcm, double* leftCensorThresholds, double* rightCensorThresholds, double* mu, double* cov, double* forecasts);

        int sampleParams(double* obs, int* cm, int nobs, double* leftCensorThresholds, double* rightCensorThresholds, double* mu, double* cov);
        int forecast(double* predictors, int* predictorFlags, double* leftCensorThresholds, double* rightCensorThresholds, double* forecasts);

        int calcDensitiesOnePredictand(double* obs, int* flags, int nobs, double* leftCensorThresholds, double* rightCensorThresholds, int predictandIndex, double* logDensities);

        int genClimatology(double* climatologies);

    private:



	int m_numVars; // The number of variables and time periods
	int m_numSamplesToBurn; // Gibbs chain length and burn-in
	int m_numSamplesToKeep;
	int m_chainLength;
	int m_randomSeed;

    shared_ptr<BjpG> m_bjpModelPtr;



    };
}

