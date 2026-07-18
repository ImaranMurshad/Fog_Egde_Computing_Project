import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "themepark/sensors"

client = mqtt.Client()


def connect():
    client.connect(BROKER, PORT)
    client.loop_start()
    print(f"✅ Connected to MQTT Broker ({BROKER}:{PORT})")


def publish(data):
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    print(f"📤 Published : {payload}")


def disconnect():
    client.loop_stop()
    client.disconnect()
    print("❌ MQTT Disconnected")