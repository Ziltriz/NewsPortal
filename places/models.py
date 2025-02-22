from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator, MaxValueValidator
import random


class RemarkablePlace(models.Model):
    name = models.CharField(max_length=255)
    location = gis_models.PointField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(25)])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

class WeatherSummary(models.Model):
    place = models.ForeignKey(RemarkablePlace, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.FloatField()
    wind_direction = models.CharField(max_length=2)
    wind_speed = models.FloatField()

    def __str__(self):
        return f"Погода в {self.place.name} на {self.timestamp}"
    
    class Meta:
        verbose_name = 'Прогноз погоды'
        verbose_name_plural = 'Прогнозы погоды'