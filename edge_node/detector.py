from config import (
    LOW_RISK,
    MEDIUM_RISK,
    HIGH_RISK,
)


def calculate_risk(sensor_type, value):

    score = 0

    if sensor_type == "Temperature":
        if value >= 100:
            score = 100
        elif value >= 90:
            score = 80
        elif value >= 80:
            score = 60

    elif sensor_type == "Speed":
        if value >= 150:
            score = 100
        elif value >= 140:
            score = 80
        elif value >= 120:
            score = 60

    elif sensor_type == "Vibration":
        if value >= 10:
            score = 100
        elif value >= 8:
            score = 80
        elif value >= 7:
            score = 60

    elif sensor_type == "Passenger":
        if value >= 60:
            score = 100
        elif value >= 50:
            score = 80
        elif value >= 40:
            score = 60

    elif sensor_type == "Brake":
        score = 100 if value == "FAILED" else 0

    if score >= HIGH_RISK:
        level = "CRITICAL"
    elif score >= MEDIUM_RISK:
        level = "HIGH"
    elif score >= LOW_RISK:
        level = "MEDIUM"
    else:
        level = "NORMAL"

    return score, level