import pandas as pd
import numpy as np 
import requests
from datetime import datetime as dt
import json

from bokeh.models import ColumnDataSource as cds
from bokeh.models import HoverTool,CrosshairTool
from bokeh.models import NumeralTickFormatter
from bokeh.models import Range1d, Span
from bokeh.embed import components
from bokeh.plotting import figure

from io import StringIO
import base64

def truncate_small_amt(x):
    return round(x,-2)

def truncate_med_amt(x):
    return round(x,-3)

def truncate_big_amt(x):
    return round(x,-4)

def truncate_whale_amt(x):
    return round(x,-5)

def truncate_low_slip(x):
    return round(x)

def truncate_med_slip(x):
    return round(x,1)

def truncate_high_slip(x):
    return round(x,2)

def get_swaps():
    api = 'https://api.flipsidecrypto.com/api/v2/queries/becfb31a-2e89-4d9c-89ab-ca95a60c2f7d/data/latest'
    
    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    return df 

def get_overall():
    api='https://api.flipsidecrypto.com/api/v2/queries/fa6bf149-b451-4f10-a098-94727f454e7b/data/latest'

    response = requests.get(api)
    print('Retrieved data')
    df = pd.DataFrame(response.json())
    return df 

swap_df = get_swaps()
overall_df = get_overall()

def get_slip_hist(pool_address):
    swap_pool_df = swap_df[swap_df['POOL_ADDRESS']==pool_address].reset_index(drop=True)
    # swap_pool_df=swap_pool_df[swap_pool_df['SLIPPAGE']>0]
    slips = swap_pool_df['SLIPPAGE']
    slips = slips[slips>0]
    max_slip = slips.max()
    min_slip = slips.min()
    range_slip = max_slip - min_slip
    
    arr_slip, edges = np.histogram(slips, bins=150)
    slip_df = pd.DataFrame({
        'txs':arr_slip,
        'left': edges[:-1], 
        'right': edges[1:],
        'label_left': edges[:-1], 
        'label_right': edges[1:]
    })
    slip_df['props'] = slip_df['txs']/slip_df['txs'].sum()

    p = figure(plot_height=300, x_axis_label = 'Slippage', y_axis_label = 'Percent of total swaps',sizing_mode="stretch_width")

    p.quad(source=cds(slip_df),bottom=0, top='props', left='left', right='right',fill_color= '#22316c',fill_alpha=0.7,line_color=None,hover_fill_color='#22316c',hover_fill_alpha=1)

    crosshair = CrosshairTool(dimensions='height',line_alpha=0.5)
    hover = HoverTool(tooltips = [('Slippage ', '@label_left{0.000%} to @label_right{0.000%}'),('Percent of swaps', '@props{0.00%}')],mode='vline')
    p.add_tools(hover,crosshair)
            
    p.xaxis.formatter=NumeralTickFormatter(format="0.000%")
    p.yaxis.formatter=NumeralTickFormatter(format="0.00%")

    p.yaxis.minor_tick_line_color = None
    p.yaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.axis_line_color = None
    p.yaxis.axis_line_color = None
    p.grid.visible=False

    script,div = components(p)

    out_dict={
        'script': script,
        'div': div,
        'all75': "{:.2%}".format(swap_pool_df['SLIPPAGE'].describe()['75%']),
        'mean': "{:.2%}".format(swap_pool_df['SLIPPAGE'].describe()['mean'])
    }

    return out_dict

def get_slip_heat(pool_address):
    swap_pool_df = swap_df[swap_df['POOL_ADDRESS']==pool_address].reset_index(drop=True)
    swap_pool_df = swap_pool_df[swap_pool_df['SLIPPAGE']>0]

    import seaborn as sns; sns.set_theme()
    sns.set(rc={'figure.figsize':(8,8)})

    amt = (swap_pool_df['SWAP_OUT_USD']+swap_pool_df['SWAP_OUT_USD'])/2
    amt.name='SWAP AMOUNT'

    slip = (swap_pool_df['SLIPPAGE']*100)
    slip = slip[slip>0].apply(truncate_low_slip)
    if len(slip.unique()) <10:
        slip = (swap_pool_df['SLIPPAGE']*100)
        slip = slip[slip>0].apply(truncate_high_slip)
        if len(slip.unique()) >100:
            slip = (swap_pool_df['SLIPPAGE']*100)
            slip = slip[slip>0].apply(truncate_med_slip)

    amt_small = amt[amt<1000].apply(truncate_small_amt)
    amt_med = amt[(amt>1000) & (amt<10000)].apply(truncate_med_amt)
    amt_big = amt[(amt>10000) & (amt<100000)].apply(truncate_big_amt)
    amt_whale = amt[amt>100000].apply(truncate_whale_amt)

    heat_data_small = pd.crosstab(slip,amt_small)
    heat_data_med = pd.crosstab(slip,amt_med)
    heat_data_big = pd.crosstab(slip,amt_big)
    heat_data_whale = pd.crosstab(slip,amt_whale)

    plot_small = sns.heatmap(heat_data_small,cmap="YlGnBu")
    plot_small.figure.savefig('static/img/heatmaps/small.png',bbox_inches = 'tight')
    plot_small.figure.clf()

    plot_med = sns.heatmap(heat_data_med,cmap="YlGnBu")
    plot_med.figure.savefig('static/img/heatmaps/med.png',bbox_inches = 'tight')
    plot_med.figure.clf()
    
    plot_big = sns.heatmap(heat_data_big,cmap="YlGnBu")
    plot_big.figure.savefig('static/img/heatmaps/big.png',bbox_inches = 'tight')
    plot_big.figure.clf()
    
    plot_whale = sns.heatmap(heat_data_whale,cmap="YlGnBu")
    plot_whale.figure.savefig('static/img/heatmaps/whale.png',bbox_inches = 'tight')
    plot_whale.figure.clf()

def get_overall_dict(pool_address):

    t_df = overall_df[overall_df['POOL_ADDRESS']==pool_address]

    result = t_df.to_json(orient="records")
    t_df = json.loads(result)[0]

    param_dict={
        "swaps":t_df['NO_SWAPS'],
        'token0_traded':t_df['TOKEN0_TRADED'],
        'token1_traded':t_df['TOKEN1_TRADED'],
        'total_vol':t_df['TOTAL_SWAP_VOL']
    }

    return param_dict
