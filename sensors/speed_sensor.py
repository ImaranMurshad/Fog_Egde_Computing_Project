import random


class SpeedSensor:
    """
    Simulates a speed sensor for a theme park ride.
    """

    def __init__(self, ride_name):
        self.ride_name = ride_name

    def read(self):

        # 80% Normal | 20% High Speed
        if random.random() < 0.8:
            value = round(random.uniform(60, 110), 2)
        else:
            value = round(random.uniform(120, 160), 2)

        return {
            "sensor_name": "Speed Sensor",
            "sensor_type": "Speed",
            "ride_name": self.ride_name,
            "value": value,
            "unit": "km/h"
        }