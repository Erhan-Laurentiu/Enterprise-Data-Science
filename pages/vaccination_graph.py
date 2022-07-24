from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import sys
sys.path.append('../EnterpriseDataScienceProject/')
from constantdata import *

import dash
dash.__version__
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go


register_page(__name__)
 
df_input_large=pd.read_csv(PROCESSED_RELATIONAL_FINAL,sep=';')
# Get Rid of Empty Rows in DataSet
df_input_large = df_input_large.dropna(axis=0, subset=[FULLY_VACCINATED_KEY])

fig = go.Figure()


layout = html.Div([
    html.Label('Select Countries'),
    dcc.Dropdown(
        id='vaccination_country_drop_down',
        options = [ {'label': each,'value':each} for each in df_input_large['country'].unique()], 
        value = DEFAULT_COUNTRIES_LIST,
        multi=True,
        searchable=True,
        search_value='',
        placeholder='Select the country...',
        clearable=True
    ),

    html.Label('Select Timeline',style={"margin-top": "1vw"}),

    dcc.Dropdown(
    id='vaccination_time',
    options=[
        {'label': 'Timeline Fully Vaccinated', 'value': FULLY_VACCINATED_KEY},
        {'label': 'Timeline Fully Vaccinated Per Population', 'value': FULLY_VACCINATED_POP_KEY}
            ],
    value=FULLY_VACCINATED_KEY,
    searchable=False,
    multi=False
    ),

    dcc.Graph(
        figure=fig, 
        id='vaccination_main_window_slope',  
        style={'width':'99vw','height':'70vh'})

])


@callback(
    Output('vaccination_main_window_slope', 'figure'),
    [Input('vaccination_country_drop_down', 'value'),
    Input('vaccination_time', 'value')]
)
def update_figure(country_list, timeline_type):

    if FULLY_VACCINATED_POP_KEY in timeline_type:
        my_yaxis={'type':"log",
               'title':'Fully Vaccinated Rate per Population (log-scale)'
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Fully Vaccinated Rate (log-scale)'
              }
    
    traces = []

    for each in country_list:

        df_plot=df_input_large[df_input_large['country']==each]
        df_plot=df_plot[['state','country',FULLY_VACCINATED_KEY,FULLY_VACCINATED_POP_KEY,'date']].groupby(['country','date']).agg(np.sum).reset_index()

        traces.append(dict(x=df_plot.date,
                                y=df_plot[timeline_type],
                                mode='markers+lines',
                                opacity=0.9,
                                ine_width=2,
                                marker_size=4,
                                name=each
                        )
                )

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
        title='Vaccination Rate Evolution of CoronaVirus'
    )}
