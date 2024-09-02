import streamlit as st
import pandas as pd
import pyodbc
from server_77.def_model import model

def get_database_size(server_name, database_name, username_id, passwords):
    driver = '{ODBC Driver 17 for SQL Server}'  
    server = server_name
    database = database_name
    username = username_id
    password = passwords
    conn_str = (
        f"Driver={driver};"
        f"Server={server};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password}")
    conn = pyodbc.connect(conn_str)
    sql_query = "SELECT sum(CONVERT(DECIMAL(12,2), df.size * 8 / 1024.0)) + sum(CONVERT(DECIMAL(12,2), (df.size - CAST(FILEPROPERTY(df.name, 'SpaceUsed') AS INT)) * 8 / 1024.0)) FROM sys.master_files df WHERE df.database_id = DB_ID()"
    df = pd.read_sql(sql_query, conn)
    return df

def calculate_usage(tables, days):
    total_sum = 0
    for table in tables:
        sum_usage, *rest = model(f"select * from {table.lower().replace(' ', '_')}_usage", days)
        total_sum += sum_usage
        globals()[f'sum_usage_{table}'] = sum_usage
    return total_sum






    


