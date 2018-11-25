################
# Author: Santiago Erroz Ferrer
# To run the app from the terminal in the folder Interactive_plots_with_python_bokeh:
# bokeh serve my_app2 --show
################


from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
import glob
from bokeh.layouts import row, column
from bokeh.models.widgets import PreText, Select
import pandas as pd
from bokeh.transform import dodge, factor_cmap


def update(attr, old, new): # This function updates the plot once we select a new value in the dropdown menu
    new_src = make_dataset(ticker1.value,ticker2.value)   # the source data is updated
    src.data.update(new_src.data)
    curdoc().clear()   # the old plot is erased
    page_logo = make_plot(new_src)
    layout = column(ticker1,ticker2, page_logo)
    curdoc().add_root(layout)  # the new plot with the new options is created

def make_plot(source):   # This function makes a bar plot with the corresponding datadata

    names= source.data['name'].tolist()   # different exchange products
    amounts = source.data['amount'].tolist()   # the amounts of the different exchange products

    cmap = {"kg"         : "#a6cee3",   # a dictionary with different colors for each unit
        "kWh" : "#1f78b4",
        "m3"                : "#d93b43",
        "unit"              : "#999d9a",
        "MJ"            : "#e08d49",
        "m*year"            : "#eaeaea",
        "metric ton*km"             : "#f1d4Af"}
    p = figure(x_range=names,y_range=(0, 1.4*max(amounts)),plot_height=500, title="Exchange products") # empty figure
    p.vbar(x='name', top='amount',source=source, width=0.9,    # histogram per exchange type
        color=factor_cmap('unit', palette=list(cmap.values()), factors=list(cmap.keys())), legend="unit")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 45   # rotated x labels to read the exchange product
    p.legend.orientation = "horizontal"   # we plot the legend (the units)
    p.legend.location ="top_center"
    p.yaxis.axis_label = "Amount"

    return p

def make_dataset(name1,name2):   # this function prepares the data to be plotted according to the selected options in the dropdown menus
    filename = './my_app2/static/'+name1.replace(" ","_")+'.csv'  
    df = pd.read_csv(filename,na_values=0).drop(columns=['volume'])
    if name2=='produced materials':
        df_exchange = df.loc[(df['group_num'] == 2) & (df['group'] == 'output') & (df['exchange'] == 'intermediate')] 
        df_exchange=df_exchange.groupby(['name','unit']).agg({"amount": "sum"}).sort_values(by=['unit','amount'], axis=0, ascending=False).reset_index()
    elif name2=='raw materials':
        df_exchange = df.loc[(df['group_num'] == 5) & (df['group'] == 'input') & (df['exchange'] == 'intermediate')] 
        df_exchange=df_exchange.groupby(['name','unit']).agg({"amount": "sum"}).sort_values(by=['unit','amount'], axis=0, ascending=False).reset_index()
    elif name2=='released gases':
        df_exchange= df.loc[(df['group'] == 'input') & (df['exchange'] == 'elementary')] 
        df_exchange=df_exchange.groupby(['name','unit']).agg({"amount": "sum"}).sort_values(by=['unit','amount'], axis=0, ascending=False).reset_index()
    elif name2=='input materials from environment':
        df_exchange= df.loc[(df['group'] == 'output') & (df['exchange'] == 'elementary')] 
        df_exchange=df_exchange.groupby(['name','unit']).agg({"amount": "sum"}).sort_values(by=['unit','amount'], axis=0, ascending=False).reset_index()
    
    return ColumnDataSource(df_exchange)


# Now we start with the main part

paths = glob.glob('./my_app2/static/*csv')    # First we read the paths of the tables

data = list()   # We create a list with the tables
for file in paths:
    name=file.split('./my_app2/static/')[1].split('.csv')[0]
    data.append(name)
DEFAULT_TICKERS = data

exchanges = ['produced materials','raw materials','released gases','input materials from environment']

ticker1 = Select(title="Activity",value=data[0], options= DEFAULT_TICKERS) # dropdown select with the chemical reactions
ticker1.on_change('value', update)
ticker2 = Select(title="Type of exchange",value=exchanges[0], options= exchanges) # dropdown select with the exchange type
ticker2.on_change('value', update)

src = make_dataset(ticker1.value,ticker2.value)  # the source of data is updated with the new selection from the dropdown menu

page_logo = make_plot(src)   # we make the plot with the selected values from the dropdown menu


layout = column(ticker1,ticker2, page_logo) # the app is desinged to have the rows in one column: the dropdown menus (up) and the plot (bottom)


curdoc().add_root(layout)   # we call the app to be shown


