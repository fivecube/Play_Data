import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output, State
import io
import base64
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import json
from json_parser import get_latest_dataframe
import datetime
from dash.exceptions import PreventUpdate
from clustering import cluster_function
from boxplot import get_box_stats

app = dash.Dash(__name__)
app.title = "Play-Data"


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    # available_indicators = df['Indicator Name'].unique()
    return html.Div([
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure={
                'data': [
                    dict(
                        x=df[df['continent'] == i]['gdp per capita'],
                        y=df[df['continent'] == i]['life expectancy'],
                        text=df[df['continent'] == i]['country'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df.continent.unique()
                ],
                'layout': dict(
                    xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                    yaxis={'title': 'Life Expectancy'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
    ])


app.layout = html.Div([
    html.Div([
        html.H2("Play-Data : Data Visualization and Research Tool"),
        html.Img(src="assets/favicon.ico")
    ], className="banner"),
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Upload CSV data manually', value='tab-1'),
        dcc.Tab(label='Use existing API from the Internet on Hot Topics', value='tab-3'),
        dcc.Tab(label='Statistics of the Data', value='tab-4'),
        dcc.Tab(label='Correlation of the Attributes', value='tab-2'),
        dcc.Tab(label='Clustering in 2 Dimension', value='tab-5')
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='tabs-content-props')
])


@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-data-upload'),
            ])
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Dropdown(
                id='demo-dropdown',
                options=[
                    {'label': 'Coronavirus World Data', 'value': 'COW'},
                    {'label': 'Coronavirus India Data', 'value': 'COI'},
                ], placeholder="Select an API"
            ),
            html.Div(id='dd-output-container')
        ])
    elif tab == 'tab-5':
        return html.Div([
            dcc.Dropdown(
                id='demo-dropdown_2',
                options=[
                    {'label': '2 Clusters', 'value': '2'},
                    {'label': '3 Clusters', 'value': '3'},
                ], placeholder="Select no of Clusters"
            ),
            html.Div(id='dd-output-container_2')
        ])
    elif tab == 'tab-4':
        return html.Div([
            dcc.Dropdown(
                id='demo-dropdown_3',
                options=[
                    {'label': 'Show Statistics', 'value': '2'},
                    {'label': 'Hide Statistics', 'value': '3'},
                ], placeholder="Choose"
            ),
            html.Div(id='dd-output-container_3')
        ])
    elif tab == 'tab-2':
        df = pd.read_csv('/Users/mohitsinghchouhan/Downloads/country_indicators.csv')
        available_indicators = df['Indicator Name'].unique()
        return html.Div([html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Fertility rate, total (births per woman)'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ],
                    style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Life expectancy at birth, total (years)'
                    ),
                    dcc.RadioItems(
                        id='yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ]),

            dcc.Graph(id='indicator-graphic'),

            dcc.Slider(
                id='year--slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()},
                step=None
            )
        ])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    df = pd.read_csv('/Users/mohitsinghchouhan/Downloads/country_indicators.csv')
    dff = df[df['Year'] == year_value]

    return {
        'data': [dict(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def api_coronavirus_world():
    df = get_latest_dataframe("coronavirus_world")
    fig = px.scatter(df, x="tests_per_1m_population", y="cases", color="deaths",
                     size='active_cases', hover_data=['country_name'])
    return html.Div([
        html.Div(["Last updated on " + str(datetime.datetime.now())]),
        html.Div([
            dcc.Graph(figure=fig,
                      id="graph_close",
                      )
        ], className="six columns"), ])


def api_coronavirus_india():
    df = get_latest_dataframe("coronavirus_india")
    fig = px.scatter(df, x="active", y="deaths", color="recovered",
                     size='confirmed', hover_data=['name'])
    return html.Div([
        html.Div(["Last updated on " + str(datetime.datetime.now())]),
        html.Div([
            dcc.Graph(figure=fig,
                      id="graph_close",
                      )
        ], className="six columns"), ])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value'),])
def update_output(value):
    if value is None:
        raise PreventUpdate
    elif value == "COW":
        return api_coronavirus_world()
    elif value == "COI":
        return api_coronavirus_india()
    else:
        raise PreventUpdate


def box_plot_statistics():
    fig = get_box_stats()
    return html.Div([
        dcc.Graph(figure=fig,
                  id="graph_close",
                  )
    ], className="six columns")


@app.callback(
    dash.dependencies.Output('dd-output-container_3', 'children'),
    [dash.dependencies.Input('demo-dropdown_3', 'value'),])
def update_output_2(value):
    if value is None:
        raise PreventUpdate
    elif value == "2":
        return box_plot_statistics()
    elif value == "3":
        raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    dash.dependencies.Output('dd-output-container_2', 'children'),
    [dash.dependencies.Input('demo-dropdown_2', 'value'),])
def update_fig(value):
    return cluster_function(value)


app.config['suppress_callback_exceptions'] = True
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
