import requests
import streamlit as st
import numpy as np
import pandas as pd
from sodapy import Socrata
import os
import base64

#Fetch the data from CFTC Website
def FetchData(date, commodity):
    client = Socrata("publicreporting.cftc.gov", None)
    results = client.get(
                        "6dca-aqww",
                        limit=100,
                        select="market_and_exchange_names AS name, commodity_name AS type, report_date_as_yyyy_mm_dd AS date, noncomm_positions_long_all AS long, noncomm_positions_short_all AS short",
                        where="commodity_name IN ('GOLD', 'SILVER')",
                        order = "report_date_as_yyyy_mm_dd DESC" )
    results_df = pd.DataFrame.from_records(results)
    return results_df

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("img.png")

#App Interface

page_bg_img =  """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://img.freepik.com/premium-vector/economy-finance-concept-financial-business-statistics-stock-market-candlesticks-bar-chart_120819-2230.jpg?w=1060");
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
st.markdown('A title with _italics_ :red[colors] and emojis :sunglasses:')

