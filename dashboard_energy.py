import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import sqlite3
#from plotly.offline import init_notebook_mode, plot_mpl
from plotly.tools import mpl_to_plotly
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

#'backgroundColor': colors['background']
#'color': colors['text'],

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
    html.Button('Get Energy Table', id='button_neo',style={'color': '#D4AF37'})
])

@app.callback(Output("myGraph", "figure"),[Input("button_neo", "n_clicks")], [State("input_text", "value")])
def update_energy_table(n_clicks,value):
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM " + value)

    data = c.fetchall()

    conn.close()
    print(data)
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

if __name__ == '__main__':
    app.run_server(debug=True)