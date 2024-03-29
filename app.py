from flask import Flask, render_template, url_for, request, redirect

import requests
from datetime import datetime,date,timedelta

files=[
    "static/js/plots/bokeh_plot.js"
]
for name in files:
    a_file = open(name, "w")
    a_file.truncate()
    a_file.close()

# import socket
# old_getaddrinfo = socket.getaddrinfo
# def new_getaddrinfo(*args, **kwargs):
#     responses = old_getaddrinfo(*args, **kwargs)
#     return [response
#             for response in responses
#             if response[0] == socket.AF_INET]
# socket.getaddrinfo = new_getaddrinfo

from scripts.uniswap_tvl_vol import get_uni_stat_plot
from scripts.uniswap.fees import get_uni_fee_plots
from scripts.uniswap.lp import get_uni_lp_plot
from scripts.uniswap.lp_react import get_lp_react_plots

from scripts.swap import get_slip_hist,get_slip_heat,get_overall_dict
from scripts.pool import get_page,get_front,get_page_stuff,get_lp_range, get_lp_react, get_fee_stuff

# from scripts.test2 import get_comps

app = Flask(__name__)

@app.route('/')
def home():
    # return render_template('home.html')
    
# @app.route('/uni_stats')
# def uni_stats():

    uni_tvl,uni_vol,front_swap_stats = get_uni_stat_plot()

    uni_top_pool_json = get_front()

    uni_fee_plot, uni_volat_plot, uni_nice_plot = get_uni_fee_plots()
    uni_lp_plot = get_uni_lp_plot()
    lp_layout,liq_layout = get_lp_react_plots()
    
    return render_template('uni/uniswap_stats.html',
        uni_tvl= uni_tvl,
        uni_vol=uni_vol,
        front_swap_stats=front_swap_stats,
        uni_top_pool_json=uni_top_pool_json,
        uni_fee_plot=uni_fee_plot, 
        uni_volat_plot=uni_volat_plot, 
        uni_nice_plot=uni_nice_plot,
        uni_lp_plot=uni_lp_plot,
        lp_layout=lp_layout,
        liq_layout=liq_layout)

@app.route('/uni_pool/<pool_address>',methods=['POST','GET'])
def pool(pool_address):

    today = date.today()
    end_date = today.strftime("%d %b, %y")
    start_date = (today + timedelta(-30) ).strftime("%d %b, %y")

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_date = datetime.strptime(start_date, "%d %b, %Y")
        try: 
            end_date = datetime.strptime(end_date, "%d %b, %Y")
        except:
            end_date = today
        
        end_date = end_date.strftime("%d %b, %y")
        start_date = start_date.strftime("%d %b, %y")

    param_list = get_page(pool_address,start_date=start_date,end_date=end_date)
    lp_range_script, lp_range_div = get_lp_range(pool_address)    
    param_dict = get_page_stuff(pool_address) 
    react_dict = get_lp_react(pool_address,start_date=start_date,end_date=end_date)
    slip_dict = get_slip_hist(pool_address)
    get_slip_heat(pool_address)
    overall_swap_dict = get_overall_dict(pool_address)
    fee_dict = get_fee_stuff(pool_address,start_date=start_date,end_date=end_date)

    return render_template('uni/pool.html',
            lp_range_script=lp_range_script, 
            lp_range_div=lp_range_div,
            end_date=end_date,
            start_date=start_date,
            pool_address = pool_address, 
            param_list=param_list,
            param_dict=param_dict,
            react_dict=react_dict,
            slip_dict=slip_dict,
            overall_swap_dict=overall_swap_dict,
            fee_dict=fee_dict)

@app.route('/test')
def test():
    script,div = get_comps()
    return render_template('test.html',script=script,div=div)

@app.route('/docs')
def docs():
    return render_template('uni/doc.html')

@app.errorhandler(404)
def error404(e):
    render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)