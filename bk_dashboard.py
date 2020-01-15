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

fig1 = plt.figure()
ax = fig1.add_subplot(1, 1, 1)
xs = []
ys = []

xs.append(0)
ys.append(0)
res = requests.get(url_labjack)
respdata = res.json()
print(respdata)
xs.append(xs[-1] + 1)
ys.append(respdata[0])

for i in range(19):
    xs.append(xs[-1] + 1)
    ys.append(respdata[0])

# Add x and y to lists
# xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
# ys.append(temp_c)

# Limit x and y lists to 20 items
xs = xs[-20:]
ys = ys[-20:]

# Draw x and y lists
ax.clear()
ax.plot(xs, ys)

# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('Real time values of LabJack Controller')
plt.ylabel('Power Measured')
#ani = animation.FuncAnimation(fig1, animate, fargs=(xs, ys), interval=1000)
plt.show()
plotly_fig_live = mpl_to_plotly(fig1)

app.layout = html.Div(style={'textAlign': 'center'},children=[
    html.Img(src=app.get_asset_url('emden_leer.png'),style={
                'height': '50%',
                'width': '50%'
            }),
    html.H1(children='PPS03 Energy Dashboard'),

    # html.Div(id="energy-table",children='''
    #     Energy Dashboard for PPS Systems
    # '''),

    html.Div([dcc.Graph(id='myGraph', figure=plotly_fig)],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Br(),
    dcc.Input(
            id="input_text".format("text"),
            type="text",
            placeholder="input type text".format("text"),
        ),
    html.Button('Get Energy Table', id='button_neo',style={'color': '#D4AF37'}),
    html.H4(id='live-update-text'),
    html.Div([dcc.Graph(id='live-update-graph',animate=True)],style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    # dcc.Graph(id='live-update-graph',animate=True,style={'width':1000}),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # 2000 milliseconds = 2 seconds
        n_intervals=0
    )
])

@app.callback(Output("myGraph", "figure"),[Input("button_neo", "n_clicks")], [State("input_text", "value")])
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

@app.callback(Output('live-update-graph','figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    res = requests.get(url_labjack)
    respdata = res.json()
    print(respdata)
    #print(type(respdata))
    global xs
    global ys
    xs.append(n + 1)
    ys.append(respdata[0])
    print(xs)
    print(ys)
    xs = xs[-20:]
    ys = ys[-20:]
    fig = go.Figure(
        data = [go.Scatter(
        # x = list(range(len(data))),
        x = list(xs),
        y = list(ys),
        mode='lines+markers'
        )])

    return fig

    # data = plotly.graph_objs.Scatter(
    #     x=xs,
    #     y=ys,
    #     name='Scatter',
    #     mode='lines+markers'
    # )
    #
    # return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(xs), max(xs)]),
    #                                             yaxis=dict(range=[min(ys), max(ys)]), )}

    # global xs
    # global ys
    # xs.append(n + 1)
    # ys.append(respdata[0])
    # print(xs)
    # print(ys)
    #
    # # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]
    #
    # # Draw x and y lists
    # ax.clear()
    # ax.plot(xs, ys)
    #
    # # Format plot
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.title('Real time values of LabJack Controller')
    # plt.ylabel('Power Measured')
    # # ani = animation.FuncAnimation(fig1, animate, fargs=(xs, ys), interval=1000)
    # plt.show()
    # plotly_fig_live = mpl_to_plotly(fig1)
    # return plotly_fig_live


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_layout(n):
    #return 'Labjack Values are {}'.format(data)
    return 'Live updating successfull for {} refreshes'.format(n)



if __name__ == '__main__':
    app.run_server(debug=True)
