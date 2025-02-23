from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import News
from constance import config


@shared_task(bind=False)
def send_daily_news():
    # Получаем новости, опубликованные сегодня
    today = timezone.now().date()  # Используем timezone-aware дату
    today_news = News.objects.filter(publication_date__date=today)

    # Проверяем, есть ли новости для отправки
    if not today_news.exists():
        print("Нет новостей для отправки")
        return

    if config:
        # Получаем настройки из Constance
        recipients = getattr(config, 'EMAIL_RECIPIENTS', '').split(',') if config.EMAIL_RECIPIENTS else []
        subject = getattr(config,'EMAIL_SUBJECT', "Новые новости")
        message = getattr(config,'EMAIL_MESSAGE', "*Чмок я тебе новости принес")

    # Генерируем HTML-сообщение
    html_message = render_to_string('email/email_template.html', {'news': today_news})

    # Отправляем email
    if recipients:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message
            )
            print(f"Успешно оправлено общение {recipients}")
        except Exception as e:
            print(f"Ошибка отправки новостей: {e}")
    else:
        print("Ошибка получения настроек Constanse.")