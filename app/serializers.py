from rest_framework import serializers
from .models import RushingStatistic

class RushingStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = RushingStatistic
        fields = '__all__'