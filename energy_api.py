import sqlite3
import matplotlib.pyplot as plt
import sys
from flask import Flask
from flask import request
from flask import json
from flask_cors import CORS
from labjack import ljm
import math
import time
import os

app = Flask(__name__,static_url_path='')
CORS(app)

@app.route('/')
def root():
    return 'hello!'

@app.route('/servelivedata')
def live_data_server():
    return app.send_static_file('livedata.html')

@app.route('/servelivedata/<page>')
def live_data_renderpage(page):
    return app.send_static_file(page)

@app.route('/labjackvalues')
def labjack_values():
    # Open first found LabJack
    handle = ljm.openS("ANY", "ANY", "ANY")

    # Call eReadName to read the serial number from the LabJack.
    name = "SERIAL_NUMBER"
    result = ljm.eReadName(handle, name)

    print("\neReadName result: ")
    print("    %s = %f" % (name, result))
    numFrames = 4
    # names = ["SERIAL_NUMBER", "PRODUCT_ID", "FIRMWARE_VERSION"]
    names = ['AIN0', 'AIN1', 'AIN2', 'AIN3']
    results = ljm.eReadNames(handle, numFrames, names)

    print("\neReadNames results: ")
    for i in range(numFrames):
        results[i] = (abs(results[i]) / 0.1) * 9
        print("Measured Power of - %s, value : %f" % (names[i], results[i]))

    return json.dumps(results)

@app.route('/labjackvalues/<idx>')
def get_labjack_value(idx):
    # Open first found LabJack
    handle = ljm.openS("ANY", "ANY", "ANY")
    print("\neFetching results for the station: {}".format(idx))
    results = (abs(ljm.eReadName(handle, idx)) / 0.1) * 9

    print("\neReadNames results: {}".format(results))

    return json.dumps(results)


@app.route('/getordnungdata/<table>')
def ordnung_data(table):
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM " + table)

    data = c.fetchall()
    return json.dumps(data)

@app.route('/getordnungdata/<table>/<processtime>')
def processtime_data(table,processtime):
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM " + table + " WHERE processTime = "+ processtime)

    data = c.fetchall()
    return json.dumps(data)

@app.route('/compareordnungdata/<table>/<processtime>/<avgval>')
def compare_processtime_data(table,processtime,avgval):
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM " + table + " WHERE processTime = "+ processtime)

    data = c.fetchall()

    for row in data:
        std_avg_val = row[2]

    if float(avgval) > std_avg_val:
        return 'Process taking longer time than usual when compared to the expected result!'
    else:
        return json.dumps(data)

def run_query(table):
    conn = sqlite3.connect('energy.db')

    c = conn.cursor()

    c.execute("SELECT processTime,energyMin_kW,energyAve_kW,energyMax_kW FROM "+ table)

    data = c.fetchall()

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

    plt.xlabel('Process Time')
    plt.ylabel('Energy Consumption Signal')
    plt.title('Energy Database Overview')
    for t in totalArr:
        plt.plot(processArr, t, color=cr[rowcolor], label=tr[rowcolor])
        plt.legend(loc='lower left')
        rowcolor += 1

    plt.show()

if __name__ == "__main__":
    table_name = sys.argv[1] if len(sys.argv) > 1  else "dataRM"
    run_query(table_name)


