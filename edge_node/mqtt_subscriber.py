import json
import paho.mqtt.client as mqtt

from processor import process_sensor_data

BROKER = "localhost"
PORT = 1883
TOPIC = "themepark/sensors"


def on_connect(client, userdata, flags, rc):
    print("✅ Edge Node Connected to MQTT Broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    print("\n📥 Received Sensor Data")
    print(data)

    process_sensor_data(
        ride_name=data["ride_name"],
        sensor_name=data["sensor_name"],
        sensor_type=data["sensor_type"],
        value=data["value"]
    )


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("🚀 Edge Node Listening...")

client.loop_forever()