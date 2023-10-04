import numpy as np

def mape(y_true, y_pred):
    y_pred = y_pred.tolist()
    y_true = y_true.tolist()
    n = len(y_true)
    mape_sum = 0
    for i in range(n):
        mape_sum += np.abs((y_pred[i] - y_true[i]) / y_true[i])
    mape = (100 / n) * np.sum(mape_sum)
    return mape