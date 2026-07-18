# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# Topics
SENSOR_TOPIC = "themepark/sensors"
FOG_TOPIC = "themepark/fog"

# Django Backend
DJANGO_API_URL = "http://54.156.242.205/api/alerts/"
DJANGO_FOG_API_URL = "http://54.156.242.205/api/fog-health/"

# Sensor Thresholds
MAX_SPEED = 100
MAX_TEMPERATURE = 45
MAX_VIBRATION = 1.5
MAX_PASSENGERS = 24

# Fog Processing
WINDOW_SIZE = 5