import paho.mqtt.client as mqtt
import requests
import pandas as pd
import sqlite3
import sys
from datetime import datetime

# The callback for when the client receives a CONNACK response from the server.
station = {}
station["EnergyReading"] = []
station["ChargeId"] = []
station["Time"] = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("World")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    curr_place = str(msg.payload).split('-')[1]
    curr_val = curr_place.split('|')[0].strip()
    chargeId = str(msg.payload).split('|')[1]
    updchargeId = chargeId.split("'")[0].strip()
    station["ChargeId"].append(updchargeId)
    #print(station["AIN0"])
    if(curr_val == '0'):
        table_name = "dataAIN0"
        curr_station = "AIN0"
    elif(curr_val == '1'):
        table_name = "dataAIN1"
        curr_station = "AIN1"
    elif (curr_val == '2'):
        table_name = "dataAIN2"
        curr_station = "AIN2"
    elif (curr_val == '3'):
        table_name = "dataAIN3"
        curr_station = "AIN3"
    elif (curr_val == '4'):
        table_name = "dataAIN4"
        curr_station = "AIN4"
    elif (curr_val == '5'):
        table_name = "dataAIN5"
        curr_station = "AIN5"
    elif (curr_val == '6'):
        table_name = "dataAIN6"
        curr_station = "AIN6"
    elif (curr_val == '7'):
        table_name = "dataAIN7"
        curr_station = "AIN7"
    else:
        table_name = "dataAIN0"
        curr_station = "AIN0"
    # curr_station = "AIN0"
    url_labjack_curr = "http://localhost:5000/labjackvalues/" + curr_station
    res = requests.get(url_labjack_curr)
    respdata = res.json()
    station["EnergyReading"].append(respdata)
    now = datetime.now()
    station["Time"].append(str(now))
    df_station = pd.DataFrame(station)
    conn = sqlite3.connect('energy.db')
    df_station.to_sql(table_name, conn, if_exists='append', index=False)
    pd.read_sql('select * from {0}'.format(table_name), conn)
    #print(df_station)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()