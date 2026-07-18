import time

from speed_sensor import SpeedSensor
from temperature_sensor import TemperatureSensor
from vibration_sensor import VibrationSensor
from passenger_sensor import PassengerSensor
from brake_sensor import BrakeSensor

from mqtt_client import connect, publish, disconnect


def main():

    ride = "Roller Coaster"

    sensors = [
        SpeedSensor(ride),
        TemperatureSensor(ride),
        VibrationSensor(ride),
        PassengerSensor(ride),
        BrakeSensor(ride)
    ]

    connect()

    print("\n========== SENSOR PUBLISHER STARTED ==========\n")

    try:

        while True:

            print("=" * 70)

            for sensor in sensors:

                data = sensor.read()

                print(data)

                publish(data)

            print("=" * 70)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nStopping Sensor Publisher...")

    finally:
        disconnect()


if __name__ == "__main__":
    main()