
import pandas as pd
import plotly.express as px

import streamlit as st
import pandas as pd
import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pytz
import os
import plotly.express as px
import streamlit as st
import streamlit as st
import pandas as pd
import datetime
import glob
import matplotlib.pyplot as plt
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
#ctx = get_script_run_ctx()
#session_info = runtime.get_instance().get_client(ctx.session_id)
#ar = session_info.request.remote_ip
#print(ctx)
#print(session_info)
#print(ar)


ctx = get_script_run_ctx()
print(ctx)
if ctx is not None:
    
    try:
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info and session_info.request:
            ar = session_info.request.remote_ip
            indian_timezone = pytz.timezone('Asia/Kolkata')
            indian_time = datetime.datetime.now(indian_timezone)
            formatted_time = indian_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"The current time in India is: {formatted_time}")
            print(f"Context: {ctx}")
            print(f"Session Info: {session_info}")
            print(f"Remote IP: {ar}")
        else:
            print("Session info or request object is missing.")
    except Exception as e:
        print(f"An error occurred while fetching session info: {e}")
else:
    print("Failed to retrieve script context.")
option = st.sidebar.radio(
    'Select an option:', 
    ['Shareholding Pattern', 'top Promoters', 'Promoter share in any company'], 
    index=0  
)

#df = pd.read_csv("/home/zxc/rag/try2.csv")
df = pd.read_csv("/home/micro2/Documents/ana1/try2.csv")


st.sidebar.header('Options')


if option == 'top Promoters':
    ti = st.number_input("Select_Top", min_value=0, max_value=100, step=0)
    st.write("cmbvjcxxbvb",ti)

    top_promoters = df['Promoter'].value_counts().head(ti).index
    #top_promoters = top_promoters.drop("Promoters")
    selected_promoter = st.sidebar.selectbox('Select Promoter:', top_promoters)


    top_promoter_df = df[df['Promoter'] == selected_promoter]

    def plot_stock_data(data, stock_list):
        for stock in stock_list:
            filtered_data = data[data["NSE Code"] == stock]
            df = pd.DataFrame(filtered_data)

            df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
            a = data["Promoter"].iloc[0]
            b = data["BSE Code"].iloc[0]

            plt.figure(figsize=(10, 6))
            plt.plot(df['Date'], df['Share'], marker='o', label=stock)
            plt.title(f'{stock} - {a} - {b}')
            plt.xlabel('Date')
            plt.ylabel('Share Price')
            plt.grid(True)
            plt.legend()

            st.pyplot(plt)
            plt.close()


    if not top_promoter_df.empty:
        a = top_promoter_df["NSE Code"].unique()
        plot_stock_data(top_promoter_df, a)
    else:
        st.write("No data available for the selected promoter.")

elif option == 'Promoter share in any company':

    #selected_promoter = st.text_input("")
    promoter_options = ["None"] + df['Promoter'].unique().tolist()
    #selected_promoter = st.selectbox("Select a Promoter", df['Promoter'].unique())
    selected_promoter = st.sidebar.selectbox("Select a Promoter", promoter_options)
    
    st.write(f'You selected: {selected_promoter}')



    top_promoter_df = df[df['Promoter'] == selected_promoter]

    def plot_stock_data(data, stock_list):
        for stock in stock_list:
            filtered_data = data[data["NSE Code"] == stock]
            df = pd.DataFrame(filtered_data)
            print(df)

            df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
            a = data["Promoter"].iloc[0]
            b = data["BSE Code"].iloc[0]

            plt.figure(figsize=(10, 6))
            plt.plot(df['Date'], df['Share'], marker='o', label=stock)
            plt.title(f'{stock} - {a} - {b}')
            plt.xlabel('Date')
            plt.ylabel('Share Price')
            plt.grid(True)
            plt.legend()

            st.pyplot(plt)
            plt.close()


    if not top_promoter_df.empty:
        a = top_promoter_df["NSE Code"].unique()
        plot_stock_data(top_promoter_df, a)
    else:
        st.write("No data available for the selected promoter.")

################################################################################################
#directory = f"/home/zxc/rag/e/"
directory = '/home/micro2/Desktop/bdvc/'



#company_codes = [os.path.splitext(filename)[0] for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
#company_codes = [os.path.splitext(filename)[0] for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
#directory = '/path/to/your/directory'  # Replace with your directory path

company_codes = [
    os.path.splitext(filename)[0] 
    for filename in os.listdir(directory) 
    if os.path.isfile(os.path.join(directory, filename)) and filename.endswith('.csv')
]

