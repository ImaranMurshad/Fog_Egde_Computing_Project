from django.contrib import admin
from .models import (
    Ride,
    Sensor,
    SensorReading,
    FogData,
    Alert
)


admin.site.register(Ride)
admin.site.register(Sensor)
admin.site.register(SensorReading)
admin.site.register(FogData)
admin.site.register(Alert)