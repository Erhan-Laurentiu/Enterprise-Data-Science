from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import sys
sys.path.append('../EnterpriseDataScienceProject/')
from paths import *
from dataprocessmanager import processAllData
import pandas as pd
import numpy as np

import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import plotly.graph_objects as go

CONFIRMED = 'confirmed'
CONFIRMED_POP = 'confirmed_percentage'
CONFIRMED_FILTERED = 'confirmed_filtered'
CONFIRMED_DR= 'confirmed_DR'
CONFIRMED_FILTERED_DR = 'confirmed_filtered_DR'
print(os.getcwd())
df_input_large=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')


timelineToCSVMap = {CONFIRMED: CASES_PROCESSED_FILE_PATH, 
                    CONFIRMED_POP: CASES_POP_PROCESSED_FILE_PATH,
                    CONFIRMED_FILTERED: CASES_FILTERED_PROCESSED_FILE_PATH,
                    CONFIRMED_DR: CASES_DR_PROCESSED_FILE_PATH,
                    CONFIRMED_FILTERED_DR: CASES_FILTERED_DR_PROCESSED_FILE_PATH
                    }


cachedList = DEFAULT_COUNTRIES_LIST
# timelineValue = 'confirmed'
prevTimelineValue =''

register_page(__name__, path="/")

df=pd.read_csv(POPULATION_PROCESSED_FILE_PATH, sep = ';')
supportedCountriesList = df['Country']
populationDict = dict(zip(supportedCountriesList, df['Population']))

df_plot=pd.read_csv(CASES_PROCESSED_FILE_PATH, sep = ';')

fig = go.Figure()

allCountryList=df_plot.columns[2:]

myOptions = []
for each in allCountryList:
    myOptions.append({'label' : each, 'value' : each})

layout = html.Div([
    html.Label('Select Countries'),
    dcc.Dropdown(
        id='cases_country_drop_down',
        options = supportedCountriesList, 
        value = cachedList, #whichare pre-selected
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
        {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
        {'label': 'Timeline Confirmed Percentage', 'value': 'confirmed_percentage'},
        {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
        {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
        {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
    ],
    value='confirmed',
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
def update_figure(country_list, timelineValue):
    global cachedList
    global df_plot

    newCountryList = list( dict.fromkeys(country_list))
    traces = []
    
    if cachedList != newCountryList:
        cachedList = newCountryList
        print(cachedList)
        if timelineValue == CONFIRMED or timelineValue == CONFIRMED_POP:
            processAllData(cachedList)
        else:
            processAllData(cachedList, True)
    else:
        if timelineValue == CONFIRMED or timelineValue == CONFIRMED_POP:
            processAllData(cachedList)
        else:
            processAllData(cachedList, True)   
        
    df_plot = pd.read_csv(timelineToCSVMap[timelineValue], sep = ';')

    for each in cachedList:
        traces.append(dict(x=df_plot.date,
                            y=df_plot[each],
                            mode='markers+lines',
                            opacity=0.9,
                            line_width=2,
                            marker_size=4,
                            name=each))

    return {'data' : traces, 'layout'  : dict(
        xaxis={
            'title'     : 'Time',
            'tickangle' : 45,
            'nTicks'    : 20,
            'tickfont'  : dict(size=14,color='#7f7f7f')
        },
        yaxis={
            'title' : 'Cases of CoronaVirus',
            'type'  : 'log',
            'range' : '[1.1,5.5]'
        },
        title='Cases Evolution of CoronaVirus'
    )}
