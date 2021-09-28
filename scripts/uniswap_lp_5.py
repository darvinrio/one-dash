# setting up environment
import pandas as pd
import numpy as np
import requests
import time
import copy
import json
from datetime import datetime as dt

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import NumeralTickFormatter, CustomJS

from scripts.formatters import format_money
from scripts.process_plot import get_div

# import socket
# old_getaddrinfo = socket.getaddrinfo
# def new_getaddrinfo(*args, **kwargs):
#     responses = old_getaddrinfo(*args, **kwargs)
#     return [response
#             for response in responses
#             if response[0] == socket.AF_INET]
# socket.getaddrinfo = new_getaddrinfo

color_dict={
    'WETH-USDT 3000 60':'#259c77',
    'USDC-USDT 500 10':'#f4b731',
    'USDC-WETH 3000 60':'#256fc0',
    'FRAX-USDC 500 10':'black',
    'WBTC-WETH 3000 60':'#ff0079'
}

def get_uni_top5():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/3a807bea-3e78-46ef-9b8c-2604a1bf38d1/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['BLOCK_HOUR'] = pd.to_datetime(df['BLOCK_HOUR']).dt.tz_localize(None)
    return df

def make_uni_top5_lp_plot():
    global uni_top_df
    uni_top_df = get_uni_top5()

    p = figure(plot_height=400,x_axis_type='datetime'
                  ,sizing_mode="stretch_width",tools='xwheel_zoom,ywheel_zoom,xpan,reset')

    for pool in list(uni_top_df['POOL_NAME'].unique()):
        src = uni_top_df[uni_top_df['POOL_NAME']==pool]
        line = p.line(source=cds(src),x='BLOCK_HOUR',y='TVL_USD',
                    line_width=2,legend_label=pool,color=color_dict[pool])


    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    tooltips = [('Date', '@BLOCK_HOUR{%F}'),('TVL', '@TVL_USD{($ 00.00 a)}'),
            ('Pool','@POOL_NAME')]
    hovertool = HoverTool(tooltips=tooltips,formatters={'@BLOCK_HOUR': 'datetime'})
    p.add_tools(crosshair,hovertool)
    p.legend.click_policy="hide"

    p.legend.label_text_font_size = '8pt'
    p.legend.location='top_left'
    p.grid.visible = False
    p.yaxis.formatter=NumeralTickFormatter(format="$ 0.00 a")

    return get_div(p)

def make_top5_lp_today():
    today_tvl = uni_top_df[uni_top_df['BLOCK_HOUR'] == uni_top_df['BLOCK_HOUR'].max()][['POOL_NAME','TVL_USD']]
    today_tvl['TVL_USD'] = today_tvl['TVL_USD'].apply(format_money)
    result = today_tvl.to_dict(orient="records")

    return result

uni_top5_lp_plot = make_uni_top5_lp_plot()
top5_lp_today = make_top5_lp_today()

def get_uni_top5_lp_plot():
    return uni_top5_lp_plot,top5_lp_today

