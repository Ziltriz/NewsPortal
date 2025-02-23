from django.db.models.signals import post_save
from django.dispatch import receiver
from constance.signals import config_updated
from constance import config
from django_celery_beat.models import PeriodicTask, CrontabSchedule


@receiver(config_updated)
def update_news_schedule(sender, key, old_value, new_value, **kwargs):
    if key in ['HOUR', 'MINUTES']:

        # Обновляем расписание
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=config.MINUTES or '0',
            hour=config.HOUR or '10',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        # Находим задачу и обновляем её расписание
        periodic_task = PeriodicTask.objects.filter(task='news.tasks.send_daily_news').first()

        if periodic_task:
            periodic_task.crontab = schedule
            periodic_task.save()
        else:
            task_name = f"send_email"
            PeriodicTask.objects.create(
                name=task_name,
                crontab = schedule,
                task ='news.tasks.send_daily_news',  
            )
        
