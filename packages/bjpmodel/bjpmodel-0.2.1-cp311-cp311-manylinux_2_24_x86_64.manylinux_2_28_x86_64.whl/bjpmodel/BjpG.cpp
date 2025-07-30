
#include "BjpG.h"
#include <numeric>
#include <random>  // Add this at the top if not already included

// define static BjpG variables

namespace bjp {

const int BjpG::OBSERVED = 1;
const int BjpG::LEFTCENSORED = 2;
const int BjpG::MISSING = 3;
const int BjpG::RIGHTCENSORED = 4;


BjpG::BjpG(int numVars, int burnIn, int chainLength, int randomSeed)
    // initialise the random number generator
    : m_distFactory(randomSeed)
{

    m_numVars = numVars;
    m_numSamplesToBurn = burnIn;
    m_chainLength = chainLength;
    m_numSamplesToKeep = chainLength - burnIn;

    std::cout << "\t" << "The number of variables is " << getNumVars() << std::endl;
	std::cout << "\t" << "The length of the Markov chain is " << getChainLength() << std::endl;

    m_order = vector<int>(getNumVars());
    // fill m_order using STL iota method
    iota(m_order.begin(),m_order.end(), 0);

	m_v = VectorMatD(m_numSamplesToKeep,MatrixXd(getNumVars(), getNumVars()));
	m_mu = VectorVecD(m_numSamplesToKeep,VectorXd(getNumVars()));

}


void BjpG::checkInputs()
{
	if ( m_inputData.rows() != m_inputDataFlags.rows() || m_inputData.cols() != m_inputDataFlags.cols()) {
	    cout << m_inputData.rows() << endl;
	    cout << m_inputDataFlags.rows() << endl;
	    cout << m_inputData.cols() << endl;
	    cout << m_inputDataFlags.cols() << endl;

		cout << "Error in input data size. Exiting..." << endl;
		exit(EXIT_FAILURE);
	}

	for (int i = 0; i < getNumVars(); ++i)
	{
		for (int j = 0; j < getNumTimePeriods(); ++j) {

            if (m_inputDataFlags(i,j) == 1 || m_inputDataFlags(i,j) == 2 || m_inputDataFlags(i,j) == 3 || m_inputDataFlags(i,j) == 4) {
                // all good
            } else {
                cout << "Illegal input data flag. Exiting..." << endl;
                exit(EXIT_FAILURE);
            }
        }
	}
}


void BjpG::replaceMissingWithMean()
{
    m_currentZ = m_inputData;

    for (int i = 0; i < getNumVars(); ++i) {
        double sum = 0.0;
        int count = 0;

        for (int j = 0; j < getNumTimePeriods(); ++j) {
            if (m_inputDataFlags(i, j) != MISSING) {
                sum += m_inputData(i, j);
                ++count;
            }
        }

        // Handle case where all values are missing
        if (count == 0) {
            throw std::runtime_error("All values are missing for variable " + std::to_string(i));
        }

        double mean = sum / count;

        // Replace missing values
        for (int j = 0; j < getNumTimePeriods(); ++j) {
            if (m_inputDataFlags(i, j) == MISSING) {
                m_currentZ(i, j) = mean;
            }
        }
    }
}




void BjpG::sample(const MatrixXd& inputData, const MatrixXi& inputDataFlags,
                    const MatrixXd& leftCensorThresholds, const MatrixXd& rightCensorThresholds)
{

    m_inputData = inputData;
    m_inputDataFlags = inputDataFlags;

    m_leftCensorThresholds = leftCensorThresholds;
    m_rightCensorThresholds = rightCensorThresholds;

    setNumTimePeriods(m_inputData.cols());
    checkInputs();
    replaceMissingWithMean();

	cout << "\t" << "Sampling using " << getNumTimePeriods() << " time periods" << endl;

	for (int i = 0; i < getChainLength(); ++i)
	{

	    sampleV();
	    sampleMu();
		sampleZ();


        if (i >= getNumSamplesToBurn())
		{
            m_v[i-getNumSamplesToBurn()] = m_currentV; // save copy
            m_mu[i-getNumSamplesToBurn()] = m_currentMu; // save copy
		}
	}

}



MatrixXd BjpG::predict(const MatrixXd& inputData, const MatrixXi& inputDataFlags,
                        const MatrixXd& leftCensorThresholds, const MatrixXd& rightCensorThresholds)
{

    m_inputData = inputData;
    m_inputDataFlags = inputDataFlags;

    m_leftCensorThresholds = leftCensorThresholds;
    m_rightCensorThresholds = rightCensorThresholds;

    setNumTimePeriods(m_inputData.cols());
    checkInputs();

	MatrixXd predZ = m_inputData;

	for (int i = 0; i < getNumVars(); i++) {
        predZ(i, 0) = (m_inputDataFlags(i, 0) == MISSING) ? m_mu[0](i) : predZ(i, 0);
	}

    m_currentZ = predZ;

    MatrixXd predictions = MatrixXd(getNumVars(), getNumSamplesToKeep());

	for (int i = 0; i < getChainLength(); ++i)
	{

        m_currentMu = m_mu[i];
        m_currentV = m_v[i];

        sampleZ();

		if (i >= getNumSamplesToBurn())
		{
			predictions.col(i-getNumSamplesToBurn()) = m_currentZ; // save copy
		}
	}

	return predictions;
}



void BjpG::sampleV()
{

    MatrixXd Z_mean = m_currentZ.rowwise().mean();
	MatrixXd Z_minus_z_mean(m_currentZ.rows(), m_currentZ.cols());

	for (int i = 0; i < getNumTimePeriods(); ++i)
	{
		Z_minus_z_mean.col(i) = m_currentZ.col(i) - Z_mean;
	}

	MatrixXd scale = Z_minus_z_mean * Z_minus_z_mean.transpose();

	MatrixXd mat_s_inv = scale.inverse();
	MatrixXd matV_inv = m_distFactory.randWishart(mat_s_inv, getNumTimePeriods()-1);

	m_currentV  = matV_inv.inverse();
}



void BjpG::sampleMu()
{

    VectorXd meanZ = m_currentZ.rowwise().mean();
	MatrixXd scaledV = m_currentV / double(getNumTimePeriods());

	m_currentMu = m_distFactory.randMultivariateNormal(meanZ, scaledV);
}



void BjpG::sampleZ()
{

        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(m_order.begin(), m_order.end(), g);

        int i;
		for (int j=0; j < m_order.size(); j++)
		{

            i = m_order[j];

            double condMean;
            MatrixXd currentV_inv = m_currentV.inverse();
			double condStdev = sqrt(1.0/currentV_inv(i,i));


			for (int k = 0; k < getNumTimePeriods(); k++)
			{
				switch (m_inputDataFlags(i, k)) {

				case OBSERVED:

				    m_currentZ(i, k) = m_inputData(i, k);
				    break;

				case LEFTCENSORED:

                    condMean = conditionalMean(i, m_currentV, m_currentMu, m_currentZ.col(k));
					m_currentZ(i, k) = imputeLeftCensored(condMean, condStdev, m_leftCensorThresholds(i));

					break;

				case RIGHTCENSORED:

                    condMean = conditionalMean(i, m_currentV, m_currentMu, m_currentZ.col(k));
					m_currentZ(i, k) = imputeRightCensored(condMean, condStdev, m_rightCensorThresholds(i));
					break;

                case MISSING:

                    condMean = conditionalMean(i, m_currentV, m_currentMu, m_currentZ.col(k));
					m_currentZ(i, k) = m_distFactory.randNormal(condMean, condStdev);
					break;

				}
			}
		}

}



void removeRow(Eigen::MatrixXd& matrix, unsigned int rowToRemove)
{
    unsigned int numRows = matrix.rows()-1;
    unsigned int numCols = matrix.cols();

    if( rowToRemove < numRows )
        matrix.block(rowToRemove,0,numRows-rowToRemove,numCols) = matrix.block(rowToRemove+1,0,numRows-rowToRemove,numCols);

    matrix.conservativeResize(numRows,numCols);
}



void removeColumn(Eigen::MatrixXd& matrix, unsigned int colToRemove)
{
    unsigned int numRows = matrix.rows();
    unsigned int numCols = matrix.cols()-1;

    if( colToRemove < numCols )
        matrix.block(0,colToRemove,numRows,numCols-colToRemove) = matrix.block(0,colToRemove+1,numRows,numCols-colToRemove);
	    
    matrix.conservativeResize(numRows,numCols);
}



VectorXd BjpG::removeVectorElement(const VectorXd& vec, const int elementToRemove) const
{

    int numElements = vec.size();
    VectorXd newVec(numElements-1);
    for (int i=0; i!=numElements; i++) {

        if (i < elementToRemove) {
            newVec(i) = vec(i);
        } else if (i > elementToRemove) {
            newVec(i-1) = vec(i);
        }
    }

	return newVec;
}



double BjpG::conditionalMean(int i, MatrixXd &cov, VectorXd &mu, const VectorXd &a)
{

    MatrixXd cov12 = cov.row(i);
    removeColumn(cov12, i);

    MatrixXd cov22 = cov;
    removeRow(cov22, i);
    removeColumn(cov22, i);
    MatrixXd cov22_inv = cov22.inverse();

    MatrixXd diff = removeVectorElement(a, i) - removeVectorElement(mu, i);
    MatrixXd deviation = cov12*cov22_inv*diff;

    return mu(i) + deviation(0,0);

}



double BjpG::imputeLeftCensored(double mean, double stdev, double censor)
{

    double uniformVal = m_distFactory.randUniform();
    double cdfValue = m_distFactory.normalCdf( (censor-mean)/stdev);
	double augmentedValue =  uniformVal*cdfValue ;

	// deal with edge case - uniformVal or cdfValue could be 0.0, causing a subsequent overflow
	double imputed_value;

	if (augmentedValue < 1E-6)
	{
		imputed_value = censor;
	}
	else
	{
		imputed_value = m_distFactory.normalQuantile(augmentedValue)*stdev + mean;

	}

	return imputed_value;
}


double BjpG::imputeRightCensored(double mean, double stdev, double censor)
{

    double uniformVal = m_distFactory.randUniform();
    double cdfValue = m_distFactory.normalCdf((censor-mean)/stdev);
	double augmentedValue = (1 - cdfValue)*uniformVal;

    // deal with edge case - uniformVal or cdfValue could be 0.0, causing a subsequent overflow
	double imputed_value;

	if (augmentedValue < 1E-6)
	{
		imputed_value = censor;
	}
	else
	{
		imputed_value = m_distFactory.normalQuantile(1-augmentedValue)*stdev + mean;

	}

	return imputed_value;
}



void BjpG::setNumTimePeriods(int numTimePeriods)
{
    m_numTimePeriods = numTimePeriods;
}



void BjpG::setNumVars(int numVars)
{
    m_numVars = numVars;
}



void BjpG::setMu(VectorVecD mu)
{
    m_mu = mu;
}



void BjpG::setV(VectorMatD v)
{
    m_v = v;
}

void BjpG::setNumSamplesToBurn(int numSamplesToBurn) {

    m_numSamplesToBurn = numSamplesToBurn;

}



void BjpG::setNumSamplesToKeep(int numSamplesToKeep) {

    m_numSamplesToKeep = numSamplesToKeep;
}



void BjpG::setChainLength(int chainLength) {

    m_chainLength = chainLength;
}

} // end bjp namespace