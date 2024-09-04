import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

import os
import plotly.express as px
import streamlit as st
import streamlit as st
import pandas as pd
import datetime


df1 = pd.read_csv('/home/micro2/Documents/ana1/try.csv')
option = st.sidebar.radio(
    'Select an option:', 
    ['None', 'Plot Stock Data by Promoter', 'Plot Summary Statistics'], 
    index=0  
)

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df1.columns:
    df1 = df1.drop(columns=['Unnamed: 0'])

# Input for company code
title = st.text_input("Enter the company code (BSE Code/NSE Code)", "")
print(title)
print(df1.dtypes)


# Filter the DataFrame based on the input
df = df1[df1['NSE Code'] == f'{title}']
print(df)

# If no matching records, return an error
if df.empty:
    st.write("No records found for the provided company code.")
else:
    # Display the filtered DataFrame without the index
    #st.write(df.to_html(index=False), unsafe_allow_html=True)
    st.write("Data preview:")
    st.dataframe(df, width=100000000)






























#@st.experimental_memo(ttl=60)
@st.cache_data
def plot_promoters(df):
    try:

        a = b = c = None




        filtered_df = df.iloc[1:]
        filtered_df = filtered_df.sort_values(by='Share', ascending=False)

        # Create the bar chart for Promoters
        fig = px.bar(filtered_df, x='Promoter', y='Share',
                    labels={'Promoter': 'Promoter', 'Share': 'Share'},
                    title=f"Promoters_{df['Share'][0]}",
                    text='Share')

        st.plotly_chart(fig)






    except TypeError as e:
        print("data error") 




df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce').dt.date

# Get unique dates and format them
dates = df['Date'].unique()
dates_series = pd.Series(dates)
formatted_dates = dates_series.apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else 'NaT')
formatted_dates_list = [date for date in formatted_dates if date != 'NaT']

# Streamlit app
st.title('quarter Selection')

# Convert formatted_dates_list to a list of datetime.date objects
formatted_dates_list = [pd.to_datetime(date).date() for date in formatted_dates_list]

d = st.selectbox('Select a date:', formatted_dates_list)

# Convert selected date to the format used in DataFrame
selected_date = pd.to_datetime(d).date()

st.write(f'Selected date: {selected_date}')

print("date", selected_date)
print(df)
print(df['Date'])

if st.button('Submit'):
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]) 
    # Filter data based on selected_date
    filtered_data = df[df['Date'] == selected_date]

    filtered_data = filtered_data.reset_index(drop=True)
    st.dataframe(filtered_data)

    if not filtered_data.empty:
        plot_promoters(filtered_data)  
    else:
        st.write("No data available for the selected date.")

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("/home/micro2/Documents/ana1/try.csv")

# Sidebar
st.sidebar.header('Options')

# Option 1: Plot stock data for a selected promoter
#option = st.sidebar.radio('Select an option:', ['Plot Stock Data by Promoter', 'Plot Summary Statistics'])
#option = st.sidebar.radio(
    #'Select an option:', 
    #['None', 'Plot Stock Data by Promoter', 'Plot Summary Statistics'], 
    #index=0  )
if option == 'Plot Stock Data by Promoter':
    # Select Promoter
    top_promoters = df['Promoter'].value_counts().head(10).index
    top_promoters = top_promoters.drop("Promoters")
    selected_promoter = st.sidebar.selectbox('Select Promoter:', top_promoters)

    # Filter data based on selected Promoter
    top_promoter_df = df[df['Promoter'] == selected_promoter]

    def plot_stock_data(data, stock_list):
        for stock in stock_list:
            filtered_data = data[data["NSE Code"] == stock]
            df = pd.DataFrame(filtered_data)

            df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
            a = data["Promoter"].iloc[0]

            plt.figure(figsize=(10, 6))
            plt.plot(df['Date'], df['Share'], marker='o', label=stock)
            plt.title(f'{stock} - {a}')
            plt.xlabel('Date')
            plt.ylabel('Share Price')
            plt.grid(True)
            plt.legend()

            st.pyplot(plt)
            plt.close()

    # Plot data for the selected promoter
    if not top_promoter_df.empty:
        a = top_promoter_df["NSE Code"].unique()
        plot_stock_data(top_promoter_df, a)
    else:
        st.write("No data available for the selected promoter.")

elif option == 'Plot Summary Statistics':
    #top_promoters = df['Promoter']
    #top_promoters = top_promoters.drop("Promoters")
    #elected_promoter = st.sidebar.selectbox('Select Promoter:', top_promoters)
    selected_promoter = st.text_input("")

    # Filter data based on selected Promoter
    top_promoter_df = df[df['Promoter'] == selected_promoter]

    def plot_stock_data(data, stock_list):
        for stock in stock_list:
            filtered_data = data[data["NSE Code"] == stock]
            df = pd.DataFrame(filtered_data)

            df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
            a = data["Promoter"].iloc[0]

            plt.figure(figsize=(10, 6))
            plt.plot(df['Date'], df['Share'], marker='o', label=stock)
            plt.title(f'{stock} - {a}')
            plt.xlabel('Date')
            plt.ylabel('Share Price')
            plt.grid(True)
            plt.legend()

            st.pyplot(plt)
            plt.close()

    # Plot data for the selected promoter
    if not top_promoter_df.empty:
        a = top_promoter_df["NSE Code"].unique()
        plot_stock_data(top_promoter_df, a)
    else:
        st.write("No data available for the selected promoter.")
    











