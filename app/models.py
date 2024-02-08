from django.db import models
from django.utils import timezone


class WeatherModel(models.Model):
    city = models.CharField(max_length=255)

    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()

    last_update = models.DateTimeField(auto_now=True)

    def is_need_update(self):
        return (timezone.now() - self.last_update).total_seconds() > 30 * 60
