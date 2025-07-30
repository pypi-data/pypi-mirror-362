#include "DistributionFactory.h"

#define _USE_MATH_DEFINES
#include <cmath>

namespace bjp {

    DistributionFactory::DistributionFactory()
        : rng(5),
          m_distNormal(0.0, 1.0),
          m_distUniform(0.0000000001, 0.999999999)
    {
        // Default random seed of 5
    }

    DistributionFactory::DistributionFactory(int seed)
        : rng(seed),
          m_distNormal(0.0, 1.0),
          m_distUniform(0.0000000001, 0.999999999)
    {
        // Custom random seed provided
    }

    double DistributionFactory::randUniform() {
        return m_distUniform(rng);
    }

    double DistributionFactory::randNormal() {
        return m_distNormal(rng);
    }

    double DistributionFactory::randNormal(double mean, double stdev) {
        return m_distNormal(rng) * stdev + mean;
    }

    double DistributionFactory::normalPdf(double value) {
        double variance = 1.0;
        double mean = 0.0;
        return (1.0 / std::sqrt(2.0 * M_PI * variance)) *
               std::exp(-0.5 * std::pow((value - mean), 2) / variance);
    }

    double DistributionFactory::normalCdf(double value) {
        return 0.5 * (1.0 + std::erf(value / std::sqrt(2.0)));
    }

    double DistributionFactory::normalQuantile(double value) {
        // Approximation of the quantile function using inverse error function
        return std::sqrt(2.0) * erfinv(2.0 * value - 1.0);
    }


VectorXd DistributionFactory::randMultivariateNormal(VectorXd& mu, MatrixXd& cov)
{

    int numVars = mu.size();
    VectorXd stdNormSample(numVars);
	MatrixXd cholFactor = cov.llt().matrixL();

	for (int i = 0; i < numVars; i++)
	{
	    stdNormSample(i) = randNormal();
	}

	return (cholFactor * stdNormSample) + mu;

}


MatrixXd DistributionFactory::randWishart(MatrixXd& scale, int degFreedom)
{

    int notPosDefCount = 0;
    bool notPosDef = true;

    int numVars = scale.rows();

    MatrixXd L = scale.llt().matrixL();
    MatrixXd A(numVars, degFreedom);

    MatrixXd result;

    while (notPosDef) {

        for (int i = 0; i < numVars; ++i)
        {
            for (int j = 0; j < degFreedom; ++j)
            {
                A(i, j) = randNormal();
            }
        }

        MatrixXd LA = L * A;
//        result = LA * LA.transpose();
        result = L * A * A.transpose() * L.transpose();

        if (result.llt().info() == Eigen::NumericalIssue) {
            notPosDefCount = notPosDefCount + 1;

            if (notPosDefCount == 10) {
                std::cout << "could not find a positive definite V. Exiting" << std::endl;
                exit(EXIT_FAILURE);
            }
            std::cout << "V not positive definite - retrying attempt #" << notPosDefCount << std::endl;

        } else {
            notPosDef = false;
        }

    }

    return result;

}


// Custom implementation of the inverse error function
// https://stackoverflow.com/questions/5971830/need-code-for-inverse-error-function
double DistributionFactory::erfinv(double y) {

    // Coefficients for rational approximation
    const double a[] = { 0.886226899, -1.645349621,  0.914624893, -0.140543331 };
    const double b[] = { -2.118377725,  1.442710462, -0.329097515,  0.012229801 };
    const double c[] = { -1.970840454, -1.624906493,  3.429567803,  1.641345311 };
    const double d[] = {  3.543889200,  1.637067800 };

    const double y0 = 0.7; // Threshold for dividing approximation regions
    double x, z;          // Variables for intermediate calculations

    // Check the range of the input
    if (y < -1.0 || y > 1.0) {
        throw std::invalid_argument("erfinv(y) argument out of range");
    }

    if (std::fabs(y) == 1.0) {
        // Handle edge cases where y is -1 or 1
        x = -y * std::log(0.0); // Produces +infinity for y = 1, -infinity for y = -1
    } else if (y < -y0) {
        // For y in the range (-1, -y0), use an approximation for the lower tail
        z = std::sqrt(-std::log((1.0 + y) / 2.0));
        x = -(((c[3] * z + c[2]) * z + c[1]) * z + c[0]) /
            ((d[1] * z + d[0]) * z + 1.0);
    } else if (y < y0) {
        // For y in the range [-y0, y0], use a central approximation
        z = y * y;
        x = y * (((a[3] * z + a[2]) * z + a[1]) * z + a[0]) /
            ((((b[3] * z + b[2]) * z + b[1]) * z + b[0]) * z + 1.0);
    } else {
        // For y in the range [y0, 1), use an approximation for the upper tail
        z = std::sqrt(-std::log((1.0 - y) / 2.0));
        x = (((c[3] * z + c[2]) * z + c[1]) * z + c[0]) /
            ((d[1] * z + d[0]) * z + 1.0);
    }

    // Polish the result using Newton-Raphson refinement. 1 or 2 iterations should be plenty.
    for (int i = 0; i < 2; ++i) {
        x = x - (std::erf(x) - y) / (2.0 / std::sqrt(M_PI) * std::exp(-x * x));
    }

    return x; // Return the computed inverse error function value
}


}
