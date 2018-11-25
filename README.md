# Interactive plots with python

Create apps to make interactive plots with python/bokeh.

## Requirements

These codes have been written using python 3 and require the following libraries: bokeh, glob, pandas

## my_app : Interactive figures

This folder contains an application that plots the figures inside a folder. One can interactively select the pdf to represent and it will be displayed. The program reads the figures inside the "static" folder and has the option to choose from those figures to be presented in the browser. 

To run the app from the terminal in the folder Interactive_plots_with_python_bokeh:

```
bokeh serve my_app --show
```

Source of example figures: Erroz-Ferrer et al 2019 (MNRAS)


## my_app2 : Interactive plots from tables

This folder contains an application that creates barplots with the selected rows and columns from a table. The program reads the tables inside the "static" folder. Then, barplots are created with the selected rows and columns in the table, which can be interactively selected.

To run the app from the terminal in the folder Interactive_plots_with_python_bokeh:

```
bokeh serve my_app2 --show
```

Source of example data: chemical reactions and their components
