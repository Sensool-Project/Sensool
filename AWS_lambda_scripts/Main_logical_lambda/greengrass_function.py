import time
import json
import platform
import greengrasssdk
import logging

client = greengrasssdk.client('iot-data')
logger=logging.getLogger('logger')
output_topic="servo/trigger"

def lambda_handler(event, context):
    topic = context.client_context.custom['subject']
    humidity = event['humidity']
    if humidity>60:
         trigger=True
    else:
         trigger=False

    client.publish(topic=output_topic, payload=str(trigger))
    return str(trigger)