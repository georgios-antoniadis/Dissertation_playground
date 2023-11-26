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


def mape(y_true, y_pred):
    if type(y_pred) == list and type(y_true) == list:
        y_pred = y_pred
        y_true = y_true
    elif type(y_pred) != list and type(y_true) != list:
        y_pred = y_pred.tolist()
        y_true = y_true.tolist()
    elif type(y_true) != list:
        y_true = y_true.tolist()
    elif type(y_pred) != list:
        y_pred = y_pred.tolist()
    n = len(y_true)
    mape_sum = 0
    for i in range(n):
        mape_sum += np.abs((y_pred[i] - y_true[i]) / y_true[i])
    mape = (100 / n) * np.sum(mape_sum)
    return mape

def smape(y_true, y_pred):
    if type(y_pred) == list and type(y_true) == list:
        y_pred = y_pred
        y_true = y_true
    elif type(y_pred) != list and type(y_true) != list:
        y_pred = y_pred.tolist()
        y_true = y_true.tolist()
    elif type(y_true) != list:
        y_true = y_true.tolist()
    elif type(y_pred) != list:
        y_pred = y_pred.tolist()

    # Debugging
    # print(f"Predictions type: {type(y_pred)}")
    # print(f"Label data type: {type(y_true)}")

    n = len(y_true)
    smape_sum = 0
    for i in range(n):
        smape_sum += (np.abs(y_pred[i] - y_true[i])) / ((np.abs(y_true[i]) + np.abs(y_pred[i])) / 2)
    smape = (100 / n) * np.sum(smape_sum)
    return smape