import pandas as pd
import numpy as np
import requests
import time
import copy
import json
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
from numerize import numerize

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool, Range1d
from bokeh.models import NumeralTickFormatter, CustomJS,DatetimeTickFormatter
from bokeh.embed import components

from scripts.formatters import * 
from scripts.process_plot import get_div


token_color_dict={
    "uni":"#fc077d",
    'weth':'#454a75',
    'wbtc':'#ef9242',
    'usdt':'#259c77',
    'usdc':'#256fc0',
    'dai':'#f4b731',
    'frax':'#000000',
    'seth2':'#95dd8c'
}

def get_uni_pool():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/3a807bea-3e78-46ef-9b8c-2604a1bf38d1/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    df['DATE_STR'] = df['DATE'].dt.strftime("%d %b, %y")
    return df.sort_values('DATE')

def get_lp_react():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/c7b5ca8c-31a8-4764-82ec-88e593949d14/data/latest'
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['BLK_DATE'] = pd.to_datetime(df['BLK_DATE']).dt.tz_localize(None)
    return df.sort_values(['BLK_DATE','CHANGE_THAT_DAY']).reset_index(drop=True)

def get_top_pools():
    api='https://api.flipsidecrypto.com/api/v2/queries/7587d835-dd9f-4b0b-8a15-2b9c73c462f8/data/latest'

    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())

    return response.json(),df

def get_uni_range():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/a863e3be-4615-48c7-986d-77fc6e7dd1e6/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    df['DATE_STR'] = df['DATE'].dt.strftime("%d %b, %y")
    return df.sort_values('DATE')

uni_pool_df = get_uni_pool()
uni_top_pool_json, uni_top_pool_df = get_top_pools()
range_df = get_uni_range()
react_df = get_lp_react()


def get_page_stuff(pool_address):
    pool_df = uni_top_pool_df[uni_top_pool_df['POOL_ADDRESS']==pool_address]
    
    result = pool_df.to_json(orient="records")
    pool_df = json.loads(result)[0]
    
    param_dict={
        "pool_name":pool_df['POOL_NAME'],
        "token0":pool_df['TOKEN0_SYMBOL'],
        "token1":pool_df['TOKEN1_SYMBOL'],
        "token0_icon":"img/crypto-logo/"+(pool_df['TOKEN0_SYMBOL'].lower())+".png",
        "token1_icon":"img/crypto-logo/"+(pool_df['TOKEN1_SYMBOL'].lower())+".png",
        'token0_color':token_color_dict[pool_df['TOKEN0_SYMBOL'].lower()],
        'token1_color':token_color_dict[pool_df['TOKEN1_SYMBOL'].lower()]
    }
    
    return param_dict


