from celery import shared_task
from .models import RemarkablePlace, WeatherSummary
from django_celery_beat.models import PeriodicTask
from django.utils.timezone import now
import random


@shared_task(bind=False)
def update_weather(place_id):

    try:
        place = RemarkablePlace.objects.get(pk=place_id)
    except RemarkablePlace.DoesNotExist:
        return "Не найдено место для получения сводки погоды"
    
    if place:
        weather_data = get_weather(place.location.x, place.location.y)
        WeatherSummary.objects.create(place=place, **weather_data)

        task_name = f"get_weather_{place_id}"  
        periodic_task = PeriodicTask.objects.filter(name=task_name).first()

        if periodic_task:
            periodic_task.last_run_at = now()
            periodic_task.save()

        return "Task completed successfully"
    


def get_weather(lat, lon):
    fake_data = {
        'temperature': round(random.uniform(-50, 50), 2),
        'humidity': random.randint(0, 100),
        'pressure': round(random.uniform(700, 800), 2),
        'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
        'wind_speed': round(random.uniform(0, 30), 2)
    }
    return fake_data