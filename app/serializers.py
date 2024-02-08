from rest_framework import serializers

from app.models import WeatherModel


class CitySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=255)


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherModel
        fields = ['temperature', 'pressure', 'wind_speed']
        read_only_fields = fields
