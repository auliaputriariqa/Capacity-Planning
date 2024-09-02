import datetime
import pyodbc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

import pandas as pd
import pyodbc
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def monthly_model(sql_query, period):
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
    df_usage['month'] = df_usage.index.month
    df_usage['year'] = df_usage.index.year
    df_usage['lag_1'] = df_usage['usage'].shift(1)
    df_usage = df_usage.dropna()

    # Train model for usage
    Xusage = df_usage[['month', 'year', 'lag_1']]
    yusage = df_usage['usage']
    X_train_usage, X_test_usage, y_train_usage, y_test_usage = train_test_split(Xusage, yusage, test_size=0.2, shuffle=False)
    model_usage = RandomForestRegressor(n_estimators=250)
    model_usage.fit(X_train_usage, y_train_usage)

    # Forecast future values for usage
    last_date = df_usage.index[-1]
    future_dates_usage = [last_date + pd.DateOffset(months=i) for i in range(1, period + 1)]

    # Create DataFrame for future dates
    future_df_usage = pd.DataFrame(index=future_dates_usage)
    future_df_usage['month'] = future_df_usage.index.month
    future_df_usage['year'] = future_df_usage.index.year
    future_df_usage['lag_1'] = df_usage['usage'].iloc[-1]

    # Predict future usage values
    usage_predictions = np.round(model_usage.predict(future_df_usage))

    # Rows DataFrame
    df_rows = df[['DATE', 'Rows']].set_index('DATE')
    df_rows['month'] = df_rows.index.month
    df_rows['year'] = df_rows.index.year
    df_rows['lag_1'] = df_rows['Rows'].shift(1)
    df_rows = df_rows.dropna()

    # Train model for rows
    Xrows = df_rows[['month', 'year', 'lag_1']]
    yrows = df_rows['Rows']
    X_train_rows, X_test_rows, y_train_rows, y_test_rows = train_test_split(Xrows, yrows, test_size=0.2, shuffle=False)
    model_rows = RandomForestRegressor(n_estimators=250)
    model_rows.fit(X_train_rows, y_train_rows)

    # Forecast future values for rows
    last_date = df_rows.index[-1]
    future_dates_rows = [last_date + pd.DateOffset(months=i) for i in range(1, period + 1)]

    # Create DataFrame for future dates
    future_df_rows = pd.DataFrame(index=future_dates_rows)
    future_df_rows['month'] = future_df_rows.index.month
    future_df_rows['year'] = future_df_rows.index.year
    future_df_rows['lag_1'] = df_rows['Rows'].iloc[-1]

    # Predict future rows values
    rows_predictions = np.round(model_rows.predict(future_df_rows))

    # Compute sums
    sum_usage = round((usage_predictions.sum()/1000))
    sum_rows = round((rows_predictions.sum()/1000))

    return (sum_usage, sum_rows, usage_predictions, rows_predictions, future_dates_usage, future_dates_rows, df_usage, df_rows)

