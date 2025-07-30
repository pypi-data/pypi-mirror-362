import numpy as np
import bjpmodel.dummy_bjp as dummy
from bjpmodel.model import BayesianModel

def run_test(seed, lcensor, rcensor, test_name):
    np.random.seed(seed)
    print(lcensor, rcensor)

    num_vars = 2
    num_data_samples = 1000
    mean = np.array([0.5, -0.2])
    cov = np.array([[2.0, 0.3], [0.3, 0.5]])

    mvn_data = np.random.multivariate_normal(mean, cov, size=num_data_samples).T
    mvn_data = np.array(mvn_data, copy=True, order='C')

    mvn_data = np.clip(mvn_data, lcensor[:, None], rcensor[:, None])

    bjp = BayesianModel(num_vars, burn=1000, chainlength=5000, seed='fixed', trans_optimiser='SCE')

    bjp_fitting_data = bjp.sample(mvn_data, ['yjt', 'yjt'], lcensor, rcensor)

    predictor = np.array([-9999, -9999])

    predictions_result = bjp.forecast(predictor, gen_climatology=False)
    predictions = predictions_result['forecast']

    print(f"--- {test_name} ---")
    print("Mean Data:", mvn_data.mean(axis=1), "Std Data:", mvn_data.std(axis=1))
    print("Mean Predictions:", predictions.mean(axis=0), "Std Predictions:", predictions.std(axis=0))

if __name__ == "__main__":
    # Example censoring thresholds
    seed = 5
    np.random.seed(seed)
    mean = np.array([0.5, -0.2])
    cov = np.array([[2.0, 0.3], [0.3, 0.5]])
    data = np.random.multivariate_normal(mean, cov, size=10000).T
    lcensor = np.percentile(data, 10, axis=1)
    rcensor = np.percentile(data, 90, axis=1)

    run_test(seed, lcensor, rcensor, "Left and right censoring")