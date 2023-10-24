import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from urllib.request import urlopen
import json



def generate_wealthy_ind_fig():
    skc = pd.DataFrame(
        ['20001', '20003', '20011',
         '20015', '20019', '20021',
         '20031', '20035', '20037',
         '20049', '20059', '20073',
         '20077', '20079', '20095',
         '20099', '20107', '20113',
         '20115', '20121', '20125',
         '20133', '20155', '20173',
         '20191', '20205', '20207'],
        columns=['fips']
    )

    token = 'pk.eyJ1Ijoid3N1cHBtYyIsImEiOiJjbDA2dWNiZmEyYjRqM2lsc2hrZ2g5Z3ZrIn0.Qcm0AOjbrEP6NPJ6u-14EA'

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv('data/healthy-wealthy-wise-data.csv', dtype={'fips': 'str'})
    df = df.sort_values(by=['wealthy_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['wealthy_quartile'].unique()):
        dfp = df[df['wealthy_quartile'] == quartile]
        fig.add_choroplethmapbox(
            geojson=counties,
            locations=dfp['fips'],
            z=[i, ] * len(dfp),
            featureidkey='id',
            showlegend=True,
            name=quartile,
            colorscale=colorscales[i],
            showscale=False,
            text='County:  ' + dfp['county'].str.title() +
                 '<br>Quartile:  ' + dfp['wealthy_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        zmin=0,
        zmax=0,
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['wealthy_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    fig.add_trace(choropleth)

    fig.update_layout(
        legend_title='Index Performance',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        mapbox_accesstoken=token,
        mapbox=dict(style='carto-positron', zoom=6, center={'lat': 38.4937, 'lon': -98.3804})
    )
    
   
    fig.update_layout(
            annotations=[
                dict(text='Low birth quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig


wealthy_ind_fig = generate_wealthy_ind_fig()

def generate_inc_ratio_ind_fig():
    skc = pd.DataFrame(
        ['20001', '20003', '20011',
         '20015', '20019', '20021',
         '20031', '20035', '20037',
         '20049', '20059', '20073',
         '20077', '20079', '20095',
         '20099', '20107', '20113',
         '20115', '20121', '20125',
         '20133', '20155', '20173',
         '20191', '20205', '20207'],
        columns=['fips']
    )

    token = 'pk.eyJ1Ijoid3N1cHBtYyIsImEiOiJjbDA2dWNiZmEyYjRqM2lsc2hrZ2g5Z3ZrIn0.Qcm0AOjbrEP6NPJ6u-14EA'

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv('data/healthy-wealthy-wise-data.csv', dtype={'fips': 'str'})
    df = df.sort_values(by=['inc_ratio_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['inc_ratio_quartile'].unique()):
        dfp = df[df['inc_ratio_quartile'] == quartile]
        fig.add_choroplethmapbox(
            geojson=counties,
            locations=dfp['fips'],
            z=[i, ] * len(dfp),
            featureidkey='id',
            showlegend=True,
            name=quartile,
            colorscale=colorscales[i],
            showscale=False,
            text='County:  ' + dfp['county'].str.title() +
                 '<br>Quartile:  ' + dfp['inc_ratio_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['inc_ratio_ind'],
        zmin=df['inc_ratio_ind'].min(),
        zmax=df['inc_ratio_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['inc_ratio_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    fig.add_trace(choropleth)

    fig.update_layout(
        legend_title='Index Performance',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        mapbox_accesstoken=token,
        mapbox=dict(style='carto-positron', zoom=6, center={'lat': 38.4937, 'lon': -98.3804})
    )
    
   
    fig.update_layout(
            annotations=[
                dict(text='Low birth quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig


inc_ratio_ind_fig = generate_inc_ratio_ind_fig()

def generate_child_pov_ind_fig():
    skc = pd.DataFrame(
        ['20001', '20003', '20011',
         '20015', '20019', '20021',
         '20031', '20035', '20037',
         '20049', '20059', '20073',
         '20077', '20079', '20095',
         '20099', '20107', '20113',
         '20115', '20121', '20125',
         '20133', '20155', '20173',
         '20191', '20205', '20207'],
        columns=['fips']
    )

    token = 'pk.eyJ1Ijoid3N1cHBtYyIsImEiOiJjbDA2dWNiZmEyYjRqM2lsc2hrZ2g5Z3ZrIn0.Qcm0AOjbrEP6NPJ6u-14EA'

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv('data/healthy-wealthy-wise-data.csv', dtype={'fips': 'str'})
    df = df.sort_values(by=['child_pov_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['child_pov_quartile'].unique()):
        dfp = df[df['child_pov_quartile'] == quartile]
        fig.add_choroplethmapbox(
            geojson=counties,
            locations=dfp['fips'],
            z=[i, ] * len(dfp),
            featureidkey='id',
            showlegend=True,
            name=quartile,
            colorscale=colorscales[i],
            showscale=False,
            text='County:  ' + dfp['county'].str.title() +
                 '<br>Quartile:  ' + dfp['child_pov_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['child_pov_ind'],
        zmin=df['child_pov_ind'].min(),
        zmax=df['child_pov_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['child_pov_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    fig.add_trace(choropleth)

    fig.update_layout(
        legend_title='Index Performance',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        mapbox_accesstoken=token,
        mapbox=dict(style='carto-positron', zoom=6, center={'lat': 38.4937, 'lon': -98.3804})
    )
    
   
    fig.update_layout(
            annotations=[
                dict(text='Low birth quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig


child_pov_ind_fig = generate_child_pov_ind_fig()

def generate_unemp_ind_fig():
    skc = pd.DataFrame(
        ['20001', '20003', '20011',
         '20015', '20019', '20021',
         '20031', '20035', '20037',
         '20049', '20059', '20073',
         '20077', '20079', '20095',
         '20099', '20107', '20113',
         '20115', '20121', '20125',
         '20133', '20155', '20173',
         '20191', '20205', '20207'],
        columns=['fips']
    )

    token = 'pk.eyJ1Ijoid3N1cHBtYyIsImEiOiJjbDA2dWNiZmEyYjRqM2lsc2hrZ2g5Z3ZrIn0.Qcm0AOjbrEP6NPJ6u-14EA'

    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    df = pd.read_csv('data/healthy-wealthy-wise-data.csv', dtype={'fips': 'str'})
    df = df.sort_values(by=['unemp_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['unemp_quartile'].unique()):
        dfp = df[df['unemp_quartile'] == quartile]
        fig.add_choroplethmapbox(
            geojson=counties,
            locations=dfp['fips'],
            z=[i, ] * len(dfp),
            featureidkey='id',
            showlegend=True,
            name=quartile,
            colorscale=colorscales[i],
            showscale=False,
            text='County:  ' + dfp['county'].str.title() +
                 '<br>Quartile:  ' + dfp['unemp_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['unemp_ind'],
        zmin=df['unemp_ind'].min(),
        zmax=df['unemp_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['unemp_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    fig.add_trace(choropleth)

    fig.update_layout(
        legend_title='Index Performance',
        margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        mapbox_accesstoken=token,
        mapbox=dict(style='carto-positron', zoom=6, center={'lat': 38.4937, 'lon': -98.3804})
    )
    
   
    fig.update_layout(
            annotations=[
                dict(text='Low birth quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig


unemp_ind_fig = generate_unemp_ind_fig()



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
    wealthindex.run_server(debug=True, use_reloader=False)


