# app.py
import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from server_77.def_monthly_model import monthly_model

def call_monthly(sql_query, period):
    from server_77.def_monthly_model import monthly_model
    #sql_query = "select * from produksi_care_usage" # Replace with your actual SQL query
    # Run the model
    sum_usage, sum_rows, usage_predictions, rows_predictions, future_dates_usage, future_dates_rows, df_usage, df_rows = monthly_model(sql_query, period)

    #Plot usage
    fig_usage = plt.figure(figsize=(8, 5))
    plt.plot(df_usage.index, df_usage['usage'], label='Pertumbuhan', marker='.')
    plt.plot(future_dates_usage, usage_predictions, label='Prediksi', color='red', marker='.')
    plt.xlabel('Date')
    plt.ylabel('Usage')
    plt.legend()
    plt.grid(True)

    # Plot rows
    fig_rows = plt.figure(figsize=(8, 5))
    plt.plot(df_rows.index, df_rows['Rows'], label='Pertumbuhan', marker='.')
    plt.plot(future_dates_rows, rows_predictions, label='Prediksi', color='red', marker='.')
    plt.xlabel('Date')
    plt.ylabel('Rows')
    plt.legend()
    plt.grid(True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("<h3 style='font-size: 15px;'>Plot Pertumbuhan Usage</h3>", unsafe_allow_html=True)
        st.pyplot(fig_usage)
    with col2:
        st.write("<h3 style='font-size: 15px;'>Plot Pertumbuhan Rows</h3>", unsafe_allow_html=True)
        st.pyplot(fig_rows)

    # Display prediction details
    data = {'date': future_dates_usage, 'prediction usage (KB)': usage_predictions, 'prediction rows (KB)': rows_predictions}
    df = pd.DataFrame(data)
    pd.set_option('display.max_rows', None)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("<h3 style='font-size: 15px;'>Prediction Details</h3>", unsafe_allow_html=True)
        st.dataframe(df)
    with col2:
        st.header("")
        if period == 12:
            st.write("Total prediction usage 1 tahun kedepan yaitu", sum_usage, "MB")
        elif period == 24:
            st.write("Total prediction usage 2 tahun kedepan yaitu", sum_usage, "MB")
        elif period == 36:
            st.write("Total prediction usage 3 tahun kedepan yaitu", sum_usage, "MB")

    

