from .base import *


# General settings

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


# Database

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD')
    }
}


# Static Files

STATIC_ROOT = BASE_DIR / 'static'


# Secure Connections

CSRF_COOKIE_SECURE = True

SECURE_REFERRER_POLICY = 'origin'

SECURE_SSL_REDIRECT = False  # nginx already redirects http traffic to https

SESSION_COOKIE_SECURE = True
