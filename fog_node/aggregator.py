from collections import defaultdict


class FogAggregator:

    def __init__(self):
        self.data = defaultdict(list)

    def add_reading(self, sensor_type, value):
        self.data[sensor_type].append(value)

    def get_average(self, sensor_type):

        values = self.data.get(sensor_type, [])

        if not values:
            return 0

        return round(sum(values) / len(values), 2)

    def clear(self):
        self.data.clear()