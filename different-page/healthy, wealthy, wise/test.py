import flask
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from urllib.request import urlopen
import json



def generate_health_ind_fig():
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
    df = df.sort_values(by=['healthy_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['healthy_quartile'].unique()):
        dfp = df[df['healthy_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['healthy_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        zmin=0,
        zmax=0,
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['healthy_quartile'].str.split(' ').str[0],
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
                dict(text='Health Indicator', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

health_indicator_fig = generate_health_ind_fig()


def generate_fair_poor_fig():
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
    df = df.sort_values(by=['fair_poor_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['fair_poor_quartile'].unique()):
        dfp = df[df['fair_poor_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['fair_poor_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['fair_poor_ind'],
        zmin=df['fair_poor_ind'].min(),
        zmax=df['fair_poor_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['fair_poor_quartile'].str.split(' ').str[0],
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
                dict(text='Health Indicator', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

fair_poor_fig = generate_fair_poor_fig()

def generate_unhealthy_mental_ind_fig():
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
    df = df.sort_values(by=['unhealthy_mental_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['unhealthy_mental_quartile'].unique()):
        dfp = df[df['unhealthy_mental_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['unhealthy_mental_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['unhealthy_mental_ind'],
        zmin=df['unhealthy_mental_ind'].min(),
        zmax=df['unhealthy_mental_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['unhealthy_mental_quartile'].str.split(' ').str[0],
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
                dict(text='unhealthy mental quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

unhealthy_mental_ind_fig = generate_unhealthy_mental_ind_fig()

def generate_unhealth_ind_fig():
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
    df = df.sort_values(by=['unhealthy_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['unhealthy_quartile'].unique()):
        dfp = df[df['unhealthy_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['unhealthy_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['unhealthy_ind'],
        zmin=df['unhealthy_ind'].min(),
        zmax=df['unhealthy_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['unhealthy_quartile'].str.split(' ').str[0],
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
                dict(text='Unhealthy indicator', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

unhealthy_indicator_fig = generate_unhealth_ind_fig()

def generate_low_birth_ind_fig():
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
    df = df.sort_values(by=['low_birth_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['low_birth_quartile'].unique()):
        dfp = df[df['low_birth_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['low_birth_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['low_birth_ind'],
        zmin=df['low_birth_ind'].min(),
        zmax=df['low_birth_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['low_birth_quartile'].str.split(' ').str[0],
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

low_birth_ind_fig = generate_low_birth_ind_fig()

def generate_smoking_ind_fig():
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
    df = df.sort_values(by=['smoking_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['smoking_quartile'].unique()):
        dfp = df[df['smoking_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['smoking_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['smoking_ind'],
        zmin=df['smoking_ind'].min(),
        zmax=df['smoking_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['smoking_quartile'].str.split(' ').str[0],
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
                dict(text='smoking', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

smoking_ind_fig = generate_smoking_ind_fig()

def generate_obesity_ind_fig():
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
    df = df.sort_values(by=['obesity_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['obesity_quartile'].unique()):
        dfp = df[df['obesity_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['obesity_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['obesity_ind'],
        zmin=df['obesity_ind'].min(),
        zmax=df['obesity_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['obesity_quartile'].str.split(' ').str[0],
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
                dict(text='smoking', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

obesity_ind_fig = generate_obesity_ind_fig()

def generate_inactive_ind_fig():
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
    df = df.sort_values(by=['inactive_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['inactive_quartile'].unique()):
        dfp = df[df['inactive_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['inactive_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['inactive_ind'],
        zmin=df['inactive_ind'].min(),
        zmax=df['inactive_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['inactive_quartile'].str.split(' ').str[0],
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
                dict(text='inactive', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

inactive_ind_fig = generate_inactive_ind_fig()

def generate_drinking_ind_fig():
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
    df = df.sort_values(by=['drinking_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['drinking_quartile'].unique()):
        dfp = df[df['drinking_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['drinking_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['drinking_ind'],
        zmin=df['drinking_ind'].min(),
        zmax=df['drinking_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['drinking_quartile'].str.split(' ').str[0],
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
                dict(text='drinking quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

drinking_ind_fig = generate_drinking_ind_fig()

def generate_uninsured_ind_fig():
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
    df = df.sort_values(by=['uninsured_quartile'])

    colorscales = [
        [(0.0, 'rgba(22,74,88,1.0)'), (1.0, 'rgba(22,74,88,1.0)')],
        [(0.0, 'rgba(22,74,88,0.75)'), (1.0, 'rgba(22,74,88,0.75)')],
        [(0.0, 'rgba(22,74,88,0.5)'), (1.0, 'rgba(22,74,88,0.5)')],
        [(0.0, 'rgba(22,74,88,0.25)'), (1.0, 'rgba(22,74,88,0.25)')]
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['uninsured_quartile'].unique()):
        dfp = df[df['uninsured_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['uninsured_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['uninsured_ind'],
        zmin=df['uninsured_ind'].min(),
        zmax=df['uninsured_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(255,193,0)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['uninsured_quartile'].str.split(' ').str[0],
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
                dict(text='uninsured quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

uninsured_ind_fig = generate_uninsured_ind_fig()

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

def generate_wise_ind_fig():
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
    df = df.sort_values(by=['wise_quartile'])

    colorscales = [
    ((0.0, 'rgba(255,193,0,0.25)'), (1.0, 'rgba(255,193,0,0.25)')),
    ((0.0, 'rgba(255,193,0,0.5)'), (1.0, 'rgba(255,193,0,0.5)')),
    ((0.0, 'rgba(255,193,0,0.75)'), (1.0, 'rgba(255,193,0,0.75)')),
    ((0.0, 'rgba(255,193,0,1.0)'), (1.0, 'rgba(255,193,0,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['wise_quartile'].unique()):
        dfp = df[df['wise_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['wise_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        zmin=0,
        zmax=0,
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(22,74,88)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['wise_quartile'].str.split(' ').str[0],
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
                dict(text='wise quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

wise_ind_fig = generate_wise_ind_fig()

def generate_high_school_ind_fig():
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
    df = df.sort_values(by=['high_school_quartile'])

    colorscales = [
    ((0.0, 'rgba(255,193,0,0.25)'), (1.0, 'rgba(255,193,0,0.25)')),
    ((0.0, 'rgba(255,193,0,0.5)'), (1.0, 'rgba(255,193,0,0.5)')),
    ((0.0, 'rgba(255,193,0,0.75)'), (1.0, 'rgba(255,193,0,0.75)')),
    ((0.0, 'rgba(255,193,0,1.0)'), (1.0, 'rgba(255,193,0,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['high_school_quartile'].unique()):
        dfp = df[df['high_school_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['high_school_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['high_school_ind'],
        zmin=df['high_school_ind'].min(),
        zmax=df['high_school_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(22,74,88)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['high_school_quartile'].str.split(' ').str[0],
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
                dict(text='high school quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

high_school_ind_fig = generate_high_school_ind_fig()

def generate_some_college_ind_fig():
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
    df = df.sort_values(by=['some_college_quartile'])

    colorscales = [
    ((0.0, 'rgba(255,193,0,0.25)'), (1.0, 'rgba(255,193,0,0.25)')),
    ((0.0, 'rgba(255,193,0,0.5)'), (1.0, 'rgba(255,193,0,0.5)')),
    ((0.0, 'rgba(255,193,0,0.75)'), (1.0, 'rgba(255,193,0,0.75)')),
    ((0.0, 'rgba(255,193,0,1.0)'), (1.0, 'rgba(255,193,0,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['some_college_quartile'].unique()):
        dfp = df[df['some_college_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['some_college_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['some_college_ind'],
        zmin=df['some_college_ind'].min(),
        zmax=df['some_college_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(22,74,88)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['some_college_quartile'].str.split(' ').str[0],
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
                dict(text='some college quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

some_college_ind_fig = generate_some_college_ind_fig()

def generate_soc_assoc_ind_fig():
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
    df = df.sort_values(by=['soc_assoc_quartile'])

    colorscales = [
    ((0.0, 'rgba(255,193,0,0.25)'), (1.0, 'rgba(255,193,0,0.25)')),
    ((0.0, 'rgba(255,193,0,0.5)'), (1.0, 'rgba(255,193,0,0.5)')),
    ((0.0, 'rgba(255,193,0,0.75)'), (1.0, 'rgba(255,193,0,0.75)')),
    ((0.0, 'rgba(255,193,0,1.0)'), (1.0, 'rgba(255,193,0,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['soc_assoc_quartile'].unique()):
        dfp = df[df['soc_assoc_quartile'] == quartile]
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
                 '<br>Quartile:  ' + dfp['soc_assoc_quartile'].str.split(' ').str[0],
            hoverinfo='text'
        )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['soc_assoc_ind'],
        zmin=df['soc_assoc_ind'].min(),
        zmax=df['soc_assoc_ind'].max(),
        colorscale=[[0, 'rgba(0, 0, 0, 0)'], [1, 'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(22,74,88)',
        marker_line_width=2,
        showscale=False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
             '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['soc_assoc_quartile'].str.split(' ').str[0],
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
                dict(text='soc assoc quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

soc_assoc_ind_fig = generate_soc_assoc_ind_fig()

def generate_distress_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['index_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['index_quartile'].unique()):
        dfp = df[df['index_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['index_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        zmin=0, zmax=0,
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['index_quartile'].str.split(' ').str[0],
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
                dict(text='Distress Index', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

distress_fig = generate_distress_fig()

def generate_hs_lower_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['hs_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['hs_quartile'].unique()):
        dfp = df[df['hs_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['hs_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['hs_lower'],
        zmin=df['hs_lower'].min(), 
        zmax=df['hs_lower'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['index_quartile'].str.split(' ').str[0],
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
                dict(text='hs quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

hs_lower_fig = generate_hs_lower_fig()

def generate_vacancy_rate_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['vacancy_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['vacancy_quartile'].unique()):
        dfp = df[df['vacancy_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['vacancy_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['vacancy_rate'],
        zmin=df['vacancy_rate'].min(), 
        zmax=df['vacancy_rate'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['vacancy_quartile'].str.split(' ').str[0],
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
                dict(text='Vacancy Rate', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

vacancy_rate_fig = generate_vacancy_rate_fig()

def generate_unemployment_rate_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
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
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['unemp_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['unemployment_rate'],
        zmin=df['unemployment_rate'].min(), 
        zmax=df['unemployment_rate'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
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
                dict(text='Unemployment Rate', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

unemployment_rate_fig = generate_unemployment_rate_fig()

def generate_poverty_rate_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['poverty_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['poverty_quartile'].unique()):
        dfp = df[df['poverty_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['poverty_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['poverty_rate'],
        zmin=df['poverty_rate'].min(), 
        zmax=df['poverty_rate'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['poverty_quartile'].str.split(' ').str[0],
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
                dict(text='Poverty Rate', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

poverty_rate_fig = generate_poverty_rate_fig()

def generate_med_inc_rate_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['med_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['med_quartile'].unique()):
        dfp = df[df['med_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['med_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['med_inc_rate'],
        zmin=df['med_inc_rate'].min(), 
        zmax=df['med_inc_rate'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['med_quartile'].str.split(' ').str[0],
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
                dict(text='med inc rate', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

med_inc_rate_fig = generate_med_inc_rate_fig()

def generate_emp_chg_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['emp_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['emp_quartile'].unique()):
        dfp = df[df['emp_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['emp_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['emp_chg'],
        zmin=df['emp_chg'].min(), 
        zmax=df['emp_chg'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['emp_quartile'].str.split(' ').str[0],
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
                dict(text='Employment Quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

emp_chg_fig = generate_emp_chg_fig()

def generate_est_chg_fig():
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


    df = pd.read_csv('data/2020-distress-index-data.csv', dtype={'fips':'str'})
    df = df.sort_values(by=['est_quartile'])

    colorscales = [
    ((0.0, 'rgba(231,38,40,0.25)'), (1.0, 'rgba(231,38,40,0.25)')),
    ((0.0, 'rgba(231,38,40,0.5)'), (1.0, 'rgba(231,38,40,0.5)')),
    ((0.0, 'rgba(231,38,40,0.75)'), (1.0, 'rgba(231,38,40,0.75)')),
    ((0.0, 'rgba(231,38,40,1.0)'), (1.0, 'rgba(231,38,40,1.0)'))
    ]

    fig = go.Figure()

    for i, quartile in enumerate(df['est_quartile'].unique()):
        dfp = df[df['est_quartile'] == quartile]
        fig.add_choroplethmapbox(
        geojson=counties, locations=dfp['fips'],
        z=[i,] * len(dfp), featureidkey='id',
        showlegend=True, name=quartile,
        colorscale=colorscales[i], showscale=False,
        text='County:  ' + dfp['county'].str.title() +
        '<br>Quartile:  ' + dfp['est_quartile'].str.split(' ').str[0],
        hoverinfo='text'
    )

    choropleth = go.Choroplethmapbox(
        geojson=counties,
        locations=df[df.fips.isin(skc['fips'].tolist())]['fips'],
        z=df[df.fips.isin(skc['fips'].tolist())]['est_chg'],
        zmin=df['est_chg'].min(), 
        zmax=df['est_chg'].max(),
        colorscale = [[0,'rgba(0, 0, 0, 0)'],[1,'rgba(0, 0, 0, 0)']],
        marker_line_color='rgb(131,201,217)',
        marker_line_width=2,
        showscale = False,
        text='County:  ' + df[df.fips.isin(skc['fips'].tolist())]['county'].str.title() +
        '<br>Quartile:  ' + df[df.fips.isin(skc['fips'].tolist())]['est_quartile'].str.split(' ').str[0],
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
                dict(text='Employment Quartile', showarrow=False, x=0.5, y=1.05, xref='paper', yref='paper', align='center')
            ]
        )

    return fig

est_chg_fig = generate_est_chg_fig()


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
    "% Completed Highschool": high_school_ind_fig,
    "% Some College": some_college_ind_fig,
    "Social Association Rate": soc_assoc_ind_fig
}

distress_maps = {
    "Distress Indicator":distress_fig,
    "No Highschool Diploma": hs_lower_fig,
    "Housing Vacancy Rate": vacancy_rate_fig,
    "Unemployment Rate": unemployment_rate_fig,
    "Poverty Rate": poverty_rate_fig,
    "Median Income Ratio": med_inc_rate_fig,
    "Change in Employement": emp_chg_fig,
    "Change in Establishment": est_chg_fig
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
        value = list(distress_maps.keys())[0]
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

