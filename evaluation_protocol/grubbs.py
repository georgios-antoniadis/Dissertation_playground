# Grubb's test
from scipy import stats
import numpy as np

def grubbs(data, alpha):
  outliers = 0
  mean = np.mean(data)
  std_dev = np.std(data)
  z_scores = np.abs((data-mean)/(np.abs(std_dev)))
  max_z_score = max(z_scores)
  length_of_data = len(data)
  critical_value = stats.t.ppf(1 - alpha / (2*length_of_data), length_of_data -2)
  if max_z_score > critical_value:
    outlier_index = np.argmax(z_scores)
    outliers += 1
  else:
    outliers = 0 
  return outliers

def grubbs_score(predicted, test_points):
  # alpha == confidence level, e.g. alpha = 0.05 -> Confidence level = 95%
    alpha = 0.05
    model_grubbs = grubbs(predicted, alpha)
    test_data_grubbs = grubbs(test_points, alpha)
    grubbs_score = test_data_grubbs - model_grubbs # The less the score the better the result!

    return grubbs_score 