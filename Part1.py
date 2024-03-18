import sys
from pyqes import micsvc
import pandas as pd
import requests
from datetime import datetime
import pytz
import streamlit as st

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

ticker_input = st.text_input('Enter a ticker symbol:', '').upper() 
ticker_input_upper = ticker_input.upper()  
df = pd.DataFrame(columns=["TICKER", "WEIGHT"])
new_row = pd.DataFrame({'TICKER': [ticker_input], 'WEIGHT': [1]})
df = pd.concat([df, new_row], ignore_index=True)
df.rename(columns={"Column1": "TICKER", "NewColumn": "WEIGHT"}, inplace=True)
today_date = datetime.now().strftime('%Y-%m-%d')
eastern_tz = pytz.timezone('US/Eastern')
df.insert(0, "DATE", datetime.now(eastern_tz).strftime("%Y-%m-%d"))
portfolio_df = df

if st.button('Submit'):

    user_name = st.secrets["user_name"]
    pass_word = st.secrets["pass_word"]
    connection = micsvc.Connection(username = user_name, password = pass_word)

    attribution_broad = connection.get_attribution()
    attribution_broad.set_risk_model('QES_US_AC_2')
    attribution_broad.set_user_data(name='attribution_data.csv', data=portfolio_df)
    attribution_broad.set_weight_factor(weight_factor='WEIGHT')
    attribution_broad.submit()
    attribution_broad.wait(max_wait_secs=600)
    broad_att_result = attribution_broad.get_results()
    st.write('Summary:')
    st.dataframe(broad_att_result.get_summary())
    st.write('Exposure:')
    correlation_matrix = broad_att_result.get_exposures()
    transposed_correlation_matrix = correlation_matrix.T
    num_rows = transposed_correlation_matrix.shape[0]
    st.dataframe(transposed_correlation_matrix, height=35*num_rows, width = 340)

