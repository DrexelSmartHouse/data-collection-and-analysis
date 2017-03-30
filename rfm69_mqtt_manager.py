#!/usr/bin/env python

"""
This is a simple mqtt client that manages the rfm69 network.
It does things like poll the sensors at a specified interval
and check when a device goes down.
"""
import paho.mqtt.client as mqtt
import time

#config file reading function
def config_file(filename):
    
    file = open(filename,"r")
    dictionary={}
    for line in file:
        if ":" in line:
            index = line.index(':')
            dictionary.update({line[:index]: line[(index+1): -1]})
    server_ip = dictionary['server_ip']
    server_port = dictionary['server_port']
    client_id = dictionary['client_id']
    interval = dictionary['interval']
    return(server_ip, server_port, client_id, interval)
 
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

    #default config filename set to config_file.txt
    filename=input("Enter Filename: ") or "config_file.txt"
    #reads config file and returns relevant variables
    (server_ip, server_port, client_id, interval) = config_file(filename)
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
