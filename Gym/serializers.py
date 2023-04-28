from rest_framework import serializers
from .models import Gyms

class GymsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gyms
        fields = '__all__'
        read_only_fields = ()