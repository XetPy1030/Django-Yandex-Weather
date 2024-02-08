from django.test import TestCase
from rest_framework.test import APIRequestFactory

from app.views import WeatherView


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

    def test_weather(self):
        request = self.factory.get("/weather", {"city": "Moscow"})
        response = WeatherView.as_view()(request)

        assert response.status_code == 200
        assert response.data is not None

    def test_city_not_found(self):
        request = self.factory.get("/weather", {"city": "oawdowadij"})
        response = WeatherView.as_view()(request)

        assert response.status_code == 500
        assert response.data['detail'] == 'City not found'
