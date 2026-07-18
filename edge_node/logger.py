from datetime import datetime


def log_event(sensor_type, value, score, level):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 60)
    print(f"[{timestamp}]")
    print(f"Sensor      : {sensor_type}")
    print(f"Value       : {value}")
    print(f"Risk Score  : {score}")
    print(f"Risk Level  : {level}")
    print("=" * 60)