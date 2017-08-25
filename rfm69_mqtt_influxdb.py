#!/usr/bin/env python

"""
This is a simple mqtt client that manages the rfm69 network.
It does things like poll the sensors at a specified interval
and check when a device goes down.

Please configure your database information.
This information has been redacted from the file due to privacy concerns.

The MQTT message will be parsed into an array with indices in this format:
('Time', 'Network ID', 'Node ID', 'Sensor Type', 'Sensor Value')

"""

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import time
import signal, sys
import csv
import datetime
from config_file import get_conf

# conf file file default path
conf_file_path = 'dshPython.conf'
dataFileName = 'dshData.csv'
startTime = time.clock()

# callback functions

def on_connect(client, userdata, flags, rc):
    print('connected with result: ' + str(rc))

    # resubscribe whenever connecting or reconnecting
    client.subscribe("RFM69/0/+/+")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    spTopic = msg.topic.split("/")
    msg_json = [
        {
            "measurement": "Grafana",
            "tags": {
                "NodeID": spTopic[3],
		"SensorType": spTopic[4]
            },
            "fields": {
                "NetworkID": spTopic[2],
		"SensorValue": float(msg.payload)
            }
        }
    ]
    clientdb = InfluxDBClient(hostDB, portDB, userDB, pwDB, dbName)
    clientdb.write_points(msg_json)
    
# helper function
#request: either "SCAN" or "SWEEP"
def send_request(request,client,network_id):
    topic = 'RFM69/' + str(network_id) + '/requests'
    client.publish(topic, request, 1)
    

# signal handler for ctrl-c
def signal_handler(signal, frame):
    print("\nEnding Program.....")
    sys.exit(0)

def main():

    signal.signal(signal.SIGINT, signal_handler)

    # get consts from the config file
    try:
        conf_file = open(conf_file_path, 'r')
        config = get_conf(conf_file)
        conf_file.close()
    except:
        print('Bad config file, ending')
        sys.exit(0)

    #reads config file and returns relevant variables
    #TODO default values in case these are ommited from the config

    server_ip = config['server ip']
    server_port = config['server port']
    client_id = config['client id']
    keep_alive = config['keep alive'] # max number of seconds without sending a message to the broker
    sweep_interval_s = config['interval']
    hostDB = config['host']
    portDB = config['port']
    userDB = config['user']
    pwDB = config['password']
    dbName = config['databasename']

    client = mqtt.Client(client_id)
    
    # set the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # start the connection
    client.connect(server_ip, server_port, keep_alive)

    # start the thread for processing incoming data
    client.loop_start()

    # main loop
    while True:
        send_request('SCAN',client,0)
        send_request('SWEEP',client,0)
        time.sleep(sweep_interval_s)
    # stop the thread
    client.loop_stop()

if __name__ == '__main__':
    main()
