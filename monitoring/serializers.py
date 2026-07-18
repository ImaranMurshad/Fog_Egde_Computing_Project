from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = "__all__"
        
        
from .models import FogHealth


class FogHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = FogHealth
        fields = "__all__"