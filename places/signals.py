from django.db.models.signals import pre_save, post_save
from newsportal.task_manager import app as celery_app
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from .models import RemarkablePlace




@receiver(post_save, sender=RemarkablePlace)
def start_sync_on_event_change(sender, instance, created, **kwargs):
    """
    Запускает задачу на получение сводки погоды, после сохранения
    """
    # Запускаем задачу для этого мероприятия
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=3600,  # Каждый час
        period=IntervalSchedule.SECONDS,
    )

    # Создаем уникальное имя для задачи
    task_name = f"get_weather_{instance.id}"

    # Создаем или обновляем периодическую задачу
    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            'interval': schedule,
            'task': 'places.tasks.update_weather',  
            'args': json.dumps([instance.id]),  # Аргументы задачи как JSON-строка
        }
    )