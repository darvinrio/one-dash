from flask import Flask, render_template, url_for, request, redirect

import requests

files=[
    "static/js/plots/bokeh_plot.js"
]
for name in files:
    a_file = open(name, "w")
    a_file.truncate()
    a_file.close()


from scripts.uniswap_tvl_vol import get_uni_stat_plot
from scripts.analysis.uniswap.fees import get_uni_fee_plots
from scripts.analysis.uniswap.lp import get_uni_lp_plot
from scripts.uniswap_lp_5 import get_uni_top5_lp_plot
from scripts.analysis.uniswap.lp_react import get_lp_react_plots

import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response
            for response in responses
            if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/uni_stats')
def uni_stats():
    uni_tvl,uni_vol = get_uni_stat_plot()
    uni_top5_lp_plot,top5_lp_today = get_uni_top5_lp_plot()
    
    return render_template('uni/uniswap_stats.html',
        uni_tvl= uni_tvl,
        uni_vol=uni_vol,
        uni_top5_lp_plot=uni_top5_lp_plot,
        top5_lp_today=top5_lp_today)

@app.route('/uni_analytics')
def uni_analytics():
    uni_fee_plot, uni_volat_plot, uni_nice_plot = get_uni_fee_plots()
    uni_lp_plot = get_uni_lp_plot()
    lp_layout,liq_layout = get_lp_react_plots()

    return render_template('uni/uniswap_analysis.html',
        uni_fee_plot=uni_fee_plot, 
        uni_volat_plot=uni_volat_plot, 
        uni_nice_plot=uni_nice_plot,
        uni_lp_plot=uni_lp_plot,
        lp_layout=lp_layout,
        liq_layout=liq_layout)

# @app.route('/uni_fees')
# def uni_fees():
#     uni_fee_plot, uni_volat_plot, uni_nice_plot = get_uni_fee_plots()

#     return render_template('uni/uni_fees.html', uni_fee_plot=uni_fee_plot, uni_volat_plot=uni_volat_plot, uni_nice_plot=uni_nice_plot)


if __name__ == "__main__":
    app.run(debug=True)