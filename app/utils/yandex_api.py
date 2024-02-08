import requests
from geopy import geocoders
from rest_framework.exceptions import APIException

from config.settings import YANDEX_WEATHER_TOKEN

TOKEN = YANDEX_WEATHER_TOKEN


def get_coords_from_city(city: str) -> tuple[float, float]:
    geolocator = geocoders.Nominatim(user_agent="django")
    try:
        geocode = geolocator.geocode(city)
    except Exception:
        raise APIException('Geocoder error')

    if geocode is None:
        raise APIException('City not found')

    return geocode.latitude, geocode.longitude


def get_weather(city: str) -> dict:
    latitude, longitude = get_coords_from_city(city)

    url = 'https://api.weather.yandex.ru/v2/forecast'
    params = {
        'lat': latitude,
        'lon': longitude,
        'lang': 'ru_RU',
    }
    headers = {
        'X-Yandex-API-Key': TOKEN
    }
    response = requests.get(url, params=params, headers=headers)
    if not response.ok:
        raise APIException('Yandex weather API error')

    return response.json()
