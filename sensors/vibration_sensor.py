import random


class VibrationSensor:
    """
    Simulates a vibration sensor.
    """

    def __init__(self, ride_name):
        self.ride_name = ride_name

    def read(self):

        # 80% Normal | 20% High Vibration
        if random.random() < 0.8:
            value = round(random.uniform(1.0, 6.5), 2)
        else:
            value = round(random.uniform(7.0, 10.0), 2)

        return {
            "sensor_name": "Vibration Sensor",
            "sensor_type": "Vibration",
            "ride_name": self.ride_name,
            "value": value,
            "unit": "g"
        }