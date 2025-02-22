from celery import shared_task
from .models import RemarkablePlace, WeatherSummary
import random


@shared_task
def update_weather():
    places = RemarkablePlace.objects.all()
    for place in places:
        weather_data = get_weather(place.location.x, place.location.y)
        WeatherSummary.objects.create(place=place, **weather_data)


def get_weather(lat, lon):
    fake_data = {
        'temperature': round(random.uniform(-50, 50), 2),
        'humidity': random.randint(0, 100),
        'pressure': round(random.uniform(700, 800), 2),
        'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
        'wind_speed': round(random.uniform(0, 30), 2)
    }
    return fake_data