# Create your views here.
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import WeatherModel
from app.serializers import CitySerializer, WeatherSerializer
from app.utils.yandex_api import get_weather


class WeatherView(APIView):
    def get(self, request: WSGIRequest):
        city_serializer = CitySerializer(data=request.GET)
        city_serializer.is_valid(raise_exception=True)
        city = city_serializer.validated_data['city']

        weather_model = WeatherModel.objects.filter(city=city).first()
        is_need_update = weather_model is None or weather_model.is_need_update()
        is_save = False
        if weather_model is None:
            weather_model = WeatherModel(city=city)
            is_save = True

        if is_need_update:
            weather_data = get_weather(city)
            weather_model.temperature = weather_data['fact']['temp']
            weather_model.pressure = weather_data['fact']['pressure_mm']
            weather_model.wind_speed = weather_data['fact']['wind_speed']
            is_save = True

        if is_save:
            weather_model.save()

        weather_serializer = WeatherSerializer(weather_model)
        return Response(weather_serializer.data)