#!/usr/bin/env python3
#-- coding: utf-8 --
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json
import RPi.GPIO as GPIO

#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent

def servoCallback(client, userdata, message):
    trigger=message.payload
    print("Received message: "+ trigger)
    
    GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
    GPIO.setwarnings(False) #Disable warnings

    #Use pin 12 for PWM signal
    pwm_gpio = 12
    frequence = 50
    GPIO.setup(pwm_gpio, GPIO.OUT)
    pwm = GPIO.PWM(pwm_gpio, frequence)

    #Init at 0°
    pwm.start(angle_to_percent(0))
    time.sleep(1)
    
    if trigger == 1:
        pwm.ChangeDutyCycle(angle_to_percent(90))
        time.sleep(1)
    else:
        pwm.ChangeDutyCycle(angle_to_percent(180))
        time.sleep(1)

    #Close GPIO & cleanup
    pwm.stop()
    GPIO.cleanup()

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
while True:
    time.sleep(1)
