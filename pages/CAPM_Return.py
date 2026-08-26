# importing libraries

import datetime
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader.data as web
import pages.utils.capm_functions as capm_functions

st.set_page_config(
    page_title = "CAPM",
    page_icon= "chart_with_upwards_trend",
    layout = 'wide'
)

st.title("Capital Asset Pricing Model")

# getting input from user

col1,col2 = st.columns([1,1])

with col1:
    stocks_list = st.multiselect("Choose 4 Stocks", ('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL','META','JPM'), ['TSLA','AAPL','AMZN','GOOGL'])
with col2:
    year = st.number_input("Number Of Years",1,10)

# downloading data for SP500
try :
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)

    SP500 = web.DataReader(['sp500'],'fred',start,end)

    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock,period = f'{year}y')
        stocks_df[f'{stock}'] = data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date','sp500']

    stocks_df = pd.merge(stocks_df, SP500, on = 'Date', how = 'inner')
    
    col1,col2 = st.columns([1,1])

    with col1:
        st.markdown("### DataFrame Head")
        st.dataframe(stocks_df.head(),width = 'stretch')

    with col2:
        st.markdown("### DataFrame Tail")
        st.dataframe(stocks_df.tail(),width = 'stretch')

    col1,col2 = st.columns([1,1])

    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))

    with col2:
        st.markdown("### Price of all the Stocks (After Normalizing)")
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))
    
    stocks_daily_return = capm_functions.daily_return(stocks_df)
    
    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i!='Date' and i != 'sp500':
            b,a = capm_functions.calculate_beta(stocks_daily_return,i)

            beta[i] = b
            alpha[i] = a

    beta_df = pd.DataFrame(columns = ['Stock','Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df,width='stretch',hide_index=True)

    rf = 0
    rm = stocks_daily_return['sp500'].mean()*252

    return_df = pd.DataFrame()
    return_value = []

    for stock,value in beta.items():
        return_value.append(str(round(rf + (value * (rm-rf)),2)))

    return_df['Stock'] = stocks_list
    return_df['Return Value'] = return_value

    with col2:
        st.markdown("### Calculated Return using CAPM")
        st.dataframe(return_df,width='stretch',hide_index=True)

except:
    st.write("Please Select Valid Inputs")
