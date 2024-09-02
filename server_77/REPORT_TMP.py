import pandas as pd
import pyodbc
import streamlit as st
from server_77.def_time import monthly
from server_77.def_view import daily
from server_77.def_callmonthly import call_monthly
from server_77.def_statis import get_database_size
from server_77.def_statis import calculate_usage


def show_page3():
    st.title("REPORT_TMP")

    existing_TMP = int(get_database_size("192.168.140.178", "Report_TMP", "pekerja", "P@SDB_PKR2021").iloc[0, 0])
    TMP1 = ["TMP_01", "TMP_02"]
    TMP2 = ["TMP_06_Detail", "TMP_07_Detail"]
    total_sum_usage_TMP = calculate_usage(TMP1, 1095) + calculate_usage(TMP2, 36)
    
    st.write("Total storage usage Report_TMP data existing:", existing_TMP, "MB")
    st.write("Total prediction Report_TMP usage (3 tahun):", round(total_sum_usage_TMP), "MB")
    st.write("Total kebutuhan Report_TMP sampai 3 tahun kedepan:", round(existing_TMP + total_sum_usage_TMP), "MB")
    st.header("")
    #st.write(f"<h3 style='text-align: center; font-size: 28px;'>PREDICTION DETAILS</h3>", unsafe_allow_html=True)

    days_mapping = {
        "1 Tahun": 365,
        "2 Tahun": 730,
        "3 Tahun": 1095}
    
    header_mapping1 = {
        "TMP_01": "TMP 01 CIP CAPTIVE NON CAPTIVE",
        "TMP_02": "TMP 02 KARK"}
       
    header_mapping2 = {
        "TMP_06_Detail" : "TMP 06 OJK PREMIUM DETAIL",
        "TMP_07_Detail" : "TMP 07 CLAIM OJK DETAIL"}
    
    # Define the column layout
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_table = st.selectbox("Pilih Table", ["None", "TMP_01", "TMP_02", "TMP_06_Detail", "TMP_07_Detail"])
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

    

    