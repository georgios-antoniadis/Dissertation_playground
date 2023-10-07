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
    outlier_value = data[outlier_index]
    # print(f"Outlier detected: {outlier_value} at index {outlier_index}")
    outliers += 1
  else:
    # print("No outliers detected.")
    outliers = 0 
  return outliers

def grubbs_score(predicted, test_points, alpha):
  # alpha == confidence level, e.g. alpha = 0.05 -> Confidence level = 95%
    model_grubbs = grubbs(predicted, alpha)
    test_data_grubbs = grubbs(test_points, alpha)
    grubbs_score = test_data_grubbs - model_grubbs # The less the score the better the result!

    # if test_data_grubbs == 0:
    #   if model_grubbs == 0 and test_data_grubbs !=0:
    #     grubbs_score = 'Model performed well'
    #   elif model_grubbs !=0 and test_data_grubbs !=0:
    #       grubbs_score = f"Model predicted outliers: {model_grubbs}' \n Test data outliers: {test_data_grubbs}"
      
    # if grubbs_score != 0:
    #     if model_grubbs == 0 and test_data_grubbs != 0:
    #       grubbs_score = 'Model did not predict the outliers'
    #     elif model_grubbs != 0 and test_data_grubbs == 0:
    #       grubbs_score = 'Model predicted outliers that did not exist'
    #     else:
    #       grubbs_score = f"Model predicted outliers: {model_grubbs}' \n Test data outliers: {test_data_grubbs}"

    return grubbs_score 