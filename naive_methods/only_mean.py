import numpy as np

def mean_naive(input_data, test_set_length):
    input_data = input_data
    data_mean = np.mean(input_data)
    naive_predictions = [data_mean] * test_set_length
    return naive_predictions