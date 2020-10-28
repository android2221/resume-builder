"""
Django settings for resume_builder project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Big Production flag, we use production settings where we need to based on the 
# boolean value of this field
IS_PRODUCTION=False
PRODUCTION_SETTING=os.environ.get("DJANGO_IS_PRODUCTION", False)

if PRODUCTION_SETTING == 'True':
    IS_PRODUCTION=True
else:
    IS_PRODUCTION=False

# Activate Google Analytics
ACTIVATE_GOOGLE_ANALYTICS=os.environ.get("ACTIVATE_GOOGLE_ANALYTICS", False)
if ACTIVATE_GOOGLE_ANALYTICS == 'True':
    ACTIVATE_GOOGLE_ANALYTICS=True
else:
    ACTIVATE_GOOGLE_ANALYTICS=False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# RESUME BUILDER APP CONFIGS
ROOT_URL = os.environ.get("DJANGO_SITE_URL", "")

SITE_URL = ROOT_URL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEFAULT_SECRET_KEY = 'o-9=#fc$is3jt$sv#1$28dd!d@#!nh5dshcqc7ql1ko07a-b=y'
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", DEFAULT_SECRET_KEY) 

# DEBUG
DJANGO_DEBUG=os.environ.get("DJANGO_DEBUG", False)
if DJANGO_DEBUG == 'True':
    DEBUG=True
else:
    DEBUG=False

if IS_PRODUCTION == False:
    ALLOWED_HOSTS=['localhost', ROOT_URL]
else:
    ALLOWED_HOSTS = [ROOT_URL, f'www.{ROOT_URL}']

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/builder"
LOGOUT_REDIRECT_URL = "/"

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Application definition

INSTALLED_APPS = [
    'builder.apps.BuilderConfig',
    'accounts.apps.AccountsConfig',
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

X_FRAME_OPTIONS = 'SAMEORIGIN' 

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'

ROOT_URLCONF = 'resume_builder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'resume_builder.context_processors.get_production_setting',
                'resume_builder.context_processors.add_url_setting'
            ],
        },
    },
]

WSGI_APPLICATION = 'resume_builder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DB_OPTIONS = ""

DB_SSL_ENABLED = os.environ.get("DB_SSL_ENABLED", False)

if DB_SSL_ENABLED:
    DB_OPTIONS = {'sslmode': 'require'}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_DBNAME", ""),
        'USER': os.environ.get("DB_USERNAME", ""),
        'HOST': os.environ.get("DB_FQDN", ""),
        'PASSWORD': os.environ.get("DB_PASSWORD", ""),
        'PORT': os.environ.get("DB_PORT", ""),
        'DB_OPTIONS': DB_OPTIONS
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/django-static-root/'

# Email Settings
USE_SENDGRID=os.environ.get("USE_SENDGRID", True)
if (USE_SENDGRID == 'False'):
    SHOULD_USE_SENDGRID=False
else:
    SHOULD_USE_SENDGRID=True

if SHOULD_USE_SENDGRID == True:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_ECHO_TO_STDOUT=True
DEFAULT_FROM_EMAIL  = 'do-not-reply@seemyresume.io'
SERVER_EMAIL  = 'do-not-reply@seemyresume.io'

EMAIL_FILE_PATH = os.environ.get("DJANGO_EMAIL_FILE_PATH", "")

if EMAIL_FILE_PATH is None:
    EMAIL_FILE_PATH = "/sent_emails/"

# My Settings

if IS_PRODUCTION == True:
    SECURE_SSL_REDIRECT=True
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
    X_FRAME_OPTIONS='DENY'
    SECURE_REFERRER_POLICY='origin'

FEEDBACK_FORM_URL = os.environ.get("FEEDBACK_FORM_URL", "")
SUPPORT_FORM_URL = os.environ.get("SUPPORT_FORM_URL", "")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}