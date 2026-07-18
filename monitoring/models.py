from django.db import models


# ----------------------------
# Ride Model
# ----------------------------

class Ride(models.Model):

    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('STOPPED', 'Stopped'),
        ('MAINTENANCE', 'Maintenance'),
        ('EMERGENCY', 'Emergency'),
    ]

    name = models.CharField(max_length=100)

    location = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='RUNNING'
    )

    installed_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------
# Sensor Model
# ----------------------------

class Sensor(models.Model):

    SENSOR_TYPES = [
        ('SPEED', 'Speed'),
        ('TEMPERATURE', 'Temperature'),
        ('VIBRATION', 'Vibration'),
        ('PASSENGER', 'Passenger'),
        ('BRAKE', 'Brake'),
    ]

    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="sensors"
    )

    sensor_name = models.CharField(max_length=100)

    sensor_type = models.CharField(
        max_length=20,
        choices=SENSOR_TYPES
    )

    unit = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sensor_name


# ----------------------------
# Sensor Reading
# ----------------------------

class SensorReading(models.Model):

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="readings"
    )

    value = models.FloatField()

    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.sensor_name} - {self.value}"


# ----------------------------
# Fog Processed Data
# ----------------------------

class FogData(models.Model):

    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE
    )

    average_value = models.FloatField()

    risk_score = models.FloatField()

    status = models.CharField(max_length=50)

    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ride.name} - {self.risk_score}"


# ----------------------------
# Alert
# ----------------------------

class Alert(models.Model):

    SEVERITY = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY
    )

    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title