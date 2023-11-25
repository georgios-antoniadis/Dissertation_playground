import numpy as np

def last_value_naive(input_data, test_set_length):
    last_value = input_data[-1]
    naive_predictions = [last_value] * test_set_length
    return naive_predictions