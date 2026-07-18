import requests

API_URL = "http://54.156.242.205/api/alerts/"


def send_alert(
    ride_name,
    sensor_name,
    sensor_type,
    value,
    status,
    message,
    risk_score
):

    payload = {
        "ride_name": ride_name,
        "sensor_name": sensor_name,
        "sensor_type": sensor_type,
        "value": value,
        "status": status,
        "message": message,
        "risk_score": risk_score
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code in [200, 201]:
            print("✅ Alert Sent Successfully")
        else:
            print(f"❌ Error : {response.status_code}")
            print(response.text)

    except Exception as e:
        print("Connection Error:", e)