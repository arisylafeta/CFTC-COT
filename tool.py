import requests
import streamlit as st
import numpy as np
import pandas as pd
from sodapy import Socrata
import os
import base64
from datetime import datetime
import altair as alt
import plotly.express as px

def comTrans(selection):
    match selection:
        case 'SP500':
            id = '13874+'
        case 'NDX100':
            id = '20974+'
        case 'GOLD':
            id = '088691'
        case 'SILVER':
            id = '084691'
        case 'USOIL':
            id = '06765I'
        case 'EURUSD':
            id = '099741'
        case 'GBPUSD':
            id = '096742'
        case 'JPYUSD':
            id = '097741'
        case 'NZDUSD':
            id = '112741'
        case 'AUDUSD':
            id = '232741'
        case 'CADUSD':
            id = '090741'
        case 'CHFUSD':
            id = '092741'
    return id

#Fetch the data from CFTC Website
def FetchData(commodity):
    client = Socrata("publicreporting.cftc.gov", None)
    results = client.get(
                        "6dca-aqww",
                        limit=100,
                        select='''contract_market_name AS name,
                                cftc_contract_market_code as id,  
                                commodity_name AS type, 
                                report_date_as_yyyy_mm_dd AS date, 
                                open_interest_all as open_interest,
                                change_in_open_interest_all as interest_change, 
                                noncomm_positions_long_all AS long, 
                                noncomm_positions_short_all AS short, 
                                comm_positions_long_all AS comm_long, 
                                comm_positions_short_all AS comm_short,
                                change_in_noncomm_long_all as long_change,
                                change_in_noncomm_short_all as short_change, 
                                change_in_comm_long_all as comm_long_change,
                                change_in_comm_short_all as comm_short_change''',
                        where=f"cftc_contract_market_code = '{commodity}'",
                        order = "report_date_as_yyyy_mm_dd DESC" )
    results_df = pd.DataFrame.from_records(results)
    return results_df


#App Interface

page_bg_img =  """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://i.imgur.com/y8o7Vq3.jpg");
background-size: cover;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title('Welcome to Trading Pal :chart:')
st.text('''Trading Pal is a tool that helps you analyze the COT Report. 
Select the commodity and timespan and check what institutions are doing.''')
st.write("")
col1, col2 = st.columns(2)

with col1:
    commodity = st.selectbox("1. Select your commodity", ('SP500', 'NDX100', 'GOLD', 'SILVER', 'USOIL', 'EURUSD', 'GBPUSD', 'JPYUSD', 'CADUSD', 'AUDUSD' ,'NZDUSD',  'CHFUSD'))
with col2:
    st.write('')
    
if st.button("Let's get it"):
        commodityID = comTrans(commodity)
        df = FetchData(commodityID)
        df['date'] = df['date'].apply(lambda x: x[:-13])
        showdata = df[['date', 'long', 'short', 'long_change', 'short_change']]
        st.dataframe(showdata)


        


