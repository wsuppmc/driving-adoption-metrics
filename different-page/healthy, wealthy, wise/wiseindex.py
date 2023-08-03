import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from soc_assoc_ind import soc_assoc_ind_fig
from some_college_ind import some_college_ind_fig
from high_school_ind import high_school_ind_fig
from wise_ind import wise_ind_fig




wiseindex = dash.Dash(__name__)

# External CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    }
]
wiseindex = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define your Dash layout
wiseindex.layout = html.Div(
    children=[
        html.H1("Wealth Index", style={'textAlign': 'center'}),  # Title: Health Index in the center
        html.Div(
            dcc.Dropdown(
                id='index-dropdown',
                options=[
                    {'label': 'wise indicator', 'value': 'wise_ind_fig'},
                    {'label': 'Social association', 'value': 'soc_assoc_ind_fig'},
                    {'label': 'Some college', 'value': 'some_college_ind_fig'},
                    {'label': 'High school', 'value': 'high_school_ind_fig'}
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
@wiseindex.callback(
    dash.dependencies.Output('index-graph', 'figure'),
    [dash.dependencies.Input('index-dropdown', 'value')]
)
def update_graph(index):
    # Update the graph based on the dropdown selection
    if index == 'wise_ind_fig':
        return wise_ind_fig
    elif index == 'soc_assoc_ind':
        return soc_assoc_ind_fig
    elif index == 'some_college_ind':
        return some_college_ind_fig
    elif index == 'high_school_ind_fig':
        return high_school_ind_fig
    else:
        # Handle other cases
        return go.Figure()

if __name__ == '__main__':
    wiseindex.run_server(debug=True)