st.write("This is a quarter data of promoters.")

options =  ['']+ company_codes
#options = ["Select a company code"] + company_codes
selected_code = st.selectbox("Select the company code (bse_code)/(nse_code)", options=options)

if selected_code is not None:
    # Construct the file path based on the selected code
    #path = f"/home/zxc/rag/e/{selected_code}.csv"
    path = f"/home/micro2/Desktop/bdvc//{selected_code}.csv"
    #st.write(f"File path: {path}")
else:
    print("no comany")

try:
    df = pd.read_csv(path)  # Corrected the path variable
except FileNotFoundError as e:
    st.write("File not found. Please check the file path or company code.")
    st.stop()

st.write("Data preview:")
st.dataframe(df, width=100000000)





























#@st.experimental_memo(ttl=60)
@st.cache_data
def plot_promoters(df):
    try:

        a = b = c = None

        # Check for 'FIIs' and 'DIIs'
        if 'FIIs' in df['Promoter'].values:
            diss_indices = df[df['Promoter'] == 'FIIs'].index.tolist()
            print('FIIs', diss_indices)
            a = diss_indices[0]
        elif "DIIs" in df["Promoter"].values:
            diss_indices = df[df['Promoter'] == 'DIIs'].index.tolist()
            print('DIIs', diss_indices)
            a = diss_indices[0] 
        else:
            public_indices = df[df['Promoter'] == 'Public'].index.tolist()
            print('Public', public_indices)
            a = public_indices[0] if public_indices else None
            print('a:', a)

        if a is not None:
            filtered_df = df.iloc[1:a]
            filtered_df = filtered_df.sort_values(by='Share', ascending=False)

            # Create the bar chart for Promoters
            fig = px.bar(filtered_df, x='Promoter', y='Share',
                        labels={'Promoter': 'Promoter', 'Share': 'Share'},
                        title=f"Promoters_{df['Share'][0]}",
                        text='Share')

            st.plotly_chart(fig)
        else:
            print("No valid indices found for 'a'.")

        # Check for 'DIIs' and 'Government'
        if 'DIIs' in df['Promoter'].values:
            fiis_indices = df[df['Promoter'] == 'DIIs'].index.tolist()
            print('DIIs', fiis_indices)
            b = fiis_indices[0]
        else:
            diis_indices = df[df['Promoter'] == 'Government'].index.tolist()
            print('Government', diis_indices)
            b = diis_indices[0] if diis_indices else None

        print('b:', b)

        if b is not None and "FIIs" in df["Promoter"].values:
            filtered_df = df.iloc[a+1:b]
            filtered_df = filtered_df.sort_values(by='Share', ascending=False)

            # Create the bar chart for FIIs
            fig = px.bar(filtered_df, x='Promoter', y='Share',
                        labels={'Promoter': 'FIIS', 'Share': 'Share'},
                        title=f"FIIs_{df['Share'][a]}")
            fig.update_layout(
                hoverlabel=dict(
                    font=dict(
                        family="Arial",
                        size=14,
                        color="black"
                    ),
                    bgcolor="white",
                    bordercolor="black"
                )
            )

            st.plotly_chart(fig)
        else:
            print("No valid indices found for 'b'.")

        # Check for 'Government' and 'Public'
        if 'Government' in df['Promoter'].values:
            fiis_indices = df[df['Promoter'] == 'Government'].index.tolist()
            print('Government', fiis_indices)
            c = fiis_indices[0]
        elif 'Public' in df['Promoter'].values:
            diis_indices = df[df['Promoter'] == 'Public'].index.tolist()
            print('Public', diis_indices)
            c = diis_indices[0]
        else:
            print('Neither Government nor Public in Promoter column')
            c = None

        print('c:', c)


        if c is not None and "DIIs" in df["Promoter"].values:
            filtered_df = df.iloc[b+1:c]
            filtered_df = filtered_df.sort_values(by='Share', ascending=False)


            fig = px.bar(filtered_df, x='Promoter', y='Share',
                        labels={'Promoter': 'DIIS', 'Share': 'Share'},
                        title=f"DIIs_{df['Share'][b]}")
            fig.update_layout(
                hoverlabel=dict(
                    font=dict(
                        family="Arial",
                        size=14,
                        color="black"
                    ),
                    bgcolor="white",
                    bordercolor="black"
                )
            )

            st.plotly_chart(fig)
        else:
            print("No valid indices found for 'c'.")
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

