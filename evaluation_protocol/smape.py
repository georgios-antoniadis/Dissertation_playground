import numpy as np

def smape(y_true, y_pred):
    y_pred = y_pred.tolist()
    y_true = y_true.tolist()
    n = len(y_true)
    smape_sum = 0
    for i in range(n):
        smape_sum += (np.abs(y_pred[i] - y_true[i])) / ((np.abs(y_true[i]) + np.abs(y_pred[i])) / 2)
    smape = (100 / n) * np.sum(smape_sum)
    return smape