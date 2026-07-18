import json
import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    SENSOR_TOPIC,
)

from aggregator import FogAggregator
from sender import send_fog_health
from ride_health import calculate_health


aggregator = FogAggregator()


def on_connect(client, userdata, flags, rc):
    print("✅ Fog Node Connected")
    client.subscribe(SENSOR_TOPIC)


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    print("\n📥 Fog Received")
    print(data)

    sensor_type = data["sensor_type"]
    value = data["value"]

    # Ignore brake values for averaging
    if sensor_type != "Brake":
        aggregator.add_reading(sensor_type, float(value))

    # Calculate averages
    averages = {
        "Speed": aggregator.get_average("Speed"),
        "Temperature": aggregator.get_average("Temperature"),
        "Vibration": aggregator.get_average("Vibration"),
        "Passenger": aggregator.get_average("Passenger"),
    }

    print("\n📊 Current Averages")
    print(averages)

    # Calculate Ride Health
    health, health_status = calculate_health(
        averages["Speed"],
        averages["Temperature"],
        averages["Vibration"],
        averages["Passenger"],
    )

    print("\n❤️ Ride Health")
    print(f"Health Score : {health}%")
    print(f"Status       : {health_status}")

    # Send Fog Health to Django
    send_fog_health({
        "ride_name": data["ride_name"],
        "health_score": health,
        "health_status": health_status,
        "average_speed": averages["Speed"],
        "average_temperature": averages["Temperature"],
        "average_vibration": averages["Vibration"],
        "average_passenger": averages["Passenger"],
    })


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)

print("🚀 Fog Node Listening...")

client.loop_forever()