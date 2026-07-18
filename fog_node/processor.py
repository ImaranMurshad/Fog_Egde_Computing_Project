from rules import evaluate_sensor


def process_sensor_data(sensor_data):
    """
    Process incoming sensor data and return alert if needed.
    """

    alert = evaluate_sensor(sensor_data)

    if alert:
        return {
            "ride_name": sensor_data["ride_name"],
            "sensor_name": sensor_data["sensor_name"],
            "sensor_type": sensor_data["sensor_type"],
            "value": sensor_data["value"],
            "status": alert["status"],
            "message": alert["message"]
        }

    return None