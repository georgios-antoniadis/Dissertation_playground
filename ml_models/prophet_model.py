import pandas as pd
from prophet import Prophet

def prophet_model(train, test):
    train.columns = ['ds', 'y']
    test.columns = ['ds', 'y']

    model = Prophet(interval_width=0.95)
    model.fit(train)
    
    future_preds = len(test['ds'])

    # Make forecasts for as many years as the ones included in the test dataset
    future_dates = model.make_future_dataframe(periods=future_preds, freq='YS')

    forecast = model.predict(future_dates)

    forecast_organized = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    predicted = forecast['yhat'][-future_preds:]

    return predicted