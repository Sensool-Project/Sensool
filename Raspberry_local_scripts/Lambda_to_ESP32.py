#!/usr/bin/env python3
#-- coding: utf-8 --
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json
import RPi.GPIO as GPIO
from bluetooth import *
from datetime import datetime
import time
import calendar
import sys

def servoCallback(client, userdata, message):
    trigger=message.payload

    if trigger:
        addr = "24:6F:28:78:FC:A6"
        #uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        #service_matches = find_service( uuid = uuid, address = addr )
        service_matches = find_service(address = addr)

        buf_size = 1024;

        if len(service_matches) == 0:
            print("couldn't find the SampleServer service =(")
            sys.exit(0)

        for s in range(len(service_matches)):
            print("\nservice_matches: [" + str(s) + "]:")
            print(service_matches[s])
            
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        port=1
        print("connecting to \"%s\" on %s, port %s" % (name, host, port))

        # Create the client socket
        sock=BluetoothSocket(RFCOMM)
        sock.connect((host, port))

        print("connected")
        
        print(trigger)
        if (trigger == "True"):
            hello = 1
        else:
            hello = 0
        print(hello)
        print(str(hello))
        sock.send(str(hello))
    
    return trigger
        
    sock.close()
    #print(trigger)
    #jerome=json.loads(trigger, "utf-8")
    #humidity = jerome["humidity_DHT11"]
    
    #MAC address of ESP32
rootCAPath = "./root-ca-cert.pem"
certificatePath = "25b74c4b40.cert.pem"
privateKeyPath = "25b74c4b40.private.key"
host = "airh6d2ooyyep-ats.iot.us-east-2.amazonaws.com"
port = 8883
clientId = "servo1"
topic = "servo/trigger"

servo_MQTTClient = AWSIoTMQTTClient(clientId)
servo_MQTTClient.configureEndpoint(host, port)
servo_MQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

servo_MQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
servo_MQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
servo_MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
servo_MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
servo_MQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

servo_MQTTClient.connect()

servo_MQTTClient.subscribe(topic, 1, servoCallback)

servoCallback
while True:
    time.sleep(1)



