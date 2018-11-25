################
# Author: Santiago Erroz Ferrer
# To run the app from the terminal in the folder Interactive_plots_with_python_bokeh:
# bokeh serve my_app --show
# source of figures: Erroz-Ferrer et al 2019 (MNRAS)
################


from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
from bokeh.layouts import row, column
from bokeh.models.widgets import PreText, Select
import glob


def update(attr, old, new):   # This function updates the plot once we select a new value in the dropdown menu
    new_src = make_dataset(ticker1.value)
    src.data.update(new_src.data)

def make_plot(source):    # This function reads the pdf file that was produced using challenge.py
    page_logo = figure(plot_width = 1400, plot_height = 800)
    page_logo.toolbar.logo = None
    page_logo.toolbar_location = None
    page_logo.x_range=Range1d(start=0, end=1)
    page_logo.y_range=Range1d(start=0, end=1)
    page_logo.xaxis.visible = None
    page_logo.yaxis.visible = None
    page_logo.xgrid.grid_line_color = None
    page_logo.ygrid.grid_line_color = None
    page_logo.image_url(url='url', x=0.0, y = 1, h=None, w=None, source=source)
    page_logo.outline_line_alpha = 0 
    return page_logo

def make_dataset(name):   # This function selects the filename to read
    filename = './my_app/static/'+name+'.pdf'
    return ColumnDataSource(dict(url = [filename]))


# Now we start with the main part

paths = glob.glob('./my_app/static/*pdf')   # First we read the paths of the pdfs that were produced with challenge.py

data = list()     # We create a list with the databases that is plotted at each path
for file in paths:
    name=file.split('./my_app/static/')[1].split('.pdf')[0]
    data.append(name)
DEFAULT_TICKERS = data


ticker1 = Select(title='Select activity to plot',value=data[0], options= DEFAULT_TICKERS)   # dropdown select with the databases
ticker1.on_change('value', update)    # this will update the plot once we select a new option in the dropdown menu

src = make_dataset(ticker1.value)    # the source of data is updated with the new selection from the dropdown menu

page_logo = make_plot(src)    # we make the plot with the selected values from the dropdown menu


layout = column(ticker1, page_logo)   # the app is desinged to have two rows in one column: the dropdown menu (up) and the plot (bottom)


curdoc().add_root(layout)   # we call the app to be shown


