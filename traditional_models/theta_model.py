import numpy as np
#Theta model
def theta_model_forecast(series, h):
    # Extract the first two observations
    theta_0 = series.iloc[0]
    theta_1 = series.iloc[1]

    # Forecast using the Theta model formula
    forecasts = theta_0 + np.arange(1, h+1) * ((theta_1 - theta_0) / 1)  # 1 is the time step between observations

    return forecasts