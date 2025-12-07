"""
Development settings for worldbuilding project.
"""

from .base import *
from decouple import config

# Enable PostGIS/GIS features if configured
USE_POSTGIS = config('USE_POSTGIS', default=False, cast=bool)

if USE_POSTGIS:
    # Add GIS apps when PostGIS is enabled
    if 'django.contrib.gis' not in INSTALLED_APPS:
        INSTALLED_APPS.insert(INSTALLED_APPS.index('django.contrib.staticfiles') + 1, 'django.contrib.gis')
    if 'rest_framework_gis' not in INSTALLED_APPS:
        INSTALLED_APPS.insert(INSTALLED_APPS.index('corsheaders') + 1, 'rest_framework_gis')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0', cast=lambda v: [s.strip() for s in v.split(',')])

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Note: For memory_maps app to work fully, PostgreSQL with PostGIS extension is required
# For initial development without PostGIS, you can use SQLite (limited GIS features)

if USE_POSTGIS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': config('POSTGRES_DB', default='worldbuilding'),
            'USER': config('POSTGRES_USER', default='worldbuilding_user'),
            'PASSWORD': config('POSTGRES_PASSWORD', default='password'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # Fallback to SQLite for development without PostGIS
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS settings for development
# CORS settings - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Development-specific logging
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['memory_maps'] = {
    'handlers': ['console', 'file'],
    'level': 'DEBUG',
    'propagate': False,
}

# Disable some security features for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
