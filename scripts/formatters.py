from numerize import numerize

def format_money(x):
    return  numerize.numerize(x)

def format_fee_percent(x):
    return str(x)+"%"