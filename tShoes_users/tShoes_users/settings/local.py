""" Development settings """

from .base import *
from .base import env

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='fz1g#2-^9u(8fe_$tm+vt9tqt5-ypqw61%yc14&#)*!-((o=4b')
ALLOWED_HOSTS = ["*"]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Email
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SENDGRID_API_KEY = env('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405

CORS_ORIGIN_ALLOW_ALL = True
""" CORS_ORIGIN_WHITELIST = (
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:4200",
    "http://127.0.0.1:8080",
    "http://192.168.0.10:8080",
    "https://localhost:8080",
    "http://3.88.140.100:8000"
) """