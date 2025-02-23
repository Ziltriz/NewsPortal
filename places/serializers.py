from rest_framework import serializers
from .models import RemarkablePlace, WeatherSummary


class RemarkablePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarkablePlace
        fields = ['id', 'name', 'location', 'rating']

class WeatherSummarySerializer(serializers.ModelSerializer):
    place = RemarkablePlaceSerializer() 

    class Meta:
        model = WeatherSummary
        fields = ['place', 'timestamp', 'temperature', 'humidity', 'pressure', 'wind_direction', 'wind_speed']