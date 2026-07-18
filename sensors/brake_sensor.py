import random


class BrakeSensor:
    """
    Simulates brake status.
    """

    def __init__(self, ride_name):
        self.ride_name = ride_name

    def read(self):

        # 90% Normal | 10% Brake Failure
        if random.random() < 0.9:
            value = "OK"
        else:
            value = "FAILED"

        return {
            "sensor_name": "Brake Sensor",
            "sensor_type": "Brake",
            "ride_name": self.ride_name,
            "value": value,
            "unit": ""
        }