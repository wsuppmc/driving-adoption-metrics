import dash
import flask
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
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

from inc_ratio_ind import inc_ratio_ind_fig
from child_pov_ind import child_pov_ind_fig
from unemp_ind import unemp_ind_fig
from wealthy_ind import wealthy_ind_fig

from soc_assoc_ind import soc_assoc_ind_fig
from some_college_ind import some_college_ind_fig
from high_school_ind import high_school_ind_fig
from wise_ind import wise_ind_fig

from distress import distress_fig
from hs_lower import hs_lower_fig
from vacancy_rate import vacancy_rate_fig
from unemployment_rate import unemployment_rate_fig
from poverty_rate import poverty_rate_fig
from med_inc_rate import med_inc_rate_fig
from emp_chg import emp_chg_fig
from est_chg import est_chg_fig

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
health_maps = {
    "Health Indicator": health_indicator_fig,
    "% Fair or Poor Health": fair_poor_fig,
    "Average Number of Physically Unhealthy Days": unhealthy_indicator_fig,
    "Average Number of Mentally Unhealthy Days ": unhealthy_mental_ind_fig,    
    "% Low Birthweight": low_birth_ind_fig,
    "% Adults Reporting Currently Smoking": smoking_ind_fig,
    "% Adults with Obesity": obesity_ind_fig,
    "% Physically Inactive": inactive_ind_fig,
    "% Excessive Drinking": drinking_ind_fig,
    "% Uninsured": uninsured_ind_fig
}

wealth_maps = {
    "Wealth Indicator": wealthy_ind_fig,
    "Income Ratio": inc_ratio_ind_fig,
    "% Children in Poverty": child_pov_ind_fig,
    "Unemployment Rate": unemp_ind_fig,

}

wise_maps = {
    "Wise Indicator": wise_ind_fig,
    "% Completed High School": high_school_ind_fig,
    "% Some College": some_college_ind_fig,
    "Social Association Rate": soc_assoc_ind_fig
}

distress_maps = {
<<<<<<< Updated upstream
    "Distress Indicator":distress_fig,
    "No Highschool Diploma": hs_lower_fig,
=======
    "Distress Index": distress_fig,
    "% No High School Diploma": hs_lower_fig,
>>>>>>> Stashed changes
    "Housing Vacancy Rate": vacancy_rate_fig,
    "Unemployment Rate": unemployment_rate_fig,
    "Poverty Rate": poverty_rate_fig,
    "Median Income Ratio": med_inc_rate_fig,
<<<<<<< Updated upstream
    "Change in Employement": emp_chg_fig,
    "Change in Establishment": est_chg_fig
=======
    "Change in Employment": emp_chg_fig,
    "Change in Establishments": est_chg_fig
>>>>>>> Stashed changes
}

server = flask.Flask(__name__)
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Healthy, Wealthy, And Wise Dashboard"),
    
    # First dropdown to select index type
    dcc.Dropdown(
        id='index-type-dropdown',
        options=[
            {'label': 'Health Index', 'value': 'health'},
            {'label': 'Wealth Index', 'value': 'wealth'},
            {'label': 'Wise Index', 'value': 'wise'},
            {'label': 'Distress Index', 'value': 'distress'}

        ],
        value='health',
        style={'width': '40%', 'display': 'inline-block'}
    ),
    
    # Second dropdown to select specific map based on the index type
    dcc.Dropdown(
        id='map-option-dropdown',
        style={'width': '40%', 'display': 'inline-block', 'float': 'right'}
    ),
    
    # Placeholder for displaying the selected map
    dcc.Graph(id='main-map')
])

# Callback to update the second dropdown based on the selected index type
@app.callback(
    Output('map-option-dropdown', 'options'),
    Output('map-option-dropdown', 'value'),
    Input('index-type-dropdown', 'value')
)
def update_map_options(index_type):
    if index_type == 'health':
        options = [{'label': option, 'value': option} for option in health_maps.keys()]
        value = list(health_maps.keys())[0]
    elif index_type == 'wealth':
        options = [{'label': option, 'value': option} for option in wealth_maps.keys()]
        value = list(wealth_maps.keys())[0]
    elif index_type == 'wise':
        options = [{'label': option, 'value': option} for option in wise_maps.keys()]
        value = list(wise_maps.keys())[0]
    elif index_type == 'distress':
        options = [{'label': option, 'value': option} for option in distress_maps.keys()]
<<<<<<< Updated upstream
        value = list(distress_maps.keys())[0]
=======
        value = list(wise_maps.keys())[0]
>>>>>>> Stashed changes
    else:
        options = []
        value = None
    return options, value

# Callback to update the main map based on the selected index type and map option
@app.callback(
    Output('main-map', 'figure'),
    Input('index-type-dropdown', 'value'),
    Input('map-option-dropdown', 'value')
)
def update_main_map(index_type, map_option):
    if index_type == 'health':
        map_data = health_maps.get(map_option, None)
    elif index_type == 'wealth':
        map_data = wealth_maps.get(map_option, None)
    elif index_type == 'wise':
        map_data = wise_maps.get(map_option, None)
    elif index_type == 'distress':
        map_data = distress_maps.get(map_option, None)
    else:
        map_data = None

    return map_data



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

