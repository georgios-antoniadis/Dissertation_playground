# LightGBM 
import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

def lightgbm(df):
    # Assuming you have a pandas DataFrame with a 'timestamp' and 'target' column
    # Load your timeseries data into a pandas DataFrame (replace 'your_data.csv' with your actual file)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%d-%m-%y %H:%M")
    df = df.set_index('timestamp')

    # Create lag features (you can customize the number of lags)
    for i in range(1, 4):
        df[f'lag_{i}'] = df['target'].shift(i)

    df = df.dropna()

    # Split the data into train and test sets using TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in tscv.split(df):
        train_data = df.iloc[train_index]
        test_data = df.iloc[test_index]

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(train_data.drop('target', axis=1))
    y_train = train_data['target'].values

    X_test_scaled = scaler.transform(test_data.drop('target', axis=1))
    y_test = test_data['target'].values

    # Create a LightGBM dataset
    train_set = lgb.Dataset(X_train_scaled, label=y_train)
    test_set = lgb.Dataset(X_test_scaled, label=y_test, reference=train_set)

    # Set LightGBM parameters
    params = {
        'objective': 'regression',
        'metric': 'mse',
        'boosting_type': 'gbdt',
        # 'num_leaves': 31,
        'num_leaves': 5,
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }

    # Train the model
    num_round = 100
    bst = lgb.train(params, train_set, num_round, valid_sets=[test_set])

    # Make predictions on the test set
    y_pred = bst.predict(X_test_scaled, num_iteration=bst.best_iteration)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
