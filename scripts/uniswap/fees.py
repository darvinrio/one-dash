import pandas as pd
import numpy as np
import requests
import time
import copy
from datetime import datetime as dt

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import NumeralTickFormatter, DatetimeTickFormatter, CustomJS
from bokeh.models import Range1d

from bokeh.resources import CDN
from bokeh.embed import autoload_static

from scripts.formatters import format_fee_percent
from scripts.process_plot import get_div


fee_api = 'https://api.flipsidecrypto.com/api/v2/queries/0d08c482-7529-4f8b-a775-659939ff43ed/data/latest'
uni_volatile_fee_api = 'https://api.flipsidecrypto.com/api/v2/queries/86fa4d41-43bd-4be5-ae99-83877f0ed603/data/latest'
uni_nice_fee_api='https://api.flipsidecrypto.com/api/v2/queries/5f387a95-b848-43ba-8b90-b0b8de6d57ea/data/latest'

fee_color_dict={
    "0.05%":'#256fc0',
    "0.3%":'#fc077d',
    "1.0%":'#4bdb4b',
    "0.01%":'black'
    
}

def get_uni_fee(api):
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    df['DATE'] = pd.to_datetime(df['DATE']).dt.tz_localize(None)
    df['FEE_PERCENT']=df['FEE_PERCENT'].apply(format_fee_percent)
    return df

def get_uni_fee_plot():
    uni_fee_df = get_uni_fee(fee_api).sort_values(['DATE'])

    p = figure(x_axis_type='datetime',y_axis_type='log',plot_height=200,y_axis_label='Fee Generated'
                  ,sizing_mode="scale_width",tools='xwheel_zoom,ywheel_zoom,reset')

    for fee in list(uni_fee_df['FEE_PERCENT'].unique()):
        data = uni_fee_df[uni_fee_df['FEE_PERCENT']==fee]
        line = p.line(source=cds(data),x='DATE',y='FEES_COLLECTED',
                    legend_label=fee, color=fee_color_dict[fee],line_width=2)

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    hover = HoverTool(tooltips = [('Date', '@DATE{%F}'),
                                ('Fees Accumulated', '@FEES_COLLECTED{($ 0.00 a)}'),
                                ],
                        formatters={'@DATE': 'datetime'},point_policy="follow_mouse")

    hover.show_arrow = False
    p.add_tools(hover,crosshair)
    p.legend.click_policy="hide"
    p.outline_line_color = None
    # p.grid.visible = False
    p.y_range = Range1d((10**4),10**8)
    p.yaxis.formatter=NumeralTickFormatter(format="$ 0.00 a")

    p.xaxis.formatter = DatetimeTickFormatter(days="%b %d",months="%b %y")
    
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None

    return get_div(p)

def get_uni_volat_plot():
    uni_volatile_fee_df = get_uni_fee(uni_volatile_fee_api).sort_values(['DATE'])

    p = figure(x_axis_type='datetime',y_axis_type='log',plot_height=300,y_axis_label='Median APR'
                  ,sizing_mode="scale_width",tools='xwheel_zoom,ywheel_zoom,reset')

    for fee in list(uni_volatile_fee_df['FEE_PERCENT'].unique()):
        data = uni_volatile_fee_df[uni_volatile_fee_df['FEE_PERCENT']==fee]
        line = p.line(source=cds(data),x='DATE',y='MED_APR',
                    legend_label=fee, color=fee_color_dict[fee],line_width=2)

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    hover = HoverTool(tooltips = [('Date', '@DATE{%F}'),
                                ('Median APR', '@MED_APR %'),
                                ],
                        formatters={'@DATE': 'datetime'},point_policy="follow_mouse")

    hover.show_arrow = False
    p.add_tools(hover,crosshair)
    p.legend.click_policy="hide"
    p.outline_line_color = None
    # p.grid.visible = False
    p.legend.location = "bottom_left"

    p.xaxis.formatter = DatetimeTickFormatter(days="%b %d",months="%b %y")
    
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None

    return get_div(p)

def get_uni_nice_plot():
    uni_nice_fee_df = get_uni_fee(uni_nice_fee_api).sort_values(['DATE'])

    p = figure(x_axis_type='datetime',y_axis_type='log',plot_height=300,y_axis_label='Median APR'
                  ,sizing_mode="scale_width",tools='xwheel_zoom,ywheel_zoom,reset')

    for fee in list(uni_nice_fee_df['FEE_PERCENT'].unique()):
        data = uni_nice_fee_df[uni_nice_fee_df['FEE_PERCENT']==fee]
        line = p.line(source=cds(data),x='DATE',y='MED_APR',
                    legend_label=fee, color=fee_color_dict[fee],line_width=2)

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    hover = HoverTool(tooltips = [('Date', '@DATE{%F}'),
                                ('Median APR', '@MED_APR %'),
                                ],
                        formatters={'@DATE': 'datetime'},point_policy="follow_mouse")

    hover.show_arrow = False
    p.add_tools(hover,crosshair)
    p.legend.click_policy="hide"
    p.outline_line_color = None
    # p.grid.visible = False
    p.legend.location = "bottom_left"

    p.xaxis.formatter = DatetimeTickFormatter(days="%b %d",months="%b %y")
    
    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None

    return get_div(p)

uni_fee_plot = get_uni_fee_plot()
uni_volat_plot = get_uni_volat_plot()
uni_nice_plot = get_uni_nice_plot()

def get_uni_fee_plots():
    return uni_fee_plot, uni_volat_plot, uni_nice_plot
