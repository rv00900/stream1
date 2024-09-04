import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("/home/micro2/Documents/ana1/try.csv")

# Sidebar
st.sidebar.header('Options')

# Option 1: Plot stock data for a selected promoter
option = st.sidebar.radio('Select an option:', ['Plot Stock Data by Promoter', 'Plot Summary Statistics'])

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
    

