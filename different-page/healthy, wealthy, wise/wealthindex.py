import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from urllib.request import urlopen
from inc_ratio_ind import inc_ratio_ind_fig
from child_pov_ind import child_pov_ind_fig
from unemp_ind import unemp_ind_fig
from wealthy_ind import wealthy_ind_fig


wealthindex = dash.Dash(__name__)

# External CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    }
]
wealthindex = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define your Dash layout
wealthindex.layout = html.Div(
    children=[
        html.H1("Wealth Index", style={'textAlign': 'center'}),  # Title: Health Index in the center
        html.Div(
            dcc.Dropdown(
                id='index-dropdown',
                options=[
                    {'label': 'wealth Indicator', 'value': 'wealthy_ind_fig'},
                    {'label': 'Income Ratio', 'value': 'inc_ratio_ind_fig'},
                    {'label': '% children in poverty', 'value': 'child_pov_ind_fig'},
                    {'label': 'unemployment rate', 'value': 'unemp_ind_fig'}
                ],
                value='Wealth',  # Default value: 'wealth'
                style={'width': '75%'},  # Adjust the width of the dropdown to 35%
            ),
            style={'textAlign': 'left', 'marginLeft': '65%'}  # Move the dropdown to the right side with 65% margin from the left
        ),
        dcc.Graph(id='index-graph')
    ]
)

# Define the callback function to update the graph based on the dropdown selection
@wealthindex.callback(
    dash.dependencies.Output('index-graph', 'figure'),
    [dash.dependencies.Input('index-dropdown', 'value')]
)
def update_graph(index):
    # Update the graph based on the dropdown selection
    if index == 'wealthy_ind_fig':
        return wealthy_ind_fig
    elif index == 'inc_ratio_ind_fig':
        return inc_ratio_ind_fig
    elif index == 'child_pov_ind_fig':
        return child_pov_ind_fig
    elif index == 'unemp_ind_fig':
        return unemp_ind_fig
    else:
        # Handle other cases
        return go.Figure()

if __name__ == '__main__':
    wealthindex.run_server(debug=True)


