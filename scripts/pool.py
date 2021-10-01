import pandas as pd
import numpy as np
import requests
import time
import copy
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
from numerize import numerize

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import NumeralTickFormatter, CustomJS,DatetimeTickFormatter
from bokeh.embed import components

from scripts.formatters import * 
from scripts.process_plot import get_div

def get_uni_pool():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/3a807bea-3e78-46ef-9b8c-2604a1bf38d1/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    df['DATE_STR'] = df['DATE'].dt.strftime("%d %b, %y")
    return df.sort_values('DATE')


def get_top_pools():
    api='https://api.flipsidecrypto.com/api/v2/queries/7587d835-dd9f-4b0b-8a15-2b9c73c462f8/data/latest'

    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())

    return response.json(),df


uni_pool_df = get_uni_pool()
uni_top_pool_json, uni_top_pool_df = get_top_pools()

def get_page(pool_address,
    start_date=dt.strptime("2021-05-05", "%Y-%m-%d"),
    end_date=date.today()):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    global uni_pool_df
    global uni_top_pool_df

    cur_pool_df = uni_pool_df[uni_pool_df['POOL_ADDRESS']==pool_address]
    cur_pool_df = cur_pool_df[(cur_pool_df['DATE']>=start_date) & (cur_pool_df['DATE']<=end_date)]

    plot_list = ['GROSS_RESERVES_TOKEN0_ADJUSTED','GROSS_RESERVES_TOKEN1_ADJUSTED','PRICE01', 'PRICE10', 'SWAP_COUNT', 'SWAP_VOL', 'TOKEN0_IN','TOKEN0_OUT', 'TOKEN1_IN', 'TOKEN1_OUT', 'TVL_USD']

    line_list = ['PRICE01', 'PRICE10']
    area_list = ['GROSS_RESERVES_TOKEN0_ADJUSTED','GROSS_RESERVES_TOKEN1_ADJUSTED','SWAP_VOL', 'TVL_USD']
    bar_list = ['SWAP_COUNT','TOKEN0_IN','TOKEN0_OUT', 'TOKEN1_IN', 'TOKEN1_OUT']

    param_list=[{
            'func':col,
            'name':'Total Value Locked',
            'format':'format_number',
            'tick_format':'(0.00 a)',
            'div':None,
            'plot':None
        } for col in plot_list
    ]
    for fun in param_list:
        if fun['func'] in ['SWAP_VOL', 'TVL_USD']:
            fun['tick_format']='($ 0.00 a)'
            fun['format']='format_money'

        if fun['func'] in line_list:
            fun['tick_format']='(0.0000 a)'
            fun['format']='no_format'


    for fun in param_list:
        col = fun['func']
        src = copy.deepcopy(cur_pool_df)
        p = figure(x_axis_type='datetime',plot_height=300,sizing_mode='stretch_width',tools='xpan,ypan,xwheel_zoom,ywheel_zoom,reset')
            
        src['OUT'] = src[col].apply(eval(fun['format']))
        
        if col in line_list :
            render = p.line(source=cds(src),x='DATE',y=col,line_width=2)
        elif col in area_list :
            render = p.line(source=cds(src),x='DATE',y=col)
            p.varea(source=cds(src),x='DATE',y1=0,y2=col,fill_alpha=0.7)
        elif col in bar_list :
            render = p.vbar(source=cds(src),x='DATE',top=col,fill_alpha=0.7,hover_alpha=1,width=timedelta(days=0.7))
        else:
            print('you missed '+ cols)
        
        callback = CustomJS(args={'p': p}, code="""
            var tooltips = document.getElementsByClassName("bk-tooltip");
            const tw = 100;
            for (var i = 0; i < tooltips.length; i++) {
                tooltips[i].style.top = '10px'; 
                tooltips[i].style.left = p.width/6 + 'px'; 
                tooltips[i].style.width = tw + 'px'; 
            } """)

        tooltips= """
            <div>
            <h6>@DATE_STR</h6>
            <h4>@OUT</h4>
            </div>
            """
        p.yaxis.formatter=NumeralTickFormatter(format=fun['tick_format'])
        p.xaxis.formatter = DatetimeTickFormatter(months="%b %y")
        
        p.yaxis.minor_tick_line_color = None
        p.yaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None
        p.xaxis.major_tick_line_color = None
        p.xaxis.axis_line_color = None
        p.yaxis.axis_line_color = None
        
        p.grid.visible=False
        p.toolbar.active_scroll='auto'
        
        hover = HoverTool(tooltips = tooltips,callback=callback, mode='vline',renderers=[render])
        crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)

        hover.show_arrow = False
        p.add_tools(hover,crosshair)
        
        fun['plot'] = p
        fun['div']=src[src['DATE']==src['DATE'].max()].reset_index(drop=True)['OUT'][0]

    for fun in param_list:
        script, div = components(fun['plot'])
        fun['plot'] = div
        fun['script'] = script

    return param_list

def get_front():
    for pool in uni_top_pool_json:
        pool['TOKEN0_ICON'] = "img/crypto-logo/"+(pool['TOKEN0_SYMBOL'].lower())+".png"
        pool['TOKEN1_ICON'] = "img/crypto-logo/"+(pool['TOKEN1_SYMBOL'].lower())+".png"
        try:
            pool['TOTAL_BAL'] = format_money(pool['TOTAL_BAL'])
        except:
            pass

    return uni_top_pool_json