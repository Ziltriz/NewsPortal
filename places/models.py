from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator, MaxValueValidator
import random


class RemarkablePlace(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название места')
    location = gis_models.PointField(verbose_name='Гео-координаты места (точка)')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(25)],verbose_name='Рейтинг (от 0 до 25)')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Примечательное места'
        verbose_name_plural = 'Примечательные места'

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
        verbose_name = 'Сводка погоды'
        verbose_name_plural = 'Сводки погоды'