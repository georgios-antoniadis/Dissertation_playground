import numpy as np

def random_walk(input_data, test_set_length):
    # Debugging
    # print(input_data[0])
    last_value = input_data[-1]
    current_value = last_value
    noise_stddev = 0.1 * (max(input_data) - min(input_data))
    predicted_values = []
    for i in range(test_set_length):
        predicted_values.append(current_value)
        noise = round(np.random.normal(loc=0, scale=noise_stddev),2)
        current_value = current_value + noise
    return predicted_values