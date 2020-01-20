import paho.mqtt.client as mqtt
import requests

# The callback for when the client receives a CONNACK response from the server.
station = {}
station["AIN0"] = []
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("World")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    curr_station = "AIN0"
    url_labjack_curr = "http://localhost:5000/labjackvalues/" + curr_station
    res = requests.get(url_labjack_curr)
    respdata = res.json()
    station["AIN0"].append(respdata)
    print(station["AIN0"])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()