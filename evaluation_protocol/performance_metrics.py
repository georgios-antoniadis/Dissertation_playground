import numpy as np

def rmse(predicted, real):
    predicted = np.array(predicted)
    real = np.array(real)
    return np.sqrt(((predicted-real)**2).mean())

def nme(predicted, real):
    predicted = np.array(predicted)
    real = np.array(real)
    absolute_percentage_errors = np.abs((real - predicted) / real)
    return absolute_percentage_errors.mean()

def mae(predicted, real):
    predicted = np.array(predicted)
    real = np.array(real)
    return np.abs(predicted - real).mean()

def mse(predicted, real):
    predicted = np.array(predicted)
    real = np.array(real)
    return ((predicted - real) ** 2).mean()