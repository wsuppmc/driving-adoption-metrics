import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from urllib.request import urlopen
from health_indicator import health_indicator_fig
from fair_poor_ind import fair_poor_fig
from unhealthy_ind import unhealthy_indicator_fig
from unhealthy_mental_ind import unhealthy_mental_ind_fig
from low_birth_ind import low_birth_ind_fig
from smoking_ind import smoking_ind_fig
from obesity_ind import obesity_ind_fig
from inactive_ind import inactive_ind_fig
from drinking_ind import drinking_ind_fig
from uninsured_ind import uninsured_ind_fig



healthindex = dash.Dash(__name__)

# External CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    }
]
healthindex = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define your Dash layout
healthindex.layout = html.Div(
    children=[
        html.H1("Health Index", style={'textAlign': 'center'}),  # Title: Health Index in the center
        html.Div(
            dcc.Dropdown(
                id='index-dropdown',
                options=[
                    {'label': 'Health Index', 'value': 'health'},
                    {'label': '% Fair and Poor', 'value': 'fair_poor'},
                    {'label': 'Unhealthy', 'value': 'unhealthy_ind'},
                    {'label': 'Unhealthy mental days', 'value': 'unhealthy_mental_ind_fig'},
                    {'label': 'Low birth', 'value': 'low_birth_ind_fig'},
                    {'label': 'Smoking', 'value': 'smoking_ind_fig'},
                    {'label': 'obesity', 'value': 'obesity_ind_fig'},
                    {'label': 'inactive', 'value': 'inactive_ind_fig'},
                    {'label': 'drinking', 'value': 'drinking_ind_fig'},
                    {'label': 'uninsured quartile', 'value': 'uninsured_ind_fig'}


                ],
                value='health',  # Default value: 'health'
                style={'width': '75%'},  # Adjust the width of the dropdown to 35%
            ),
            style={'textAlign': 'left', 'marginLeft': '65%'}  # Move the dropdown to the right side with 65% margin from the left
        ),
        dcc.Graph(id='index-graph')
    ]
)

# Define the callback function to update the graph based on the dropdown selection
@healthindex.callback(
    dash.dependencies.Output('index-graph', 'figure'),
    [dash.dependencies.Input('index-dropdown', 'value')]
)
def update_graph(index):
    # Update the graph based on the dropdown selection
    if index == 'health':
        return health_indicator_fig
    elif index == 'fair_poor':
        return fair_poor_fig
    elif index == 'unhealthy_ind':
        return unhealthy_indicator_fig
    elif index == 'unhealthy_mental_ind_fig':
        return unhealthy_mental_ind_fig
    elif index == 'low_birth_ind_fig':
        return low_birth_ind_fig
    elif index == 'smoking_ind_fig':
        return smoking_ind_fig
    elif index == 'obesity_ind_fig':
        return obesity_ind_fig
    elif index == 'inactive_ind_fig':
        return inactive_ind_fig
    elif index == 'drinking_ind':
        return drinking_ind_fig
    elif index == 'drinking_ind':
        return drinking_ind_fig
    elif index == 'uninsured_ind_fig':
        return uninsured_ind_fig
    else:
        # Handle other cases
        return go.Figure()

if __name__ == '__main__':
    healthindex.run_server(debug=True)


