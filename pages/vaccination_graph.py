from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import sys
sys.path.append('../EnterpriseDataScienceProject/')
from paths import DEFAULT_COUNTRIES_LIST, POPULATION_PROCESSED_FILE_PATH, VACCINATION_POP_PROCESSED_FILE_PATH
from dataprocessmanager import processAllData


cachedList = DEFAULT_COUNTRIES_LIST

register_page(__name__)

df=pd.read_csv(POPULATION_PROCESSED_FILE_PATH, sep = ';')
supportedCountriesList = df['Country']
populationDict = dict(zip(supportedCountriesList, df['Population']))

df_plot=pd.read_csv(VACCINATION_POP_PROCESSED_FILE_PATH, sep = ';')

fig = go.Figure()

allCountryList=df_plot.columns[2:]

myOptions = []
for each in allCountryList:
    myOptions.append({'label' : each, 'value' : each})

layout = html.Div([
    html.Label('Select Countries'),
    dcc.Dropdown(
        id='vaccination_country_drop_down',
        options = supportedCountriesList, 
        value = cachedList, #whichare pre-selected
        multi=True,
        searchable=True,
        search_value='',
        placeholder='Select the country...',
        clearable=True
    ),
    dcc.Graph(
        figure=fig, 
        id='vaccination_main_window_slope',  
        style={'width':'99vw','height':'80vh'})

])


@callback(
    Output('vaccination_main_window_slope', 'figure'),
    [Input('vaccination_country_drop_down', 'value')]
)
def update_figure(country_list):
    traces = []

    global cachedList
    global df_plot

    for each in country_list:
        if not each in cachedList:
            cachedList = list( dict.fromkeys(country_list))
            print(cachedList)
            processAllData(cachedList)
            df_plot = pd.read_csv(VACCINATION_POP_PROCESSED_FILE_PATH, sep = ';')
            break

    for each in country_list:
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
            'title' : 'Vaccination Rate [%]',   
            'type'  : 'log',
            'range' : '[1.1,5.5]'
        },
        title='Vaccination Rate Evolution of CoronaVirus'
    )}
