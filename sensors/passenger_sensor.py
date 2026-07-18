import random


class PassengerSensor:
    """
    Simulates passenger count.
    """

    def __init__(self, ride_name):
        self.ride_name = ride_name

    def read(self):

        # 80% Normal | 20% Overloaded
        if random.random() < 0.8:
            value = random.randint(10, 35)
        else:
            value = random.randint(40, 60)

        return {
            "sensor_name": "Passenger Sensor",
            "sensor_type": "Passenger",
            "ride_name": self.ride_name,
            "value": value,
            "unit": "Passengers"
        }