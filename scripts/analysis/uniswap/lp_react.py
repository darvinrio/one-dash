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


un_un_api ='https://api.flipsidecrypto.com/api/v2/queries/2c950742-5b6e-4e90-b988-042787544a86/data/latest'
st_un_api = 'https://api.flipsidecrypto.com/api/v2/queries/5145287b-0387-4a16-a04e-6f70f62d7def/data/latest'
st_st_api='https://api.flipsidecrypto.com/api/v2/queries/e8d19186-26a0-43eb-9a04-61f6e5243d2f/data/latest'

def get_lp_react(api):
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
#     df['BLK_DATE'] = pd.to_datetime(df['BLK_DATE']).dt.tz_localize(None)
    return df.sort_values(['BLK_DATE','CHANGE_THAT_DAY']).reset_index(drop=True)


def make_lp_react_plots():
    un_un_df = get_lp_react(un_un_api)
    st_un_df = get_lp_react(st_un_api)
    st_st_df = get_lp_react(st_st_api)

    out_dict = {
        "un_un_df":{
            "source":un_un_df,
            "label":'Unstable-Unstable pair',
            "lp_plot":None,
            "liq_plot":None
        },
        "st_un_df":{
            "source":st_un_df,
            "label":'Stable-Unstable pair',
            "lp_plot":None,
            "liq_plot":None
        },
        "st_st_df":{
            "source":st_st_df,
            "label":'Stable-Stable pair',
            "lp_plot":None,
            "liq_plot":None
        }
    }

    types = ['Floated_into_range','Other','Still_out_of_range','Updated_range','Reduced_exposure']
    color_dict=['#f4b731','black','#0c3694','#4bdb4b','#ff0079','magenta']

    for key in out_dict.keys():
        f = pd.pivot_table(out_dict[key]['source'],values=[
            'PCT_MIN_LIQUIDITY_ADJUSTED_AVG',
            'PCT_NUM_ACTIVE_LPS_AVG'
        ],index=['BLK_DATE'],columns=['CHANGE_THAT_DAY'],fill_value=0)
        
        for move in ['PCT_MIN_LIQUIDITY_ADJUSTED_AVG','PCT_NUM_ACTIVE_LPS_AVG']:
            d = {}
            for typ in types:
                d[typ]=list(f[move][typ])
            d['index']=list(f[move].index)
            label=list(d.keys())
            p = figure(title=out_dict[key]['label'],x_range=d['index'],plot_height=175,x_axis_type='datetime'
                        ,x_axis_label='Time'
                        ,sizing_mode="stretch_width",tools='xwheel_zoom,reset')

            crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
            tooltips = [('Date', '@index'),('Action', '$name'),
                    ('percent','@$name{00.00%}')]
            hovertool = HoverTool(tooltips=tooltips,formatters={'@DATE': 'datetime'})
            p.add_tools(crosshair,hovertool)
            p.yaxis.formatter=NumeralTickFormatter(format="00.00%")
            # p.xaxis.formatter=DatetimeTickFormatter()

            p.vbar_stack(label, x='index',color=color_dict,source=d)
            p.xaxis.visible=False
            p.grid.visible=False
            if move == 'PCT_MIN_LIQUIDITY_ADJUSTED_AVG':
                out_dict[key]['liq_plot'] = p
            else:
                out_dict[key]['lp_plot'] = p
            
    lp_plots = []
    liq_plots = []
    for key in out_dict.keys():
        lp_plots.append(out_dict[key]['lp_plot'])
        liq_plots.append(out_dict[key]['liq_plot'])

    lp_layout = layout(lp_plots,sizing_mode="stretch_width")
    liq_layout = layout(liq_plots,sizing_mode="stretch_width")

    return get_div(lp_layout),get_div(liq_layout)

lp_layout,liq_layout = make_lp_react_plots() 

def get_lp_react_plots():
    return lp_layout,liq_layout 