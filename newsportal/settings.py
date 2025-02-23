"""
Django settings for newsportal project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.gis.db import models as geo_models
from leaflet.forms.widgets import LeafletWidget

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis', 
    'rest_framework',      
    'constance',           
    'constance.backends.database',  
    'django_summernote', 
    'django_celery_beat',
    'django_filters',
    'leaflet',  
    'news',                
    'places',        
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newsportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'newsportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'newsportal',
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': 'db', 
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10, 
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')  # SMTP-сервер
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)  # Порт SMTP
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)  # Включить TLS
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your-email@example.com')  # Ваш email
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-email-password')  # Пароль от email
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@example.com') 

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}



CONSTANCE_CONFIG = {
    'EMAIL_RECIPIENTS': ('', 'Email получателей (через запятую)'),
    'EMAIL_SUBJECT': ('Тема рассылки', 'Сообщение'),
    'EMAIL_MESSAGE': ('У нас тут новости новые, заходи, смотри *Чмок*!', 'Сообщение'),
    'HOUR': (9, 'Время отправки  часы (0-23)'),
    'MINUTES': (00, 'Время отправки  минуты (0-59)'),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

GDAL_LIBRARY_PATH = '/lib/aarch64-linux-gnu/libgdal.so'

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


LEAFLET_CONFIG = {
    'PLUGINS': {
        'forms': {
            'auto-include': True
        }
    }
}
LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
    'map_width': '100%',
    'display_raw': 'true',
    'map_srid': 4326,
    'Attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',

}

LEAFLET_FIELD_OPTIONS = {'widget': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}

FORMFIELD_OVERRIDES = {
    geo_models.PointField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiPointField: LEAFLET_FIELD_OPTIONS,
    geo_models.LineStringField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiLineStringField: LEAFLET_FIELD_OPTIONS,
    geo_models.PolygonField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiPolygonField: LEAFLET_FIELD_OPTIONS,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


SUMMERNOTE_THEME = 'bs4'