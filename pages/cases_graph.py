from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import py
import plotly.graph_objects as go

import sys

sys.path.append('../EnterpriseDataScienceProject/')
from paths import POPULATION_PROCESSED_FILE_PATH, CASES_POP_PROCESSED_FILE_PATH, DEFAULT_COUNTRIES_LIST
# from main import cachedCountriesList
from dataprocessmanager import processAllData

sys.path.append('../EnterpriseDataScienceProject/ui/')

cachedList =DEFAULT_COUNTRIES_LIST

register_page(__name__, path="/")

df=pd.read_csv(POPULATION_PROCESSED_FILE_PATH, sep = ';')
supportedCountriesList = df['Country']
populationDict = dict(zip(supportedCountriesList, df['Population']))

df_plot=pd.read_csv(CASES_POP_PROCESSED_FILE_PATH, sep = ';')

fig = go.Figure()
# fig.add_trace(go.Scatter(x=df_plot.date,
#                         y=df_plot['Moldova'],
#                         name='Moldova',
#                          mode='markers+lines',
#                         opacity=0.9,
#                         line_width=2,
#                         marker_size=4
#                         ))
# fig.add_trace(go.Scatter(x=df_plot.date,
# y=df_plot['Romania']))
# fig.add_trace(go.Scatter(x=df_plot.date,
# y=df_plot['Spain']))
fig.update_layout(
    xaxis_title='Time',
    yaxis_title='Cases of CoronaVirus'
    #width height etc
)

fig.update_layout(xaxis_rangeslider_visible=True)


allCountryList=df_plot.columns[2:]
# print(allCountryList)
myOptions = []
# print(type(myOptions))
for each in allCountryList:
    myOptions.append({'label' : each, 'value' : each})

# layout = html.Div(
#     [
#         html.P("Medals included:"),
#         dcc.Checklist(
#             id="heatmaps-medals",
#             options=[{"label": x, "value": x} for x in df.columns],
#             value=df.columns.tolist(),
#         ),
#         dcc.Graph(id="heatmaps-graph"),
#     ]
# )
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
    dcc.Graph(figure=fig, id='cases_main_window_slope',  style={'width':'95vw','height':'85vh'})

])


@callback(
    Output('cases_main_window_slope', 'figure'),
    [Input('cases_country_drop_down', 'value')]
)
def update_figure(country_list):
    traces = []
    # print(cachedMap)
    global cachedList
    global df_plot

    for each in country_list:
        if not each in cachedList:
            cachedList = list( dict.fromkeys(country_list))
            print(cachedList)
            processAllData(cachedList)
            df_plot = pd.read_csv(CASES_POP_PROCESSED_FILE_PATH, sep = ';')
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
            'title' : 'Cases of CoronaVirus',
            'type'  : 'log',
            'range' : '[1.1,5.5]'
        }        
    )}
