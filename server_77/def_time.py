    
import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from server_77.def_model import model
import plotly.express as px

def monthly(sql_query, period):
    from server_77.def_model import model
    #sql_query = "select * from produksi_care_usage" # Replace with your actual SQL query
    # Run the model
    sum_usage, sum_rows, usage_predictions, rows_predictions, future_dates_usage, future_dates_rows, df_usage, df_rows = model(sql_query, period)

    # Convert daily data to monthly
    df_usage = df_usage.resample('M').sum().reset_index()
    df_rows = df_rows.resample('M').sum().reset_index()
    
    data = {'date': future_dates_usage, 'prediction usage (KB)': usage_predictions, 'prediction rows (KB)': rows_predictions}
    df = pd.DataFrame(data)
    pd.set_option('display.max_rows', None)
    df.set_index('date', inplace=True)
    df_monthly = df.resample('M').sum().reset_index()
    
    fig_usage = px.line(
        df_usage,
        x='DATE',
        y='usage',
        labels={'Date': 'Date', 'Usage': 'Usage'})
    fig_usage.add_scatter(
        x=df_monthly['date'],
        y=df_monthly['prediction usage'],
        mode='lines+markers',
        name='Monthly Predictions',
        line=dict(color='red'))
    fig_usage.update_layout(
        width=500,  # Set width to 1000 pixels
        height=400,
        xaxis_title='Date',
        yaxis_title='Usage',
        legend_title='Legend',
        xaxis=dict(
            tickformat='%b %Y',  # Format the x-axis to show month and year
            tickmode='auto',
            dtick='M1'),  # Set tick interval to monthly
        yaxis=dict(showgrid=True))
    
    fig_rows = px.line(
        df_rows,
        x='DATE',
        y='Rows',
        labels={'Date': 'Date', 'Rows': 'Rows'})
    fig_rows.add_scatter(
        x=df_monthly['date'],
        y=df_monthly['prediction rows'],
        mode='lines+markers',
        name='Monthly Predictions',
        line=dict(color='red'))
    fig_rows.update_layout(
        width=500,  # Set width to 1000 pixels
        height=400,
        xaxis_title='Date',
        yaxis_title='Usage',
        legend_title='Legend',
        xaxis=dict(
            tickformat='%b %Y',  # Format the x-axis to show month and year
            tickmode='auto',
            dtick='M1'),  # Set tick interval to monthly
        yaxis=dict(showgrid=True))
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("<h3 style='font-size: 15px;'>Plot Pertumbuhan Usage</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig_usage)
    with col2:
        st.write("<h3 style='font-size: 15px;'>Plot Pertumbuhan Rows</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig_rows)

    # Display prediction details
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("<h3 style='font-size: 15px;'>Monthly Prediction Details</h3>", unsafe_allow_html=True)
        st.dataframe(df_monthly)
    with col2:
        st.header("")
        if period == 365:
            st.write("Total prediction usage 1 tahun kedepan yaitu", sum_usage, "MB")
        elif period == 730:
            st.write("Total prediction usage 2 tahun kedepan yaitu", sum_usage, "MB")
        elif period == 1095:
            st.write("Total prediction usage 3 tahun kedepan yaitu", sum_usage, "MB")
        
    
    
