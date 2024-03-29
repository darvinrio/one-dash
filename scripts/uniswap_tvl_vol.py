import pandas as pd
import numpy as np
import requests
from datetime import datetime as dt
from datetime import timedelta


from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import NumeralTickFormatter, DatetimeTickFormatter, CustomJS

from bokeh.resources import CDN
from bokeh.embed import autoload_static


from scripts.formatters import format_money,format_number
from scripts.process_plot import get_div


def get_uni_tvl():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/5af7a9cb-8df7-42db-9691-ba5574f9401b/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE_STR'] = df['BLOCK_HOUR']
    df['BLOCK_HOUR'] = pd.to_datetime(df['BLOCK_HOUR']).dt.tz_localize(None)
    df['DATE_STR'] = df['BLOCK_HOUR'].dt.strftime('%b %d, %Y')
    df['TOTAL_LIQUIDITY_STR'] =df['TOTAL_LIQUIDITY_USD'].apply(format_money)
    return df

def get_uni_vol():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/973cf5de-6fed-4734-b021-4e4e7481b234/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df = df.sort_values('DATE').reset_index(drop=True)
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    df['DATE_STR'] = df['DATE'].dt.strftime('%b %d, %Y')
    df['DAILY_VOLUME_STR'] =df['DAILY_USD_VOLUME'].apply(format_money)

    return df

def get_swap_stats():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/96b859a6-8afd-4a54-a2ac-1bbb1d4a7f91/data/latest'
    
    response = requests.get(api)
    out_dict = response.json()[0]

    for key in out_dict.keys():
        if key in ['OVERALL_SWAP_VOL','SWAP_VOL_TODAY']:
            out_dict[key] = format_money(out_dict[key])
        else :
            out_dict[key] = format_number(out_dict[key])

    return out_dict


def get_uni_tvl_plot():
    uni_tvl_df = get_uni_tvl()

    tvl_today = uni_tvl_df[uni_tvl_df['BLOCK_HOUR']==uni_tvl_df['BLOCK_HOUR'].max()].reset_index(drop=True)['TOTAL_LIQUIDITY_STR'][0]

    p = figure(x_axis_type='datetime',plot_height=300,sizing_mode="stretch_width",tools='xwheel_zoom,ywheel_zoom,xpan,reset')
    p.varea(source=cds(uni_tvl_df),x='BLOCK_HOUR',y2='TOTAL_LIQUIDITY_USD',y1=0 ,fill_color='#fc077d',fill_alpha=0.7)

    line = p.line(source=cds(uni_tvl_df),x='BLOCK_HOUR',y='TOTAL_LIQUIDITY_USD',line_color='#fc077d',line_width=2)


    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)


    callback = CustomJS(args={'p': p}, code="""
        var tooltips = document.getElementsByClassName("bk-tooltip");
        const tw = 100;
        for (var i = 0; i < tooltips.length; i++) {
            tooltips[i].style.top = '10px'; 
            tooltips[i].style.left = p.width/8 - tw/2 + 'px'; 
            tooltips[i].style.width = tw + 'px'; 
        } """)

    tooltips = """
        <div>
        <h3> @TOTAL_LIQUIDITY_STR </h3>
        <h7> @DATE_STR </h7>
        </div>
        """

    hover = HoverTool(tooltips = tooltips ,formatters={'@BLOCK_HOUR': 'datetime'},callback=callback, mode='vline',renderers=[line])

    hover.show_arrow = False
    p.yaxis.visible = False
    p.grid.visible = False
    p.add_tools(hover,crosshair)

    p.xaxis.formatter = DatetimeTickFormatter(days="%b %d",months="%b %y")
    
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None
    p.yaxis.visible = False
    p.grid.visible = False

    return get_div(p),tvl_today


def get_uni_vol_plot():
    uni_vol_df = get_uni_vol()
    
    p = figure(x_axis_type='datetime',plot_height=300,sizing_mode="stretch_width",tools='xwheel_zoom,ywheel_zoom,xpan,reset')
    line = p.vbar(source=cds(uni_vol_df),x='DATE',top='DAILY_USD_VOLUME',width=timedelta(days=0.7), fill_color='#fc077d',line_color='#fc077d')


    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)


    callback = CustomJS(args={'p': p}, code="""
        var tooltips = document.getElementsByClassName("bk-tooltip");
        const tw = 100;
        for (var i = 0; i < tooltips.length; i++) {
            tooltips[i].style.top = '10px'; 
            tooltips[i].style.left = p.width/8 - tw/2 + 'px'; 
            tooltips[i].style.width = tw + 'px'; 
        } """)

    tooltips = """
        <div style="background: #ffffff border=0px">
        <h3>@DAILY_VOLUME_STR</h3>
        <h7>@DATE_STR </h7>
        </div>
        """


    hover = HoverTool(tooltips = tooltips ,callback=callback, mode='vline')

    hover.show_arrow = False
    hover.line_policy="next"
    p.add_tools(hover,crosshair)
    p.xaxis.formatter = DatetimeTickFormatter(days="%b %d",months="%b %y")
    
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None
    p.yaxis.visible = False
    p.grid.visible = False

    return get_div(p)

uni_tvl,tvl_today = get_uni_tvl_plot()
uni_vol = get_uni_vol_plot() 
front_swap_stats = get_swap_stats()
front_swap_stats['TVL_TODAY'] = tvl_today

def get_uni_stat_plot():
    return uni_tvl,uni_vol,front_swap_stats