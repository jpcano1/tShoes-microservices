""" Development settings """

from .base import *
from .base import env

# Base
DEBUG = True

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='z-&r-2hoq*ilrolvi)(2g)x-o=hp*9)h5une=_ytgw!w8o*hjp')
ALLOWED_HOSTS = ["*"]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

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