# Grubb's test
from scipy import stats
import numpy as np

def grubbs(data, alpha):
  outliers = 0

  mean = np.mean(data)
  std_dev = np.std(data)
  z_scores = np.abs((data-mean)/std_dev)
  max_z_score = max(z_scores)
  length_of_data = len(data)
  critical_value = stats.t.ppf(1 - alpha / (2*length_of_data), length_of_data -2)
  if max_z_score > critical_value:
    outlier_index = np.argmax(z_scores)
    outlier_value = data[outlier_index]
    print(f"Outlier detected: {outlier_value} at index {outlier_index}")
    outliers += 1
  else:
    print("No outliers detected.")
  return outliers

def grubbs_score(predicted, test_points, alpha):
  # alpha == confidence level, e.g. alpha = 0.05 -> Confidence level = 95%
    model_grubbs = grubbs(predicted, alpha)
    test_data_grubbs = grubbs(test_points, alpha)
    grubbs_score = test_data_grubbs - model_grubbs # The less the score the better the result! 