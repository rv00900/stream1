

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
import plotly.graph_objects as go
from streamlit.runtime.scriptrunner import get_script_run_ctx

from jugaad_data.nse import NSELive
n = NSELive()

from bsedata.bse import BSE
b = BSE()
b = BSE(update_codes = True)
#ctx = get_script_run_ctx()
#session_info = runtime.get_instance().get_client(ctx.session_id)
#ar = session_info.request.remote_ip
#print(ctx)
#print(session_info)
#print(ar)
###################################################
def plot_promoter_share_over_time(fg):
    try:
        # Convert DataFrame column to datetime
        df = pd.DataFrame(fg)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.strftime('%Y-%d-%m')


        df_pivot = df.pivot(index='Date', columns='BSE Code', values='Share')


        fig = go.Figure()

        for promoter in df_pivot.columns:
            fig.add_trace(go.Scatter(
                x=df_pivot.index,
                y=df_pivot[promoter],
                mode='lines+markers',
                name=promoter
            ))


        fig.update_layout(
            title='Promoter Share Over Time',
            xaxis_title='Date',
            yaxis_title='Share',
            xaxis=dict(tickangle=-45),
            legend_title='BSE Code',
            width=1000,
            height=600
        )
        st.plotly_chart(fig)
    except Exception as e:
        print("error in date")
    #fig.show()



###################################################################################
def line(data):

    df = data


    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%Y-%d-%m')


    df_pivot = df.pivot(index='Date', columns='Promoter', values='Share')

    fig = go.Figure()


    for promoter in df_pivot.columns:
        fig.add_trace(go.Scatter(
            x=df_pivot.index,
            y=df_pivot[promoter],
            mode='lines+markers',
            name=promoter
        ))


    fig.update_layout(
        title='Promoter Share Over Time',
        xaxis_title='Date',
        yaxis_title='Share',
        xaxis=dict(tickangle=-45),
        legend_title='Promoter',
        width=1000,
        height=600
    )


    st.plotly_chart(fig)
ctx = get_script_run_ctx()
#print(ctx)
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
    ['Shareholding Pattern', 'Top Promoters', 'Promoter Share in Any Company',"try","tr2","Increased share by month"],index=0)
#df = pd.read_csv("/home/zxc/rag/try2.csv")
df = pd.read_csv("try2.csv")



st.sidebar.header('Options')

def plot_stock_data(data, stock_list):
    for stock in stock_list:
        filtered_data = data[data["BSE Code"] == stock]
        if filtered_data.empty:
            st.write(f"No data available for BSE Code: {stock}")
            continue

        df = pd.DataFrame(filtered_data)
        df = df.drop_duplicates(subset=['Date'])

        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        promoter_name = df["Promoter"].iloc[0]
        bse_code = df["BSE Code"].iloc[0]
        nse_code = df["NSE Code"].iloc[0]

        fig = px.line(df, x='Date', y='Share', markers=True, title=f'{nse_code} - {promoter_name} - {bse_code}')


        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Share Price',
            showlegend=True
        )

        st.plotly_chart(fig)

if option == 'Top Promoters':
    top_promoter_count = st.number_input("Select Top Promoters", min_value=1, max_value=100, step=1)
    top_promoters = df['Promoter'].value_counts().head(top_promoter_count).index
    promoter_options = ["None"] + list(top_promoters)
    selected_promoter = st.sidebar.selectbox('Select Promoter:', promoter_options)

    top_promoter_df = df[df['Promoter'] == selected_promoter]
    plot_promoter_share_over_time(top_promoter_df)

    if not top_promoter_df.empty:
        bse_codes = top_promoter_df["BSE Code"].unique()
        plot_stock_data(top_promoter_df, bse_codes)
    else:
        st.write("No data available for the selected promoter.")

elif option == 'Promoter Share in Any Company':
    promoter_options = ["None"] + df['Promoter'].unique().tolist()
    selected_promoter = st.sidebar.selectbox("Select a Promoter", promoter_options)

    if selected_promoter == "None":
        st.write("No promoter selected.")
    else:
        st.write(f'You selected: {selected_promoter}')
        top_promoter_df = df[df['Promoter'] == selected_promoter]
        #print(top_promoter_df)
        
        #if top_promoter_df["BSE Code"].unique().count >1:
        if len(top_promoter_df["BSE Code"].unique()) > 1 :
           plot_promoter_share_over_time(top_promoter_df)

        ################################################################################
        if not top_promoter_df.empty:
            stock_codes = top_promoter_df["BSE Code"].unique()

            plot_stock_data(top_promoter_df, stock_codes)
            #plot_promoter_share_over_time(top_promoter_df)
####################################################################################################



###############################################################################################################################
        else:
            st.write("No data available for the selected promoter.")

elif option == "tr2":
    d1 = ["None"] + df["BSE Code"].unique().tolist()
    d = st.sidebar.selectbox("Select a Compamy", d1)
    if d !="None":
        dr =df[df["BSE Code"]==d]
        st.dataframe(dr)
        line(dr)
        dr['Date'] = pd.to_datetime(dr['Date'])
        dr['Date'] = dr['Date'].dt.date
        dates = dr["Date"].unique()
        selected_date = st.sidebar.selectbox("Select a date:", sorted(dates, reverse=True))
        dr = dr[dr["Date"]==selected_date]
        #dr = dr.reset_index(drop=True)
        #del dr["Unnamed: 0"]
        st.dataframe(dr.reset_index(drop = True))



