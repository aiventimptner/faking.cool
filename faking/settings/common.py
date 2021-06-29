import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ['SECRET_KEY']


# Application definition

INSTALLED_APPS = [
    'mentoring',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'faking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'faking' / 'templates'],
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

WSGI_APPLICATION = 'faking.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('SQL_NAME', 'faking'),
        'USER': os.getenv('SQL_USER', 'faking'),
        'PASSWORD': os.getenv('SQL_PASSWORD', ''),
        'HOST': os.getenv('SQL_HOST', ''),
        'PORT': os.getenv('SQL_PORT', ''),
    }
}


# Email

EMAIL_USE_TLS = True

EMAIL_HOST = os.getenv('SMTP_HOST', 'localhost')

EMAIL_PORT = os.getenv('SMTP_PORT', '25')

EMAIL_HOST_USER = os.getenv('SMTP_USER', '')

EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASSWORD', '')

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL', 'noreply@faking.cool')

SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'noreply@faking.cool')


# Password validation

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

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# File storage

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'faking' / 'static',
]

MEDIA_URL = '/media/'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
