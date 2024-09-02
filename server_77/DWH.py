import pandas as pd
import pyodbc
import streamlit as st
from server_77.def_time import monthly
from server_77.def_view import daily
from server_77.def_callmonthly import call_monthly
from server_77.def_statis import get_database_size
from server_77.def_statis import calculate_usage

def show_page2():
    st.title("DWH")

    existing_DWH = int(get_database_size("192.168.140.77", "DWH", "pekerja", "P@SDB_PKR2021").iloc[0, 0])
    DWH1 = ["Produksi_Care", "Produksi_Segmentasi", "Data_Teknik_New"]
    DWH2 = ["IncomeExpense", "HasilUnderwriting"]
    total_sum_usage_DWH = calculate_usage(DWH1, 1095) + calculate_usage(DWH2, 36)
    
    st.write("Total storage usage DWH data existing:", existing_DWH, "MB")
    st.write("Total prediction DWH usage (3 tahun):", round(total_sum_usage_DWH), "MB")
    st.write("Total kebutuhan DWH sampai 3 tahun kedepan:", round(existing_DWH + total_sum_usage_DWH), "MB")
    st.header("")
    #st.write(f"<h3 style='text-align: center; font-size: 28px;'>PREDICTION DETAILS</h3>", unsafe_allow_html=True)

    days_mapping = {
        "1 Tahun": 365,
        "2 Tahun": 730,
        "3 Tahun": 1095}
    
    header_mapping1 = {
        "Produksi_Care": "PRODUKSI CARE",
        "Produksi_Segmentasi": "PRODUKSI SEGMENTASI",
        "Data_Teknik_New" : "DATA TEKNIK NEW"}
       
    header_mapping2 = {
        "IncomeExpense" : "INCOME EXPENSE",
        "HasilUnderwriting" : "HASIL UNDERWRITING",
        "DataTeknik_Klaim" : "DATA TEKNIK KLAIM"}
    
    # Define the column layout
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_table = st.selectbox("Pilih Table", ["None", "Produksi_Care", "Produksi_Segmentasi", "Data_Teknik_New", "IncomeExpense", "HasilUnderwriting", "DataTeknik_Klaim"])
    with col2:
        period_filter = st.selectbox('Forecast Period', ["None", "1 Tahun", "2 Tahun", "3 Tahun"])
    with col3:
        view_filter = st.selectbox('Tampilan Data', ["None", "Monthly", "Daily"])

    st.header("")

    # Get the number of days based on period_filter
    days = days_mapping.get(period_filter)

    # Check if a valid table is selected
    if filter_table in header_mapping1 and period_filter in days_mapping and view_filter in ["Monthly", "Daily"]:
        st.write(f"<h3 style='text-align: center; font-size: 28px;'>{header_mapping1[filter_table]}</h3>", unsafe_allow_html=True)
        
        query = f"select * from {filter_table.lower().replace(' ', '_')}_usage"
        
        # Call the appropriate function based on view_filter
        if view_filter == "Daily":
            daily(query, days)
        elif view_filter == "Monthly":
            monthly(query, days)
    elif filter_table in header_mapping2 and period_filter in days_mapping and view_filter in ["Monthly", "Daily"]:
        st.write(f"<h3 style='text-align: center; font-size: 28px;'>{header_mapping2[filter_table]}</h3>", unsafe_allow_html=True)
        
        query = f"select * from {filter_table.lower().replace(' ', '_')}_usage"
        
        # Call the appropriate function based on view_filter
        if view_filter == "Daily":
            st.write("Data hanya tersedia bulanan.")
        elif view_filter == "Monthly" and period_filter == "1 Tahun":
            call_monthly(query, 12)
        elif view_filter == "Monthly" and period_filter == "2 Tahun":
            call_monthly(query, 24)
        elif view_filter == "Monthly" and period_filter == "3 Tahun":
            call_monthly(query, 36)
    else:
        st.write("Silahkan pilih valid table, forecast period, dan tampilan data.")


    