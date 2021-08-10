from rest_framework import serializers
from .models import RushingStatistic

# Serializer for serializing all model fields for rushing statstic.
class RushingStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = RushingStatistic
        fields = '__all__'