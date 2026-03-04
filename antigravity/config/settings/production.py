"""
production.py — Settings for the live server ONLY.
All security flags are maximally strict here.
"""

from .base import *  # noqa: F401, F403
from decouple import config, Csv

# ── NEVER True in production ──────────────────────────────────────────────────
DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# ── PostgreSQL from environment variable ──────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            # Enforce SSL connection to the database
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 60,  # Keep DB connections alive for 60 seconds
    }
}

# ── HTTPS enforcement ─────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT = True              # Redirect all HTTP → HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── HSTS — tells browsers to ALWAYS use HTTPS for 1 year ─────────────────────
SECURE_HSTS_SECONDS = 31_536_000       # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ── Cookie security ───────────────────────────────────────────────────────────
SESSION_COOKIE_SECURE = True           # Session cookie only sent over HTTPS
CSRF_COOKIE_SECURE = True              # CSRF cookie only sent over HTTPS

# ── Browser security headers ──────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER = True       # X-XSS-Protection header
SECURE_CONTENT_TYPE_NOSNIFF = True     # X-Content-Type-Options: nosniff
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ── Content Security Policy — strict: blocks XSS by default ──────────────────
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)           # No inline scripts, no eval()
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)      # Nobody can embed our pages in iframes
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)          # Forms can only submit to our own domain

# ── CORS — lock down to explicit origins only ─────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv(), default='')

# ── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')
