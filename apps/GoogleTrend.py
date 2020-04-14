import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objects as go
from plotly.offline import plot
from app import app
from apps import sidebar


#fct
mot_base = ['coronavirus','ubereats','pornhub','nintendo switch','netflix',"bac"]
def google_trend_graph(w):

    pytrend = TrendReq()
    df = pd.DataFrame()
    for i in w:
        pytrend.build_payload(kw_list=[i], timeframe='today 3-m')
        interest_w = pytrend.interest_over_time() 
        df[i] = interest_w[i]

    fig_trend_w = go.Figure()
    for i in range(len(w)):
        fig_trend_w.add_trace(go.Scatter(x=df.index, y=df.iloc[:,i], mode='lines', name=w[i]))
    
    fig_trend_w.update_layout(
        font=dict(
            family='Montserrat',
            size=15,
            color='rgb(87, 88, 90)'
            ),
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=3,
            ticks='outside'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            showline=False,
            showticklabels=True,
        ),
        showlegend=True,
        plot_bgcolor='white'
    )
                    
    return fig_trend_w
fig = google_trend_graph(mot_base)

#FIGURE SLIDE COMPARAIRAISON

layout = html.Div([
    sidebar.sidebar,
    html.Div(id='main',children = [
        dbc.Row(
            [
                html.Button(id='btnOpen',className='openbtn',children='☰',n_clicks=1),
                html.Div(style={'width':'50em'}),
                html.H4('GOOGLE RESEARCH INTERESTS',style={'text-transform':'uppercase','margin-top':'20px','letter-spacing': '3px','color':'rgb(87, 88, 90)','font-weight':'bolder'})
            ],style={'box-shadow':'0 5px 10px 0 rgba(50,50,50,.33)'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.A([html.Div('Internet Trend'),html.Div(className='encoche',style={'top':'52px','margin-top':'0px'})],href ='/GoogleTrend',className = "sousOngletActived")
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col( 
                                    dbc.Input(debounce=True,
                                    id='search',
                                    type='search',
                                    placeholder='Search...',
                                    style={
                                        'width':'100%',
                                    }
                                ),width = 9,style={'padding-right':'0px'}),
                                dbc.Col(
                                    dbc.Button(id='BtnSearch',children=html.Img(src ='https://img.icons8.com/ios/500/search--v1.png',style = {'width':'16px','height':'16px'}),color='primary',className='ml-2')
                                ,width = 3,style={'padding-left':'0px'})
                            ],style={
                                'margin-top':'4em',
                            }
                        ),
                        dbc.Row(
                           [ dbc.Label('Choose or add words',style={'color':'white','margin-left':'1em'}),
                            html.Div("",id='msgError',style={'color':'red','text-transform':'uppercase'}),
                            html.Div(style={'margin-left':'2em'},id='containerCheckList',children = 
                                dbc.Checklist(id='checklist',
                                options =
                                    [{'label':el,'value':el} for el in mot_base],
                                style={'color':'white'},
                                value = [mot_base[2],mot_base[4]]
                            ),
                            ),
                            html.Div(id='test'),
                            ]
                        )
                    ],className ='sideBarOnglet',width = 2),
                dbc.Col([
                    dbc.Row("dada",style={'color':'white','margin-left':'2em','margin-top':'1em'}),
                    dcc.Graph(id='trend',figure=fig,style={'height':'850px'}),
                        
                ],style={'padding':'0px'},width = 10),
                dbc.Row(id='test')
            ]
        )
        
    ],style={'padding-top':'0px'})
])

#CALLBACKS
@app.callback(
    Output('trend','figure'),
    [Input('checklist','value')]
)
def change_search(elements):
    return google_trend_graph(elements)
@app.callback(
    [Output('containerCheckList','children'),
    Output('search','value')],
    [Input('BtnSearch','n_clicks')],
    [State('search','value'),
    State('checklist','options'),
    State('checklist','value')]
)
def update_output(clicks,value,options,checked):
    if value is not None:
        cases = [el['label'] for el in options]
        cases = cases + [value]
        return dbc.Checklist(id='checklist',
            options =
                [{'label':el,'value':el} for el in cases],
            style={'color':'white'},
            value = [el for el in checked]),''
    