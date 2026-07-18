import requests

from config import DJANGO_FOG_API_URL


def send_fog_health(data):

    try:
        response = requests.post(DJANGO_FOG_API_URL, json=data)

        if response.status_code in [200, 201]:
            print("✅ Fog Health Saved")

        else:
            print("❌ Error:", response.text)

    except Exception as e:
        print("❌ Connection Error:", e)