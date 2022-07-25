from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
sys.path.append('../EnterpriseDataScienceProject/')
from constantdata import *



register_page(__name__)


df_input_large=pd.read_csv(SIR_FINAL_FILE_PATH,sep=';')

column_headers = list(df_input_large.columns.values)
column_headers = list(filter(lambda k: '_ydata_opt1' in k, column_headers))
supportedCountries = list({x.replace('_ydata_opt1', '') for x in column_headers})
supportedCountries.sort()

fig = go.Figure()

layout = html.Div([
    html.Label('Select Countries'),
    dcc.Dropdown(
        id='sir_country_drop_down',
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
    id='sir_time',
    options=[
        {'label': 'Cumulative Fitted Line ', 'value': 'opt1'},
        {'label': 'Day to Day Difference', 'value': 'opt2'}
            ],
    value='opt2',
    searchable=False,
    multi=False
    ),

    dcc.Graph(
        figure=fig,
        id='sir_main_window_slope',
        style={'width':'99vw','height':'70vh'})
])


@callback(
    Output('sir_main_window_slope', 'figure'),
    [Input('sir_country_drop_down', 'value'),
    Input('sir_time', 'value')]
)
def update_figure(country_list, timeline_type):

    # if DEATHS_POP_KEY in timeline_type:
    my_yaxis={'type':"log",
               'title':'New Population Infected'
              }
    # else:
        # my_yaxis={'type':"log",
                #   'title':'Deaths of CoronaVirus (log-scale)'
            #   }
    
    traces = []


    x_data = df_input_large['t']

    for each in country_list:
        if timeline_type == 'opt1':
            y_data1 = df_input_large[each+'_ydata_opt1']
            y_data2 = np.cumsum(df_input_large[each+'_fitted_opt1'])
        else:
            y_data1 = np.ediff1d(df_input_large[each+'_ydata_opt2'],  to_begin=df_input_large[each+'_ydata_opt2'][1]-df_input_large[each+'_ydata_opt2'][0])
            y_data2 = df_input_large[each+'_fitted_opt2']


        traces.append(dict(x=x_data,
                                y=y_data1,
                                mode='markers',
                                opacity=0.9,
                                ine_width=2,
                                marker_size=4,
                                name=each))

        traces.append(dict(x=x_data,
                        y=y_data2,
                        mode='markers',
                        opacity=0.9,
                        ine_width=2,
                        marker_size=4,
                        name=each+' Fitted Model'))

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
        title='SIR'
    )}
