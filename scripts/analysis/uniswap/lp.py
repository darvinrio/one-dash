import pandas as pd
import numpy as np
import requests
import time
import copy
from datetime import datetime as dt

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import NumeralTickFormatter, CustomJS
from bokeh.layouts import layout

from bokeh.resources import CDN
from bokeh.embed import autoload_static

from scripts.process_plot import get_div

# import socket
# old_getaddrinfo = socket.getaddrinfo
# def new_getaddrinfo(*args, **kwargs):
#     responses = old_getaddrinfo(*args, **kwargs)
#     return [response
#             for response in responses
#             if response[0] == socket.AF_INET]
# socket.getaddrinfo = new_getaddrinfo

def get_lp_pos():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/a082884b-0efc-4ae9-a8ba-ad36f9526371/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    return df

def get_lp_pos_pct():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/02e7653c-4279-442d-b562-069fa269161c/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    return df

def make_uni_lp_plot():
    lp_df = get_lp_pos()
    lp_pct_df = get_lp_pos_pct()

    # main plot
    p = figure(x_axis_type='datetime',plot_height=450,y_axis_label='Price'
                  ,sizing_mode="stretch_width",tools='xwheel_zoom,ywheel_zoom,reset')
    src = cds(lp_df)

    seg = p.segment(source=src,x0='DATE',x1='DATE',y0='MIN_ETH_PRICE',y1='MAX_ETH_PRICE',line_width=2,line_color='black',legend_label='ETH price range')
    p.varea(source=src,x='DATE',y1='AVG_ETH_LOWER_USD',y2='AVG_ETH_HIGHER_USD',fill_alpha=0.5,fill_color='red',legend_label='LP price range')

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    tooltips = [('Date', '@DATE{%F}'),('ETH range', '@MAX_ETH_PRICE{($ 0000.00)} to @MIN_ETH_PRICE{($ 0000.00)} '),
            ('LP range','@AVG_ETH_HIGHER_USD{($ 0000.00)} to @AVG_ETH_LOWER_USD{($ 0000.00)} ')]
    hovertool = HoverTool(tooltips=tooltips,formatters={'@DATE': 'datetime'},mode='vline',renderers=[seg])
    p.add_tools(crosshair,hovertool)
    p.yaxis.formatter=NumeralTickFormatter(format="$ 0000.00")
    p.xaxis.visible=False

    #sub plot
    p2 = figure(x_axis_type='datetime',plot_height=300,y_axis_label='Percent'
                  ,sizing_mode="stretch_width",tools='xwheel_zoom,ywheel_zoom,reset')
    src2 = cds(lp_pct_df)

    p2.varea(source=src2,x='DATE',y1='VOLATILITY',y2=0,fill_alpha=0.5,fill_color='black',legend_label='ETH price range')
    p2.varea(source=src2,x='DATE',y1='PCT_RANGE_GAP',y2=0,fill_alpha=0.5,fill_color='red',legend_label='LP price range')
    seg = p2.line(source=src2,x='DATE',y='PCT_RANGE_GAP',line_width=2,line_color=None)

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    tooltips = [('Date', '@DATE{%F}'),('Price Volatility','@VOLATILITY'),('LP range','@PCT_RANGE_GAP')]
    hovertool = HoverTool(tooltips=tooltips,formatters={'@DATE': 'datetime'},mode='vline',renderers=[seg])
    p2.add_tools(crosshair,hovertool)
    p2.yaxis.formatter=NumeralTickFormatter(format="00.00")

    #layout
    l = layout([p,p2],sizing_mode="stretch_width")

    return get_div(l) 

uni_lp_plot = make_uni_lp_plot()

def get_uni_lp_plot():
    return uni_lp_plot