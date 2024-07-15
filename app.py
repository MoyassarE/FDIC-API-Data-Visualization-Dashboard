# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 19:37:13 2024

@author: me384
"""

# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by_Ploytly/execute-code-in-browser

from dash import Dash, dcc, Output, Input   # pip intall dash
import dash_bootstrap_components as dbc     # pip install dash-bootstrap-components
from dataschema.dataschema import getGraphOfChildLevelItems, getTreeMapGraphOfAllCategories


treefig = getTreeMapGraphOfAllCategories()


# Every dashboad is components displayed through the layout that interact with each other through the callback

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
server = app.server


mytitle = dcc.Markdown(children="# Breakdown of Balance Sheet Categories for Failed Banks")
CategoryBeakdownChart = dcc.Graph(figure={})
CategoryUserSelectionChart = dcc.Graph(id='treemap',figure=treefig, clickData="Assets")


# Customize your own Layout

app.layout = dbc.Container([mytitle, CategoryBeakdownChart,  CategoryUserSelectionChart])



# Callback allows components to interact
@app.callback(
    Output(CategoryBeakdownChart, component_property='figure'),
    Input(CategoryUserSelectionChart, component_property="clickData")
)

def update_graph(userclick): # function arguments come from the component_property of the Input
    fig = getGraphOfChildLevelItems(userclick['points'][0]['label'])
        
    return fig # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8050)
    
    
'''
The dashboad will run on your local host. Paste the below location to your browser:

127.0.0.1:8050
'''






























