from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd

def predict_arima(series,forecast_periods):
    series = series['target'].astype(float)
    forecast_periods = len(forecast_periods)
    p = 1
    d = 1
    q = 1
    # train_list = train_df.loc[0][1:].dropna().tolist()
    arima_model = ARIMA(series, order=(p,d,q))
    arima_results = arima_model.fit()

    fitted_values = arima_results.fittedvalues

    future_predictions = arima_results.get_forecast(steps=forecast_periods)

    complexity = 3

    return future_predictions.predicted_mean, complexity


def predict_theta(series, h):
    series = series['target']
    h = len(h)
    # Extract the first two observations
    theta_0 = series.iloc[0]
    theta_1 = series.iloc[1]

    step_between_observations = 1

    # Forecast using the Theta model formula
    forecasts = theta_0 + np.arange(1, h+1) * ((theta_1 - theta_0) / step_between_observations)  # 1 is the time step between observations

    # step_between_observations
    complexity = 1

    return forecasts, complexity


def predict_ets(train, test):
    periods = 6
    # print(train.head())
    # Sort the DataFrame by timestamp
    train = train.sort_values('timestamp')
    # train['target'].astype(float)
    # Set 'timestamp' as the index
    # train.set_index('timestamp', inplace=True)

    train_size = int(len(train))

    # Fit ETS model
    model = ExponentialSmoothing(train['target'].astype(float), trend='add', seasonal='add', seasonal_periods=periods)
    result = model.fit()

    # Make predictions on the test set
    predictions = result.forecast(len(test))

    # trend, seasonal, seasonal_periods 
    complexity = 3
    
    return predictions, complexity