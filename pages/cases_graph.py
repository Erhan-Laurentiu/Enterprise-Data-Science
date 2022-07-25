from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
sys.path.append('../EnterpriseDataScienceProject/')
from constantdata import *



register_page(__name__, path="/")


df_input_large=pd.read_csv(PROCESSED_RELATIONAL_FINAL_FILE_PATH, sep=';')

# Get Rid of Empty Rows in DataSet
df_input_large = df_input_large.dropna(axis=0, subset=[CASES_KEY])
supportedCountries =  df_input_large[COUNTRY_KEY].unique()
supportedCountries.sort()

fig = go.Figure()

layout = html.Div([
    html.Label('Select Countries'),
    dcc.Dropdown(
        id='cases_country_drop_down',
        options = supportedCountries, 
        value = DEFAULT_COUNTRIES_LIST, 
        multi=True,
        searchable=True,
        search_value='',
        placeholder='Select the country...',
        clearable=True
    ),
    
    html.Label('Select Timeline',style={"margin-top": "1vw"}),

    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Timeline Confirmed ', 'value': CASES_KEY},
        {'label': 'Timeline Confirmed Per Population', 'value': CASES_POP_KEY},
        {'label': 'Timeline Confirmed Filtered', 'value': CASES_FILTERED_KEY},
        {'label': 'Timeline Doubling Rate', 'value': CASES_DR_KEY},
        {'label': 'Timeline Doubling Rate Filtered', 'value': CASES_FILTERED_DR_KEY},
            ],
    value=CASES_KEY,
    searchable=False,
    multi=False
    ),

    dcc.Graph(
        figure=fig, 
        id='cases_main_window_slope',  
        style={'width':'99vw','height':'70vh'})
])


@callback(
    Output('cases_main_window_slope', 'figure'),
    [Input('cases_country_drop_down', 'value'),
    Input('doubling_time', 'value')]
)
def update_figure(country_list, show_doubling):

    if 'doubling_rate' in show_doubling:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days (larger numbers are better #stayathome)'
              }
    else:
        my_yaxis={'type': "log",
                  'title':'Cases of CoronaVirus (log-scale)'
              }

    traces = []
    
    for each in country_list:

        df_plot=df_input_large[df_input_large[COUNTRY_KEY]==each]

        if show_doubling=='doubling_rate_filtered':
            df_plot=df_plot[[STATE_KEY,COUNTRY_KEY,CASES_KEY,CASES_POP_KEY,CASES_FILTERED_KEY,CASES_DR_KEY,CASES_FILTERED_DR_KEY,DATE_KEY]].groupby([COUNTRY_KEY,DATE_KEY]).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[[STATE_KEY,COUNTRY_KEY,CASES_KEY,CASES_POP_KEY,CASES_FILTERED_KEY,CASES_DR_KEY,CASES_FILTERED_DR_KEY,DATE_KEY]].groupby([COUNTRY_KEY,DATE_KEY]).agg(np.sum).reset_index()

        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                opacity=0.9,
                                ine_width=2,
                                marker_size=4,
                                name=each))

    return {
        'data' : traces,
        'layout'  : dict(
        xaxis={
            'title'     : 'Time',
            'tickangle' : 45,
            'nTicks'    : 20,
            'tickfont'  : dict(size=14,color='#7f7f7f')
        },
        yaxis=my_yaxis,
        title='Cases Evolution of CoronaVirus'
    )}
