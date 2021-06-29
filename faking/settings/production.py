from .common import *  # noqa


DEBUG = False

ALLOWED_HOSTS = [
    'faking.cool',
    'www.faking.cool',
] + os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

ADMINS = [('Fachschaftsrat Maschinenbau', 'farafmb@ovgu.de')]


# File storage

STATIC_ROOT = BASE_DIR / 'data' / 'static'

MEDIA_ROOT = BASE_DIR / 'data' / 'media'


# Secure Connections

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = False  # We're using nginx as reverse proxy

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