def get_page(pool_address, start_date=dt.strptime("2021-05-05", "%Y-%m-%d"), end_date=date.today()):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    param_dict = get_page_stuff(pool_address)

    global uni_pool_df
    global uni_top_pool_df

    cur_pool_df = uni_pool_df[uni_pool_df['POOL_ADDRESS']==pool_address]
    cur_pool_df = cur_pool_df[(cur_pool_df['DATE']>=start_date) & (cur_pool_df['DATE']<=end_date)]

    plot_list = ['GROSS_RESERVES_TOKEN0_ADJUSTED','GROSS_RESERVES_TOKEN1_ADJUSTED','PRICE01', 'PRICE10', 'SWAP_COUNT', 'SWAP_VOL', 'TOKEN0_IN','TOKEN0_OUT', 'TOKEN1_IN', 'TOKEN1_OUT', 'TVL_USD']

    line_list = ['PRICE01', 'PRICE10']
    area_list = ['GROSS_RESERVES_TOKEN0_ADJUSTED','GROSS_RESERVES_TOKEN1_ADJUSTED','SWAP_VOL', 'TVL_USD']
    bar_list = ['SWAP_COUNT','TOKEN0_IN','TOKEN0_OUT', 'TOKEN1_IN', 'TOKEN1_OUT']

    token0_list = ['GROSS_RESERVES_TOKEN0_ADJUSTED','PRICE01','TOKEN0_IN','TOKEN0_OUT']
    token1_list = ['GROSS_RESERVES_TOKEN1_ADJUSTED','PRICE10','TOKEN1_IN','TOKEN1_OUT']

    param_list=[{
            'func':col,
            'name':'Total Value Locked',
            'format':'format_number',
            'tick_format':'(0.00 a)',
            'div':None,
            'plot':None,
            'color':"#101419"
        } for col in plot_list
    ]
    for fun in param_list:
        if fun['func'] in ['SWAP_VOL', 'TVL_USD']:
            fun['tick_format']='($ 0.00 a)'
            fun['format']='format_money'

        if fun['func'] in line_list:
            fun['tick_format']='(0.0000 a)'
            fun['format']='no_format'

        if fun['func'] in token0_list:
            fun['color'] = param_dict['token0_color']

        if fun['func'] in token1_list:
            fun['color'] = param_dict['token1_color']


    for fun in param_list:
        col = fun['func']
        src = copy.deepcopy(cur_pool_df)
        p = figure(x_axis_type='datetime',plot_height=300,sizing_mode='stretch_width',tools='xpan,ypan,xwheel_zoom,ywheel_zoom,reset')
            
        src['OUT'] = src[col].apply(eval(fun['format']))
        
        if col in line_list :
            render = p.line(source=cds(src), x='DATE', y=col, color=fun['color'], line_width=2)
        elif col in area_list :
            render = p.line(source=cds(src), x='DATE', y=col, color=fun['color'])
            p.varea(source=cds(src), x='DATE', y1=0, y2=col, color=fun['color'], fill_alpha=0.7)
        elif col in bar_list :
            render = p.vbar(source=cds(src), x='DATE', top=col, color=fun['color'], fill_alpha=0.7, hover_alpha=1, width=timedelta(days=0.7))
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


def get_lp_range(pool_address, start_date=dt.strptime("2021-05-05", "%Y-%m-%d"), end_date=date.today()):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    param_dict = get_page_stuff(pool_address)

    lp_df = range_df[range_df['POOL_ADDRESS']==pool_address].reset_index(drop=True)
    lp_df = lp_df[(lp_df['DATE']>=start_date) & (lp_df['DATE']<=end_date)]
    major = lp_df['TOKEN0_SYMBOL'].value_counts().sort_values(ascending=False).index[0]
    lp_df = lp_df[lp_df['TOKEN0_SYMBOL']==major]

    color1 = token_color_dict[(lp_df['TOKEN0_SYMBOL'].unique()[0]).lower()] 
    color0 = token_color_dict[(lp_df['TOKEN1_SYMBOL'].unique()[0]).lower()] 

    p = figure(plot_height=300,x_axis_type='datetime',y_axis_label='Price'
                  ,sizing_mode="stretch_width",tools='xpan,ypan,xwheel_zoom,ywheel_zoom,reset')

    src = cds(lp_df)

    aread = pd.concat([
        lp_df.sort_values('DATE')['AVG_ETH_LOWER_USD'],
        lp_df.sort_values('DATE',ascending=False)['AVG_ETH_HIGHER_USD']
    ])
    datad = pd.concat([
        lp_df.sort_values('DATE')['DATE'],
        lp_df.sort_values('DATE',ascending=False)['DATE']
    ])

    seg = p.segment(source=src,x0='DATE',x1='DATE',y0='MIN_ETH_PRICE',y1='MAX_ETH_PRICE',line_width=2,line_color=color0,legend_label=(lp_df['TOKEN1_SYMBOL'].unique()[0])+' price range')
    p.varea(source=src,x='DATE',y1='AVG_ETH_LOWER_USD',y2='AVG_ETH_HIGHER_USD',fill_alpha=0.5,fill_color=color1,legend_label=(lp_df['TOKEN0_SYMBOL'].unique()[0])+' liquidity range')

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    tooltips = [('Date', '@DATE{%F}'),((lp_df['TOKEN1_SYMBOL'].unique()[0])+' price range', '@MAX_ETH_PRICE{(0.0000)} to @MIN_ETH_PRICE{(0.0000)} '),
            ((lp_df['TOKEN0_SYMBOL'].unique()[0])+' liquidity range','@AVG_ETH_HIGHER_USD{(0.0000)} to @AVG_ETH_LOWER_USD{(0.0000)} ')]
    hovertool = HoverTool(tooltips=tooltips,formatters={'@DATE': 'datetime'},mode='vline',renderers=[seg])
    p.add_tools(crosshair,hovertool)

    p.yaxis.formatter=NumeralTickFormatter(format="0.0000")
    p.xaxis.formatter = DatetimeTickFormatter(months="%b %y")
            
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None
    p.grid.visible=False

    max_price = lp_df['MAX_ETH_PRICE'].max()
    min_price = lp_df['MIN_ETH_PRICE'].min()
    price_diff = max_price-min_price

    p.y_range = Range1d(0 if (min_price-0.5*price_diff)<0 else (min_price-0.5*price_diff), max_price+0.5*price_diff)

    lp_range_script, lp_range_div = components(p)
    return lp_range_script, lp_range_div


