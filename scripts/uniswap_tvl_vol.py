import pandas as pd
import numpy as np
import requests
from datetime import datetime as dt

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import NumeralTickFormatter, CustomJS

from bokeh.resources import CDN
from bokeh.embed import autoload_static


from scripts.formatters import format_money
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

def get_uni_tvl_plot():
    uni_tvl_df = get_uni_tvl()

    p = figure(x_axis_type='datetime',plot_height=300,x_axis_label='Time',y_axis_label='TVL_USD',sizing_mode="scale_width",tools='xwheel_zoom,ywheel_zoom,xpan,reset')
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

    hover = HoverTool(tooltips = tooltips ,formatters={'@BLOCK_HOUR': 'datetime'},callback=callback, mode='vline')

    hover.show_arrow = False
    p.outline_line_color = None
    p.axis.visible = False
    p.grid.visible = False
    p.add_tools(hover,crosshair)

    return get_div(p)


def get_uni_vol_plot():
    uni_vol_df = get_uni_vol()
    
    p = figure(x_range= uni_vol_df['DATE_STR'],x_axis_label='Time',y_axis_label='TVL_USD',plot_height=300,sizing_mode="scale_width",tools='xwheel_zoom,ywheel_zoom,xpan,reset')
    line = p.vbar(source=cds(uni_vol_df),x='DATE_STR',top='DAILY_USD_VOLUME',width=0.7, fill_color='#fc077d',line_color='#fc077d')


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
    p.outline_line_color = None
    p.axis.visible = False
    p.grid.visible = False

    return get_div(p)

uni_tvl = get_uni_tvl_plot()
uni_vol = get_uni_vol_plot() 

def get_uni_stat_plot():
    return uni_tvl,uni_vol