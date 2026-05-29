"""
Production Django settings overrides for De-commerce

Copy or point your WSGI/ASGI invocation to use this file in production, or
set DJANGO_SETTINGS_MODULE to de_commerce.production_settings.

This file intentionally keeps logic minimal and reads sensitive values
from environment variables. It sets secure defaults appropriate for
an HTTPS production environment.
"""
from .settings import *  # import base settings
import os

# SECURITY
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'example.com').split(',')

# Cookies & CSRF
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # frontend may read csrftoken cookie if using cookie-based flow
CSRF_COOKIE_SAMESITE = os.environ.get('CSRF_COOKIE_SAMESITE', 'Lax')
SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')

# Security headers
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'True') == 'True'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'

# Additional recommended production settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database and static/media should be set via environment-specific config
# e.g., use Postgres, configure STATIC_ROOT, MEDIA_URL, and cloud storage for media

# Logging: a minimal production logger to capture errors
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
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
