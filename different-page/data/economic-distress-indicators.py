# libraries
import numpy as np
import pandas as pd
import requests
import scipy.stats as ss
import matplotlib as mpl
import json
import plotly.graph_objects as go
from urllib.request import urlopen

with open('../data/census-key.txt') as key:
    api_key = key.read().strip() 

years = ['2017', '2018']
county = '*'
state = '*'    
    
for year in years:    
    # pulls five of the components from the acs 5-year data api and creates a dataframe
    dsource = 'acs'
    dname = 'acs5'
    dset = 'profile'
    cols = 'NAME,DP02_0066PE,DP03_0128PE,DP03_0009PE,DP03_0062E'    

    base_url = f'https://api.census.gov/data/{year}/{dsource}/{dname}/{dset}'    
    data_url = f'{base_url}?get={cols}&for=county:{county}&in=state:{state}&key={api_key}'
    response = requests.get(data_url)

    state_url = f'{base_url}?get=DP03_0062E&for=state:{state}&key={api_key}'
    state_response = requests.get(state_url)

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0]).\
        rename(columns={
        'DP02_0066PE':'hs_higher', 'DP03_0128PE':'poverty_rate', 
        'DP03_0009PE':'unemployment_rate', 'DP03_0062E':'median_income'
    })

    df['fips'] = df['state']+df['county']

    df.drop(columns=['county'], inplace=True)
    df = df.astype(dtype={
        'hs_higher':'float64', 'unemployment_rate':'float64', 
        'poverty_rate':'float64', 'median_income':'float64'
    }).reset_index()

    df['county'] = df['NAME'].str.split(' County').str.get(0)
    df['state_name'] = df['NAME'].str.split(', ').str.get(-1)
    df['hs_lower'] = 100 - df['hs_higher']

    inc_data = state_response.json()
    dfs = pd.DataFrame(inc_data[1:], columns=inc_data[0]).\
        rename(columns={'DP03_0062E':'st_med_inc'})
    dfs = dfs.astype(dtype={'st_med_inc':'float64'})

    df = pd.merge(df, dfs, how='left', on='state')
    df['med_inc_rate'] = (df['median_income']/df['st_med_inc']).round(3)*100

    df.drop(df[df['state']=='72'].index, inplace=True)

    df_acs = df[[
        'fips', 'state', 'county', 'state_name', 'hs_lower', 
        'unemployment_rate', 'poverty_rate', 'median_income', 'st_med_inc', 'med_inc_rate'
    ]]


    # pulls data from cbp api and calculates averages change over specified years
    dfs = []    

    yrs = [str(year) for year in list(range(int(year)-1, int(year)+1))]

    for yr in yrs:  
        dsource = 'cbp'
        cols = 'ESTAB,EMP'

        base_url = f'https://api.census.gov/data/{yr}/{dsource}' 
        data_url = f'{base_url}?get={cols}&for=county:{county}&in=state:{state}&key={api_key}'
        response=requests.get(data_url)

        # turns the json data into a dataframe object
        data = response.json()
        dfy = pd.DataFrame(data[1:], columns=data[0]).\
            rename(columns={'ESTAB':'establishments', 'EMP':'employment'})
        dfy['fips'] = dfy['state']+dfy['county']
        dfy['year'] = yr
        dfy.drop(columns=['state', 'county'], inplace=True)
        dfy = dfy.astype(dtype={'establishments':'float64', 'employment':'float64'})

        # appends the year dataframe to the list
        dfs.append(dfy)

    # concatenates the individual dataframes and returns a single dataframe
    df = pd.concat(dfs, ignore_index=True)
    df.sort_values(by=['fips', 'year'], inplace=True)

    df['employment'] = df['employment'].replace(0, np.nan)
    df['employment'] = df['employment'].fillna(df.groupby('fips')['employment'].transform('mean'))

    df['est_chg'] = df.sort_values('year').groupby('fips')['establishments'].pct_change()*100
    df['emp_chg'] = df.sort_values('year').groupby('fips')['employment'].pct_change()*100

    df1 = df.groupby('fips')['est_chg'].mean().round(1).reset_index()
    df2 = df.groupby('fips')['emp_chg'].mean().round(1).reset_index()

    df_cbp = pd.merge(df1, df2, how='left', on='fips')


    # pulls vacancy data from acs 5-year detailed dataset
    dsource = 'acs'
    dname = 'acs5'
    cols = 'NAME,B25002_001E,B25002_003E,B25004_006E'

    base_url = f'https://api.census.gov/data/{year}/{dsource}/{dname}'    
    with open('../data/census-key.txt') as key:
        api_key = key.read().strip()    

    data_url = f'{base_url}?get={cols}&for=county:{county}&in=state:{state}&key={api_key}'
    response = requests.get(data_url)

    state_url = f'{base_url}?get=DP03_0062E&for=state:{state}&key={api_key}'
    state_response = requests.get(state_url)

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0]).\
        rename(columns={
        'B25002_001E':'total', 'B25002_003E':'vacant', 'B25004_006E':'seasonal'
    })

    df['fips'] = df['state']+df['county']
    df['vacancy_rate'] = ((df['vacant'].astype(float)-df['seasonal'].astype(float))/df['total'].astype(float)*100).round(1)

    df_vac = df[['fips', 'vacancy_rate']]


    # combines the three dataframes and sorts by county name
    dff = pd.merge(df_acs, df_cbp, how='left', on='fips')
    df = pd.merge(dff, df_vac, how='left', on='fips')

    df.sort_values(by=['state', 'county'], inplace=True)

    df.loc[df['est_chg'].isnull(), 'est_chg'] = df.groupby('state')['est_chg'].transform('mean')
    df.loc[df['emp_chg'].isnull(), 'emp_chg'] = df.groupby('state')['emp_chg'].transform('mean')

    df['hs_rank'] = df['hs_lower'].rank(method='average', ascending=True)
    df['vacancy_rank'] = df['vacancy_rate'].rank(method='average', ascending=True)
    df['unemp_rank'] = df['unemployment_rate'].rank(method='average', ascending=True)
    df['poverty_rank'] = df['poverty_rate'].rank(method='average', ascending=True)
    df['med_rank'] = df['med_inc_rate'].rank(method='average', ascending=False)
    df['est_rank'] = df['est_chg'].rank(method='average', ascending=False)
    df['emp_rank'] = df['emp_chg'].rank(method='average', ascending=False)

    df['avg_rank'] = df.iloc[:,-7:].mean(axis=1).round(1)
    df['pct_rank'] = df['avg_rank'].rank(pct=True, method='average').round(3)*100
    df['us_rank'] = df['avg_rank'].rank(method='average', ascending=False)

    df['hs_rank_st'] = df.groupby('state')['hs_lower'].rank(method='average', ascending=True)
    df['vacancy_rank_st'] = df.groupby('state')['vacancy_rate'].rank(method='average', ascending=True)
    df['unemp_rank_st'] = df.groupby('state')['unemployment_rate'].rank(method='average', ascending=True)
    df['poverty_rank_st'] = df.groupby('state')['poverty_rate'].rank(method='average', ascending=True)
    df['med_rank_st'] = df.groupby('state')['med_inc_rate'].rank(method='average', ascending=False)
    df['est_rank_st'] = df.groupby('state')['est_chg'].rank(method='average', ascending=False)
    df['emp_rank_st'] = df.groupby('state')['emp_chg'].rank(method='average', ascending=False)

    df['avg_rank_st'] = df.iloc[:,-7:].mean(axis=1).round(1)
    df['pct_rank_st'] = df.groupby('state')['avg_rank'].rank(pct=True, method='average').round(3)*100
    df['st_rank'] = df.groupby('state')['avg_rank_st'].rank(method='average', ascending=False)

    df['counties'] = df.groupby('state')['fips'].transform('count')

    df.to_csv('../data/'+year+'-rankings.csv', index=False)