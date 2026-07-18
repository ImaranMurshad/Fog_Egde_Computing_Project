import json

import paho.mqtt.client as mqtt

from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from processor import process_sensor_data
from sender import send_alert


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):

    sensor_data = json.loads(msg.payload.decode())

    print("\nReceived:")
    print(sensor_data)

    alert = process_sensor_data(sensor_data)

    if alert:
        print("ALERT GENERATED")
        print(alert)

        send_alert(alert)


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)

print("Fog Node Started...")

client.loop_forever()