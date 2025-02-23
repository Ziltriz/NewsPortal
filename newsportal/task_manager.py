from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from constance import config  # Импортируйте config здесь
    sender.add_periodic_task(
        crontab(hour=config.EMAIL_SEND_HOUR or 9, minute=config.EMAIL_SEND_MINUTE or 0),
        send_daily_news.s(),
        name='send daily news'
    )