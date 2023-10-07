from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
import pandas as pd


def ets_method(train, test, periods):
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

    return predictions