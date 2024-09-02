import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import streamlit as st
import matplotlib.pyplot as plt

def show_page1():
    st.title("Penentuan Model")
    text = "<p style='text-align: justify;'>Space Usage Forecast memberikan perkiraan prediksi space yang dibutuhkan database untuk beberapa periode yang akan datang berdasarkan data historical dan trend pertumbuhan. Model Forecasting dilakukan dengan menggunakan algoritma Random Forest. Data sample yang digunakan dalam pembentukan model adalah data Produksi_Care dari tanggal 2014-01-01 s/d 2015-08-31.</p>"
    st.markdown(text, unsafe_allow_html=True)
    st.write("")

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
    query = "SELECT * FROM produksi_care_usage WHERE DATE BETWEEN '2014-01-01' AND '2015-08-31'"
    df = pd.read_sql(query, conn)
    query1 = "SELECT * FROM produksi_care_usage WHERE DATE BETWEEN '2015-09-01' AND '2015-11-30'"
    df1 = pd.read_sql(query1, conn) 

    #data preparation (df)
    df['usage'] = df['Reserved'].str.replace(' KB', '', regex=False).astype(int)
    df = df.sort_values(by='DATE', ascending=True)
    cols = ['TableName', 'Rows', 'Reserved', 'Data', 'IndexSize', 'Unused', 'TGL_RECORD']
    df.drop(cols, axis=1, inplace=True)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.set_index('DATE')

    #data preparation (df1)
    df1['usage'] = df1['Reserved'].str.replace(' KB', '', regex=False).astype(int)
    df1 = df1.sort_values(by='DATE', ascending=True)
    cols1 = ['TableName', 'Rows', 'Reserved', 'Data', 'IndexSize', 'Unused', 'TGL_RECORD']
    df1.drop(cols1, axis=1, inplace=True)
    df1['DATE'] = pd.to_datetime(df1['DATE'])
    df1 = df1.set_index('DATE')

    #forecast modelling with Random Forest
    df['day'] = df.index.day
    df['month'] = df.index.month
    df['day_of_week'] = df.index.dayofweek
    df['lag_1'] = df['usage'].shift(1)
    df = df.dropna()
    # Define features and target
    X = df[['day', 'month', 'day_of_week','lag_1']]
    y = df['usage']
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    # Train the model
    model = RandomForestRegressor(n_estimators=250)
    model.fit(X_train, y_train)

    # Forecast
    y_pred = model.predict(X_test)

    # Evaluate
    from sklearn.metrics import r2_score
    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('R-squared:', r2_score(y_test, y_pred))

    # Forecast future values
    # Create future dataframe with similar features
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=91, freq='D')
    future_df = pd.DataFrame(index=future_dates)
    future_df['day'] = future_df.index.day
    future_df['month'] = future_df.index.month
    future_df['day_of_week'] = future_df.index.dayofweek
    future_df['lag_1'] = df['usage'].iloc[-1]  # Adjust this as needed

    # Predict future values
    future_predictions = model.predict(future_df)

    # Plot results
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 4))
    plt.plot(df.index, df['usage'], label='Pertumbuhan', marker='.')
    plt.plot(future_dates, future_predictions, label='Prediksi', color='red', marker='.')
    plt.xlabel('Date')
    plt.ylabel('Usage')
    plt.title('Prediksi Pertumbuhan Produksi Care')
    plt.legend()
    plt.grid(True)

    total_existing = df['usage'].sum()
    total_prediction = future_predictions.sum()
    st.write("Total storage usage untuk data existing : ", round((total_existing/1000),2), " MB")
    st.write("Total prediction storage (3 months ahead): ", round((total_prediction/1000),2), " MB")
    st.write("")

    st.pyplot(fig)
    st.write("")

    col1, col2 = st.columns([2, 1])
    with col1:
        actual_usage = df1['usage'].to_numpy()
        data = {'date': future_dates, 'actual usage': actual_usage, 'prediction usage': future_predictions}
        df = pd.DataFrame(data)
        pd.set_option('display.max_rows', None)
        st.write("<h3 style='font-size: 15px;'>Actual and Prediction Details</h3>", unsafe_allow_html=True)
        st.dataframe(df)

    with col2:
        comparison = {'sum actual usage': [round((actual_usage.sum()/1000),2)], 
                      'sum prediction usage': [round((future_predictions.sum()/1000),2)],
                      'differences': [round((future_predictions.sum()/1000),2)-round((actual_usage.sum()/1000),2)]}
        df_compare = pd.DataFrame(comparison)
        df_compare_transposed = df_compare.transpose()
        st.write("<h3 style='font-size: 15px;'>Actual and Prediction Comparison</h3>", unsafe_allow_html=True)
        st.dataframe(df_compare_transposed)
        differences = round(round((future_predictions.sum()/1000),2)-round((actual_usage.sum()/1000),2),2)
        st.write("selisih forecast yaitu sebesar ", differences, " MB dari data actual atau kesalahan sebesar ", round(((differences/total_prediction)*100),3),
                 "% ", "sehingga dapat dikatakan model yang dibangun cukup baik digunakan untuk prediksi.")
    
        