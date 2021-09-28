from bokeh.resources import CDN
from bokeh.embed import autoload_static

def get_div(p):
    path = 'static/js/plots/bokeh_plot.js'
    js, tag = autoload_static(p, CDN, path)

    with open(path,'a') as f:
            f.write(js)

    return tag