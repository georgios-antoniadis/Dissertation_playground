import numpy as np

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