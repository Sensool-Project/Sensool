from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json
import sys
import Adafruit_DHT

rootCAPath = "./root-ca-cert.pem"
certificatePath = "73db8a015c.cert.pem"
privateKeyPath = "73db8a015c.private.key"
host = "airh6d2ooyyep-ats.iot.us-east-2.amazonaws.com"
port = 8883
clientId = "esp1"
topic = "esp1/temp"

DHT_MQTTClient = AWSIoTMQTTClient(clientId)
DHT_MQTTClient.configureEndpoint(host, port)
DHT_MQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

DHT_MQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
DHT_MQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
DHT_MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
DHT_MQTTClient.configureConnectDisconnectTimeout(180)  # 10 sec
DHT_MQTTClient.configureMQTTOperationTimeout(3)  # 5 sec

DHT_MQTTClient.connect()

loopCount = 0
while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #print ('Temp: {0:0.1f} C  Humidity : {1:0.1f} %'.format(temperature, humidity))
    message = {}
    message['temperature'] = temperature
    message['humidity'] = humidity
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    DHT_MQTTClient.publish(topic, messageJson, 0)
    print('Published topic %s: %s\n' % (topic, messageJson))
    
    loopCount += 1        