##########################################################################################
elif option == "try":
    promoter_options = ["None"] + df['Promoter'].unique().tolist()
    selected_promoter = st.sidebar.selectbox("Select a Promoter", promoter_options)
    de = df[df['Promoter'] == selected_promoter]
    d1 = ["None"] + de["BSE Code"].unique().tolist()
    d = st.sidebar.selectbox("Select a Compamy", d1)
    de = de[de["BSE Code"]==d]
    #v = de["NSE Code"].iloc[0]
    print("qwertyuioppppppppppolkmnbvc",d)


    try:
        q = b.getQuote(f"{d}")
        print(q)


        
        if q is not None:
            #st.write("Current price:", )
            #st.write("Current price:",q["currentValue"],"marketCap:",q["marketCapFull"])
            #st.write("marketCap:",q["marketCapFull"])
            #st.write(f"Current price: {q['currentValue']}, Market Cap: {q['marketCapFull']}")
            st.write(f"**Current Price:** `{q['currentValue']}` \n**Market Cap:** `{q['marketCapFull']}`")


        else:
            print("Price information is unavailable.")

    except KeyError as e:
        print(f"Error fetching current price: Missing key {e}")
    except Exception as e:
        print(f"An unexpected error occurred:")




    de["ch"] =""
    for i in range(len(de) - 1):
        j = i + 1
        if de["Share"].iloc[i] > de["Share"].iloc[j]:
            #print(">", "yes")
            de["ch"].iloc[j] = "DOWN"  
        elif de["Share"].iloc[i] < de["Share"].iloc[j]:
            #print("<", "yes")
            de["ch"].iloc[j] = "UP"  
        elif de["Share"].iloc[i+1] == de["Share"].iloc[j]:
            #print("==", "yes")
            de["ch"].iloc[j] = "EQUAL"
    #del de['Unnamed: 0']
    de.reset_index(drop=True, inplace=True)
    #st.dataframe(de)
    st.dataframe(de.T)



################################################################################################
elif option == "Increased share by month":
    du = pd.read_csv("tt6.csv")
    du['Date'] = pd.to_datetime(du['Date'])
    du['Date'] = du['Date'].dt.date
    

    dates = du["Date"].unique()
    
   # selected_date = st.selectbox("Select a date:", dates)

    selected_date = st.selectbox("Select a date:", sorted(dates, reverse=True))



    db = du[(du["Date"] == selected_date) & (du["ch"] == "UP")]
    st.dataframe(db)



    promoter_options = ["None"] + db["Promoter"].unique().tolist()
    selected_promoter = st.sidebar.selectbox("Select a Promoter", promoter_options)
    #############################################################################################
    d1 = ["None"] + db["BSE Code"].unique().tolist()
    d = st.sidebar.selectbox("Select a Compamy", d1)
    if d !="None":
        dr =df[df["BSE Code"]==d]
        #dr =df[df(["BSE Code"]==d) &(df[df"Date"]==selected_date)]
        #dr = df[(df["BSE Code"] == d) & (df["Date"] == selected_date)]
        #dr = df[(df["BSE Code"] == d) & (df["Date"] == f"{selected_date}")] 
        st.dataframe(dr)
        line(dr)
    #dr['Date'] = pd.to_datetime(dr['Date'])
    #dr['Date'] = dr['Date'].dt.date
    #dates = dr["Date"].unique()
    #selected_date = st.sidebar.selectbox("Select a date:", sorted(dates, reverse=True))
    #dr = dr[dr["Date"]==selected_date]
    #dr = dr.reset_index(drop=True)
    #del dr["Unnamed: 0"]
    #st.dataframe(dr.reset_index(drop = True))




    if selected_promoter != "None":
        tt = st.sidebar.selectbox("Select a Promoter", ["full comoany","individual","test"])
        if tt =="full comoany":
            db = du[du["Promoter"]==selected_promoter]
            st.dataframe(db)


        elif tt == "test":
            db = du[(du["Promoter"] == selected_promoter) &(du["Date"]== selected_date)]
            dv = db["BSE Code"].unique()
            r = st.sidebar.selectbox("Select a BSE Code", dv)
            print("Selected BSE Code:", r)
            dy = du[(du["BSE Code"] == r) & (du["Date"]==selected_date)]
            dj = du[du["BSE Code"] == r]
            print(dj)
            #dj.to_csv("qw.csv")
            line(dj)
            #st.dataframe(dj)
            v =dy[["Promoter","Share_Change%","BSE Code","Date"]]
            #v.to_csv("gj.csv")
            print(v)
            st.dataframe(dy)

        elif tt =="individual":
            db = du[(du["Promoter"] == selected_promoter) & (du["Date"] == selected_date)]
            print(db)

        #d = db["NSE Code"].iloc[0] if db["NSE Code"]=="nan":  db["BSE Code"].iloc[0]
        #print(d)
            db = db[["Share","MCap","Share_Change%","BSE Code"]]
            st.dataframe(db)





###############################################################################################################################################################
