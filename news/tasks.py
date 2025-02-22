from celery import shared_task
from constance import config
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from .models import News


@shared_task
def send_daily_news():
    today_news = News.objects.filter(publication_date__date=datetime.today())
    recipients = config.EMAIL_RECIPIENTS.split(',')
    subject = config.EMAIL_SUBJECT
    message = config.EMAIL_MESSAGE

    html_message = render_to_string('email_template.html', {'news': today_news})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, html_message=html_message)