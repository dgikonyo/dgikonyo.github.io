from rest_framework import serializers
from .models import Disaster

class DisasterSerializer(serializers.ModelsSerializer):
    class Meta:
        model=Disaster
        fields='__all__'