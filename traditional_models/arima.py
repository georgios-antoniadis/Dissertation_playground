from statsmodels.tsa.arima.model import ARIMA

def arima_model(train_df,forecast_periods):
    p = 1
    d = 1
    q =1
    train_list = train_df.loc[0][1:].dropna().tolist()
    arima_model = ARIMA(train_list, order=(p,d,q))
    arima_results = arima_model.fit()

    fitted_values = arima_results.fittedvalues

    future_predictions = arima_results.get_forecast(steps=forecast_periods)

    return future_predictions