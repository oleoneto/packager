"""
Django settings for packager project.
"""

import os
import re
from dotenv import load_dotenv
from .drf import *

# Read values from system environment
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG'))

ENABLE_S3 = False if DEBUG else bool(os.environ.get('ENABLE_S3', False))

ALLOWED_HOSTS = []

INTERNAL_IPS = '127.0.0.1'

CORS_ORIGIN_ALLOW_ALL = True

# Stripe account information. Use TEST values in DEBUG mode.

STRIPE_LIVE_MODE = False if DEBUG else bool(os.environ.get('STRIPE_LIVE_MODE'))

STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY')

STRIPE_TEST_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY')

STRIPE_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY') \
    if DEBUG else os.environ.get('STRIPE_LIVE_SECRET_KEY')

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY') \
    if DEBUG else os.environ.get('STRIPE_LIVE_PUBLISHABLE_KEY')


# Application definition

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_extensions',

    'polymorphic',

    'rest_framework',
    'rest_framework_httpsignature',
    'rest_framework_simplejwt',

    'debug_toolbar',
    'corsheaders',

    'packager.core.apps.CoreConfig',
]


MIDDLEWARE = [
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware', # <-- Caching
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', # <-- Caching
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware installed with django-clite
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


ROOT_URLCONF = 'packager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'packager/templates')
        ],
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

WSGI_APPLICATION = 'packager.wsgi.application'


# Database

ENGINE = 'django.db.backends.postgresql'

if "DATABASE_URL" in os.environ:

    USER, PASSWORD, HOST, PORT, NAME = re.match("^postgres://(?P<username>.*?)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/(?P<db>.*?)$", os.environ.get("DATABASE_URL", "")).groups()

    DATABASES = {
        'default': {
            'ENGINE': ENGINE,
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'HOST': HOST,
            'PORT': int(PORT),
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
     }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "") + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "packager"
    }
}

CACHE_TTL = 60 * 15

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "") + "/1"

CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "") + "/1"

CELERY_TASK_ALWAYS_EAGER = True

# CELERY_ACCEPT_CONTENT = ['application/json']

# CELERY_TASK_SERIALIZER = 'json'

# CELERY_RESULT_SERIALIZER = 'json'

# Email server backend configuration
# Use SendGrid to deliver automated email

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Password validation

# AUTH_USER_MODEL = 'authentication.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'guardian.backends.ObjectPermissionBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

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

# https://django-allauth.readthedocs.io/en/latest/providers.html

# ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_USERNAME_MIN_LENGTH = 6

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = int(os.environ.get('ACCOUNT_LOGIN_ATTEMPTS_LIMIT'))

ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = int(os.environ.get('ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT'))

ACCOUNT_USERNAME_BLACKLIST = os.environ.get('ACCOUNT_USERNAME_BLACKLIST')

ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# LOGIN_REDIRECT_URL = '/accounts/me/'

SOCIALACCOUNT_QUERY_EMAIL = True

GUARDIAN_RAISE_403 = True

OTP_TOTP_ISSUER = os.environ.get('OTP_ISSUER')


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

AWS_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

AWS_S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL')

AWS_S3_CUSTOM_DOMAIN = os.environ.get('S3_CUSTOM_DOMAIN')

AWS_LOCATION = os.environ.get('S3_LOCATION')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_IS_GZIPPED = True

if ENABLE_S3:
    DEFAULT_FILE_STORAGE = 'packager.storage.PublicFileStorage'

    STATICFILES_STORAGE = 'packager.storage.StaticStorage'

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/'

else:
    STATIC_URL = '/static/'

STATIC_ROOT = 'staticfiles/'

MEDIA_ROOT = 'mediafiles/'

MEDIA_URL = '/files/'


# Django REST Framework, JWT, and Swagger configurations go here.

# REST_FRAMEWORK = {}

# SIMPLE_JWT = {}

# SWAGGER_SETTINGS = {}


# Error logging and reporting with Sentry
# Advanced error reporting in production.

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
        RedisIntegration()
    ]
)
