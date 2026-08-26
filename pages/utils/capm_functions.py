import plotly.express as px
import numpy as np

# functions to plot interactive plotly charts
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'],y = df[i],name = i)
    fig.update_layout(
        width = 450 ,
        margin = dict(l=20,r=20,t=50,b=20),
        legend = dict(orientation = 'h' , yanchor = 'bottom' , y = 1.02 , xanchor = 'right' , x = 1)
        )
    return fig

# function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i] / df[i][0]
    return df

# function to calculate daily return
def daily_return(df):

    df_daily_return = df.copy()

    for i in df.columns[1:]:
        df_daily_return[i] = df[i].pct_change() * 100

    df_daily_return.iloc[0, 1:] = 0

    return df_daily_return

# function to calculate Beta
def calculate_beta(stocks_daily_return,stock):
    rm = stocks_daily_return['sp500'].mean()*252

    beta,alpha = np.polyfit(stocks_daily_return['sp500'],stocks_daily_return[stock],1)
    return beta,alpha