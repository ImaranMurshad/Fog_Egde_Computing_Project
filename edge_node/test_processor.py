from processor import process_sensor_data

# Temperature Alert
process_sensor_data(
    ride_name="Roller Coaster",
    sensor_name="Temperature Sensor",
    sensor_type="Temperature",
    value=95
)

# Speed Alert
process_sensor_data(
    ride_name="Roller Coaster",
    sensor_name="Speed Sensor",
    sensor_type="Speed",
    value=145
)

# Vibration Alert
process_sensor_data(
    ride_name="Roller Coaster",
    sensor_name="Vibration Sensor",
    sensor_type="Vibration",
    value=9
)

# Passenger Alert
process_sensor_data(
    ride_name="Roller Coaster",
    sensor_name="Passenger Sensor",
    sensor_type="Passenger",
    value=52
)

# Brake Alert
process_sensor_data(
    ride_name="Roller Coaster",
    sensor_name="Brake Sensor",
    sensor_type="Brake",
    value="FAILED"
)