import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from server_77.def_statis import get_database_size
from server_77.def_statis import calculate_usage


def show_home():
    st.title("Halaman Beranda")
    st.write("Selamat datang di halaman analisa server database tim Data Management")

    existing_DWH = int(get_database_size("192.168.140.77", "DWH", "pekerja", "P@SDB_PKR2021").iloc[0, 0])
    existing_TMP = int(get_database_size("192.168.140.178", "Report_TMP", "pekerja", "P@SDB_PKR2021").iloc[0, 0])

    #DEFINING TABLES
    DWH1 = ["Produksi_Care", "Produksi_Segmentasi", "Data_Teknik_New"]
    DWH2 = ["IncomeExpense", "HasilUnderwriting"]
    TMP1 = ["TMP_01", "TMP_02"]
    TMP2 = ["TMP_06_Detail", "TMP_07_Detail"]
    total_sum_usage_DWH = calculate_usage(DWH1, 1095) + calculate_usage(DWH2, 36)
    total_sum_usage_TMP = calculate_usage(TMP1, 1095) + calculate_usage(TMP2, 36)

    data = pd.DataFrame({
        'Database': ['DWH', 'Report_TMP'],
        'Usage Prediction': [total_sum_usage_DWH, total_sum_usage_TMP],
        'Existing Size': [existing_DWH, existing_TMP],
        'Total': [total_sum_usage_DWH+existing_DWH, total_sum_usage_TMP+existing_TMP]})

    # Create stacked bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['Database'],
        y=data['Usage Prediction'],
        name='Usage Prediction'))

    fig.add_trace(go.Bar(
        x=data['Database'],
        y=data['Existing Size'],
        name='Existing Size'))

    fig.add_trace(go.Bar(
        x=data['Database'],
        y=data['Total'],
        name='Total'))
    
    fig.update_layout(barmode='stack', title='Databases Actual and Prediction Size Summary', xaxis_title='Database', yaxis_title='Values')

    # Display in Streamlit
    st.plotly_chart(fig)

    
    

   

        
