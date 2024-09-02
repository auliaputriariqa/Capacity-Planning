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

driver = '{ODBC Driver 17 for SQL Server}'  
server = '192.168.140.218'
database = 'RnD_Sumber_Forecast'
username = 'pekerja'
password = 'Brinsatgram22'
conn_str = (
    f"Driver={driver};"
    f"Server={server};"
    f"Database={database};"
    f"UID={username};"
    f"PWD={password}")
conn = pyodbc.connect(conn_str)
query = "SELECT * FROM TableSpaceUsage WHERE (DATE BETWEEN '2014-01-01' AND '2015-08-31') OR DATE IS NULL"
df = pd.read_sql(query, conn)
# df

df['usage'] = df['Reserved'].str.replace(' KB', '', regex=False).astype(int)

df['DATE_filled'] = df['DATE'].fillna(method='bfill') - pd.Timedelta('1 day')
df['DATE'].fillna(df['DATE_filled'], inplace=True)
df.drop('DATE_filled', axis=1, inplace=True)

df = df.sort_values(by='DATE', ascending=True)

cols = ['TableName', 'Rows', 'Reserved', 'Data', 'IndexSize', 'Unused', 'TGL_RECORD']
df.drop(cols, axis=1, inplace=True)

df['DATE'] = pd.to_datetime(df['DATE'])
df = df.set_index('DATE')

df['day'] = df.index.day
df['month'] = df.index.month
df['day_of_week'] = df.index.dayofweek
df['lag_1'] = df['usage'].shift(1)
# Drop rows with NaN values
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

fig = plt.figure(figsize=(10, 6))
plt.plot(df.index, df['usage'], label='Historical Data', marker='o')
plt.plot(future_dates, future_predictions, label='Forecast', color='red', marker='x')
plt.xlabel('Date')
plt.ylabel('Usage')
plt.title('Database Usage Forecasting')
plt.legend()
plt.grid(True)

st.pyplot(fig)

data = {'date': future_dates, 'usage': future_predictions}
df = pd.DataFrame(data)
pd.set_option('display.max_rows', None)
# print(df[['date', 'usage']])

# # Streamlit app
# st.title('Matplotlib Plot in Streamlit')

# # Display DataFrame
# st.write("Here is the DataFrame:")
st.dataframe(df)

# # Create Matplotlib plot
# fig, ax = plt.subplots()
# ax.plot(df['date'], df['usage'], marker='o', linestyle='-')
# ax.set_xlabel('date')
# ax.set_ylabel('usage')
# ax.set_title('Sample Time Series Data')

# # Display plot in Streamlit
# st.pyplot(fig)