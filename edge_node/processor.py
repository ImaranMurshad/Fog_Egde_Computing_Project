from rules import (
    check_temperature,
    check_speed,
    check_vibration,
    check_passenger,
    check_brake,
)

from detector import calculate_risk
from logger import log_event
from sender import send_alert


def process_sensor_data(ride_name, sensor_name, sensor_type, value):

    alert = False

    if sensor_type == "Temperature":
        alert = check_temperature(value)

    elif sensor_type == "Speed":
        alert = check_speed(value)

    elif sensor_type == "Vibration":
        alert = check_vibration(value)

    elif sensor_type == "Passenger":
        alert = check_passenger(value)

    elif sensor_type == "Brake":
        alert = check_brake(value)

    if not alert:
        print("✅ Normal Reading")
        return

    risk_score, status = calculate_risk(sensor_type, value)

    log_event(
        sensor_type,
        value,
        risk_score,
        status
    )

    send_alert(
    ride_name=ride_name,
    sensor_name=sensor_name,
    sensor_type=sensor_type,
    value=value,
    status=status,
    message=f"{sensor_type} threshold exceeded",
    risk_score=risk_score
)