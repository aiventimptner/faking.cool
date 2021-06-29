from .common import *  # noqa


DEBUG = True

ALLOWED_HOSTS = ['*']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}


# File storage

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_ROOT = BASE_DIR / 'media'


# Security

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False
