import numpy as np

def predict_last_value(train, test):
    last_value = train['target'].tolist()[-1]
    naive_predictions = [last_value] * len(test)
    return naive_predictions

def predict_mean(train, test):
    data_mean = np.mean(train['target'].tolist())
    naive_predictions = [data_mean] * len(test)
    return naive_predictions

def predict_random_walk(train, test):
    # Debugging
    # print(input_data[0])
    train = train['target'].tolist()
    last_value = train[-1]
    current_value = last_value
    noise_stddev = 0.1 * (max(train) - min(train))
    predicted_values = []
    for i in range(len(test)):
        predicted_values.append(current_value)
        noise = round(np.random.normal(loc=0, scale=noise_stddev),2)
        current_value = current_value + noise
    return predicted_values
