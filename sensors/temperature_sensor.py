import random


class TemperatureSensor:
    """
    Simulates a temperature sensor.
    """

    def __init__(self, ride_name):
        self.ride_name = ride_name

    def read(self):

        # 80% Normal | 20% High Temperature
        if random.random() < 0.8:
            value = round(random.uniform(30, 70), 2)
        else:
            value = round(random.uniform(80, 100), 2)

        return {
            "sensor_name": "Temperature Sensor",
            "sensor_type": "Temperature",
            "ride_name": self.ride_name,
            "value": value,
            "unit": "°C"
        }