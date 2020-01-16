import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sqlite3
#from plotly.offline import init_notebook_mode, plot_mpl
import plotly
from plotly.tools import mpl_to_plotly
import requests
#from Labjack_reader import retrieve_analogvalues
import plotly.graph_objs as go
from collections import deque
import matplotlib.animation as animation

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt


url_labjack = "http://localhost:5000/labjackvalues"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

X = deque(maxlen=10)
X.append(1)
Y = deque(maxlen=10)
Y.append(1)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

conn = sqlite3.connect('energy.db')

c = conn.cursor()

c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM dataRM")

data = c.fetchall()
conn.close()
print(data)
processArr = []
minArr = []
avgArr = []
maxArr = []
totalArr = [minArr, avgArr, maxArr]
cr = ['r', 'b', 'g', 'y', 'p']
tr= ['energyMin_kW','energyAve_kW','energyMax_kW']
rowcolor = 0

for row in data:
    processArr.append(row[0])
    minArr.append(row[1])
    avgArr.append(row[2])
    maxArr.append(row[3])

fig = plt.figure()
plt.xlabel('Process Time')
plt.ylabel('Energy Consumption Signal')
plt.title('Energy Database Overview')
for t in totalArr:
    plt.plot(processArr, t, color=cr[rowcolor], label=tr[rowcolor])
    plt.legend(loc='lower left')
    rowcolor += 1

plotly_fig = mpl_to_plotly(fig)
#plt.show()

app.layout = html.Div(style={'textAlign': 'center'},children=[
    html.Img(src=app.get_asset_url('emden_leer.png'),style={
                'height': '50%',
                'width': '50%'
            }),
    html.H1(children='PPS03 Energy Dashboard'),

    html.Div([
    dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': 'dataRM', 'value': 'dataRM'},
                {'label': 'dataQC', 'value': 'dataQC'},
                {'label': 'dataRM_WS1', 'value': 'dataRM_WS1'},
                {'label': 'dataRM_WS3', 'value': 'dataRM_WS3'},
                {'label': 'dataRM_WS4', 'value': 'dataRM_WS4'},
                {'label': 'dataWS1_WS2', 'value': 'dataWS1_WS2'},
                {'label': 'dataWS3_WS4', 'value': 'dataWS3_WS4'},
                {'label': 'dataWS4_WS1', 'value': 'dataWS4_WS1'},
                {'label': 'dataWS2_QR', 'value': 'dataWS2_QR'},
                {'label': 'dataWS4_QR', 'value': 'dataWS4_QR'},
                {'label': 'dataWS1_QR', 'value': 'dataWS1_QR'},
                {'label': 'dataWS1W', 'value': 'dataWS1W'},
                {'label': 'dataWS2W', 'value': 'dataWS2W'},
                {'label': 'dataWS3R', 'value': 'dataWS3R'},
                {'label': 'dataWS4R', 'value': 'dataWS4R'},
                {'label': 'dataWS4B', 'value': 'dataWS4B'},
                {'label': 'dataWS1B', 'value': 'dataWS1B'}
            ],
            value='dataRM',
            style={'height': '30px', 'width': '200px'}
        )
    ],style={'display': 'inline-block','vertical-align': 'middle'}),

    html.Div([dcc.Graph(id='myGraph', figure=plotly_fig)],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Br(),
    html.H4(id='live-update-text'),
    # html.Div([dcc.Graph(id='live-update-graph',animate=True)],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        html.Iframe(id='iframe-livedata', src = 'http://localhost:5000/servelivedata', height = 600, width = 600)
    ],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # 2000 milliseconds = 2 seconds
        n_intervals=0
    )
])

@app.callback(Output("myGraph", "figure"),[Input('demo-dropdown', 'value')], [State("demo-dropdown", "value")])
def update_energy_table(n_clicks,value):
    if(value == None):
        value = "dataRM"
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM " + value)

    data = c.fetchall()

    conn.close()
    print(data)
    #retrieve_analogvalues()
    processArr = []
    minArr = []
    avgArr = []
    maxArr = []
    totalArr = [minArr, avgArr, maxArr]
    cr = ['r', 'b', 'g', 'y', 'p']
    tr = ['energyMin_kW', 'energyAve_kW', 'energyMax_kW']
    rowcolor = 0

    for row in data:
        processArr.append(row[0])
        minArr.append(row[1])
        avgArr.append(row[2])
        maxArr.append(row[3])

    fig = plt.figure()
    plt.xlabel('Process Time')
    plt.ylabel('Energy Consumption Signal')
    plt.title('Energy Database Overview')
    for t in totalArr:
        plt.plot(processArr, t, color=cr[rowcolor], label=tr[rowcolor])
        plt.legend(loc='lower left')
        rowcolor += 1

    plotly_fig = mpl_to_plotly(fig)
    return plotly_fig


    # plt.show()


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    #return 'Labjack Values are {}'.format(data)
    return 'Live updating successfull for {} refreshes'.format(n)



if __name__ == '__main__':
    app.run_server(debug=True)
