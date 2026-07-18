from config import (
    TEMPERATURE_LIMIT,
    SPEED_LIMIT,
    VIBRATION_LIMIT,
    PASSENGER_LIMIT,
)


def check_temperature(value):
    return value >= TEMPERATURE_LIMIT


def check_speed(value):
    return value >= SPEED_LIMIT


def check_vibration(value):
    return value >= VIBRATION_LIMIT


def check_passenger(value):
    return value >= PASSENGER_LIMIT


def check_brake(status):
    return status.upper() == "FAILED"