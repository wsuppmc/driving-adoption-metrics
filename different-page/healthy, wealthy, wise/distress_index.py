import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from distress import distress_fig
from hs_lower import hs_lower_fig
from vacancy_rate import vacancy_rate_fig
from unemployment_rate import unemployment_rate_fig
from poverty_rate import poverty_rate_fig
from med_inc_rate import med_inc_rate_fig
from emp_chg import emp_chg_fig
from est_chg import est_chg_fig



distress_index = dash.Dash(__name__)

# External CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    }
]
distress_index = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define your Dash layout
distress_index.layout = html.Div(
    children=[
        html.H1("Health Index", style={'textAlign': 'center'}),  # Title: Health Index in the center
        html.Div(
            dcc.Dropdown(
                id='index-dropdown',
                options=[
                    {'label': 'Distress Index', 'value': 'distress_fig'},
                    {'label': 'No Highschool Diploma', 'value': 'hs_lower_fig'},
                    {'label': 'Housing Vacancy Rate', 'value': 'vacancy_rate_fig'},
                    {'label': 'Unemployment Rate', 'value': 'unemployment_rate_fig'},
                    {'label': 'Poverty Rate', 'value': 'poverty_rate_fig'},
                    {'label': 'Median Income Ratio', 'value': 'med_inc_rate_fig'},
                    {'label': 'Change in Employement', 'value': 'emp_chg_fig'},
                    {'label': 'Change in Establishment', 'value': 'est_chg_fig'},
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
@distress_index.callback(
    dash.dependencies.Output('index-graph', 'figure'),
    [dash.dependencies.Input('index-dropdown', 'value')]
)
def update_graph(index):
    # Update the graph based on the dropdown selection
    if index == 'distress_fig':
        return distress_fig
    elif index == 'hs_lower_fig':
        return hs_lower_fig
    elif index == 'vacancy_rate_fig':
        return vacancy_rate_fig
    elif index == 'unemployment_rate_fig':
        return unemployment_rate_fig
    elif index == 'poverty_rate_fig':
        return poverty_rate_fig
    elif index == 'med_inc_rate_fig':
        return med_inc_rate_fig
    elif index == 'emp_chg_fig':
        return emp_chg_fig
    elif index == 'est_chg_fig':
        return est_chg_fig
    else:
        # Handle other cases
        return go.Figure()

if __name__ == '__main__':
    distress_index.run_server(debug=True)


