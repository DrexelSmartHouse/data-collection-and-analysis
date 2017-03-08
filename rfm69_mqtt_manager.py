#!/usr/bin/env python

"""
This is a simple mqtt client that manages the rfm69 network.
It does things like poll the sensors at a specified interval
and check when a device goes down.
"""
import paho.mqtt.client as mqtt
import time

# TODO replace with config file
server_ip = '192.168.1.2'
server_port = 1883
client_id = 'rfm69 manager'

# max number of seconds without sending a message to the broker
# This will ping the server at the interval defined below if no
# other communications occur
keep_alive = 60 

sweep_interval_s = 60 # time in seconds between each sweep

# callback functions

def on_connect(client, userdata, flags, rc):
    print('connected with result: ' + str(rc))

    # resubscribe whenever connecting or reconnecting
    client.subscribe("RFM69/+/log")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# helper functions

def scan(client, network_id):
    topic = 'RFM69/' + str(network_id) + '/requests'
    client.publish(topic, 'SCAN', 1)

def sweep(client, network_id):
    topic = 'RFM69/' + str(network_id) + '/requests'
    client.publish(topic, 'SWEEP', 1)

def main():

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
        scan(client, 0)
        sweep(client, 0)
        time.sleep(sweep_interval_s)


    # stop the thread
    client.loop_stop()


if __name__ == '__main__':
    main()
