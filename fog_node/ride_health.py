def calculate_health(speed, temperature, vibration, passenger):

    health = 100

    # Speed
    if speed > 140:
        health -= 25
    elif speed > 120:
        health -= 15

    # Temperature
    if temperature > 90:
        health -= 25
    elif temperature > 80:
        health -= 15

    # Vibration
    if vibration > 9:
        health -= 25
    elif vibration > 7:
        health -= 15

    # Passenger
    if passenger > 50:
        health -= 15
    elif passenger > 40:
        health -= 10

    if health < 0:
        health = 0

    if health >= 90:
        status = "HEALTHY"

    elif health >= 70:
        status = "WARNING"

    else:
        status = "CRITICAL"

    return health, status