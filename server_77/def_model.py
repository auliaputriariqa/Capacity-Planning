# forecast_model.py

import datetime
import pyodbc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def model(sql_query,period):
    # Database connection
    driver = '{ODBC Driver 17 for SQL Server}'  
    server = '192.168.140.138'
    database = 'RnD_Sumber_Forecast'
    username = 'sa'
    password = '12345Zx!'
    conn_str = (
        f"Driver={driver};"
        f"Server={server};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password}")
    conn = pyodbc.connect(conn_str)
    df = pd.read_sql(sql_query, conn)

    # Data preparation
    df['usage'] = df['Reserved'].str.replace(' KB', '', regex=False).astype(int)
    df['Rows'] = df['Rows'].astype(int)
    df = df.sort_values(by='DATE', ascending=True)
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Usage DataFrame
    df_usage = df[['DATE', 'usage']].set_index('DATE')
    df_usage['day'] = df_usage.index.day
    df_usage['month'] = df_usage.index.month
    df_usage['day_of_week'] = df_usage.index.dayofweek
    df_usage['lag_1'] = df_usage['usage'].shift(1)
    df_usage = df_usage.dropna()

    # Train model for usage
    Xusage = df_usage[['day', 'month', 'day_of_week', 'lag_1']]
    yusage = df_usage['usage']
    X_train_usage, X_test_usage, y_train_usage, y_test_usage = train_test_split(Xusage, yusage, test_size=0.2, shuffle=False)
    model_usage = RandomForestRegressor(n_estimators=250)
    model_usage.fit(X_train_usage, y_train_usage)
    #yusage_pred = model_usage.predict(X_test_usage)

    # Forecast future values for usage
    future_dates_usage = pd.date_range(start=df_usage.index[-1] + pd.Timedelta(days=1), periods=period, freq='D')
    future_df_usage = pd.DataFrame(index=future_dates_usage)
    future_df_usage['day'] = future_df_usage.index.day
    future_df_usage['month'] = future_df_usage.index.month
    future_df_usage['day_of_week'] = future_df_usage.index.dayofweek
    future_df_usage['lag_1'] = df_usage['usage'].iloc[-1]
    usage_predictions = np.round(model_usage.predict(future_df_usage))

    # Rows DataFrame
    df_rows = df[['DATE', 'Rows']].set_index('DATE')
    df_rows['day'] = df_rows.index.day
    df_rows['month'] = df_rows.index.month
    df_rows['day_of_week'] = df_rows.index.dayofweek
    df_rows['lag_1'] = df_rows['Rows'].shift(1)
    df_rows = df_rows.dropna()

    # Train model for rows
    Xrows = df_rows[['day', 'month', 'day_of_week', 'lag_1']]
    yrows = df_rows['Rows']
    X_train_rows, X_test_rows, y_train_rows, y_test_rows = train_test_split(Xrows, yrows, test_size=0.2, shuffle=False)
    model_rows = RandomForestRegressor(n_estimators=250)
    model_rows.fit(X_train_rows, y_train_rows)
    #yrows_pred = model_rows.predict(X_test_rows)

    # Forecast future values for rows
    future_dates_rows = pd.date_range(start=df_rows.index[-1] + pd.Timedelta(days=1), periods=period, freq='D')
    future_df_rows = pd.DataFrame(index=future_dates_rows)
    future_df_rows['day'] = future_dates_rows.day
    future_df_rows['month'] = future_dates_rows.month
    future_df_rows['day_of_week'] = future_dates_rows.dayofweek
    future_df_rows['lag_1'] = df_rows['Rows'].iloc[-1]
    rows_predictions = np.round(model_rows.predict(future_df_rows))

    # Compute sums
    sum_usage = round((usage_predictions.sum()/1000))
    sum_rows = round((rows_predictions.sum()/1000))

    return (sum_usage, sum_rows, usage_predictions, rows_predictions, future_dates_usage, future_dates_rows, df_usage, df_rows)
