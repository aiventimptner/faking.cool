from .base import *

# General settings

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


# Secure Connections

CSRF_COOKIE_SECURE = True

SECURE_REFERRER_POLICY = 'origin'

SECURE_SSL_REDIRECT = False  # nginx already redirects http traffic to https

SESSION_COOKIE_SECURE = True