def get_lp_react(pool_address, start_date=dt.strptime("2021-05-05", "%Y-%m-%d"), end_date=date.today()):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    types = ['Floated_into_range','Other','Still_out_of_range','Updated_range','Reduced_exposure']
    color_dict=['#f4b731','black','#0c3694','#4bdb4b','#ff0079','magenta']
    param_dict = get_page_stuff(pool_address)
    pool_name = param_dict['pool_name']

    source_df = react_df[react_df['POOL_NAME'] == pool_name ]
    source_df = source_df[(source_df['BLK_DATE']>=start_date) & (source_df['BLK_DATE']<=end_date)]


    f = pd.pivot_table(source_df,values=[
        'PCT_MIN_LIQUIDITY_ADJUSTED_AVG',
        'PCT_NUM_ACTIVE_LPS_AVG'
    ],index=['BLK_DATE'],columns=['CHANGE_THAT_DAY'],fill_value=0)


    out_dict=[
        {
            'title':'Liqudity activity',
            'div':None,
            'script':None
        },
        {
            'title':'Liquidity Provider Reaction',
            'div':None,
            'script':None
        }
    ]
    
    for move in ['PCT_MIN_LIQUIDITY_ADJUSTED_AVG','PCT_NUM_ACTIVE_LPS_AVG']:
        d = {}
        for typ in types:
            try:
                d[typ]=list(f[move][typ])
            except:
                d[typ]=[0]*len(list(f[move].index))
        d['index']=list(f[move].index)
        label=list(d.keys())
        p = figure(plot_height=300,x_axis_type='datetime'
                    ,x_axis_label='Time'
                    ,sizing_mode="stretch_width",tools='xpan,ypan,ywheel_zoom,xwheel_zoom,reset')

        crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
        tooltips = [('Date', '@index'),('Action', '$name'),
                ('percent','@$name{00.00%}')]
        hovertool = HoverTool(tooltips=tooltips,formatters={'@index': 'datetime'})
        p.add_tools(crosshair,hovertool)
        p.yaxis.formatter=NumeralTickFormatter(format="00.00%")
        p.xaxis.formatter=DatetimeTickFormatter()

        p.vbar_stack(label, x='index',color=color_dict,source=d,width=timedelta(days=0.7),fill_alpha=0.7,hover_alpha=1)
        p.y_range = Range1d(0,1)
        
        p.yaxis.minor_tick_line_color = None
        p.yaxis.major_tick_line_color = None
        p.xaxis.minor_tick_line_color = None
        p.xaxis.major_tick_line_color = None
        p.xaxis.axis_line_color = None
        p.yaxis.axis_line_color = None
        p.background_fill_alpha = 0
        p.grid.visible=False

        n=1
        if move == 'PCT_MIN_LIQUIDITY_ADJUSTED_AVG':
            n=0

        out_dict[n]['script'], out_dict[n]['div'] = components(p) 

    return out_dict


def get_front():
    for pool in uni_top_pool_json:
        pool['TOKEN0_ICON'] = "img/crypto-logo/"+(pool['TOKEN0_SYMBOL'].lower())+".png"
        pool['TOKEN1_ICON'] = "img/crypto-logo/"+(pool['TOKEN1_SYMBOL'].lower())+".png"
        try:
            pool['TOTAL_BAL'] = format_money(pool['TOTAL_BAL'])
        except:
            pass

    return uni_top_pool_json