from bluetooth import *
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

def input_and_send():
    print("\nType something\n")
    while True:
        data = input()
        if len(data) == 0: break
        sock.send(data)
        sock.send("\n")
        
def rx_and_echo():
    sock.send("\nsend anything\n")
    while True:
        data = sock.recv(buf_size)
        if data:
            print(data)
            sock.send(data)
            
            newdata = data.replace("\\","")
            DHT_MQTTClient.publish(topic, newdata, 0)
            print('Published topic %s: %s\n' % (topic, newdata))            
            
#MAC address of ESP32
addr = "24:6F:28:79:00:6E"
#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
#service_matches = find_service( uuid = uuid, address = addr )
service_matches = find_service( address = addr )

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

#input_and_send()
rx_and_echo()

sock.close()
print("\n--- bye ---\n")
