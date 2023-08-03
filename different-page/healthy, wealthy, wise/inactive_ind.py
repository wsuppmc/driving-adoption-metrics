import pandas as pd
import json
import plotly.graph_objects as go
from urllib.request import urlopen


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
