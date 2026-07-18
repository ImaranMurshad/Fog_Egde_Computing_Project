from config import (
    MAX_SPEED,
    MAX_TEMPERATURE,
    MAX_VIBRATION,
    MAX_PASSENGERS,
)


def evaluate_sensor(sensor_data):
    """
    Evaluates a single sensor reading and returns
    alert information if a threshold is exceeded.
    """

    sensor_type = sensor_data["sensor_type"]
    value = sensor_data["value"]

    # ---------------- Speed ----------------
    if sensor_type == "SPEED":
        if value > MAX_SPEED:
            return {
                "status": "HIGH",
                "message": f"Overspeed detected ({value} km/h)"
            }

    # ---------------- Temperature ----------------
    elif sensor_type == "TEMPERATURE":
        if value > MAX_TEMPERATURE:
            return {
                "status": "HIGH",
                "message": f"High temperature detected ({value} °C)"
            }

    # ---------------- Vibration ----------------
    elif sensor_type == "VIBRATION":
        if value > MAX_VIBRATION:
            return {
                "status": "HIGH",
                "message": f"Excessive vibration detected ({value} g)"
            }

    # ---------------- Passenger ----------------
    elif sensor_type == "PASSENGER":
        if value > MAX_PASSENGERS:
            return {
                "status": "MEDIUM",
                "message": f"Ride overloaded ({value} passengers)"
            }

    # ---------------- Brake ----------------
    elif sensor_type == "BRAKE":

        if value == "WARNING":
            return {
                "status": "MEDIUM",
                "message": "Brake system warning"
            }

        elif value == "FAIL":
            return {
                "status": "CRITICAL",
                "message": "Brake system failure"
            }

    return None