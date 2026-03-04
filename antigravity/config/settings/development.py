"""
development.py — Settings for local development only.
Never use these in production.
"""

from .base import *  # noqa: F401, F403
from decouple import config

# ── Never True in production ──────────────────────────────────────────────────
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ── Local SQLite database — easy for development, no setup needed ─────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405 — BASE_DIR from base.py
    }
}

# ── Email — print to console in dev instead of sending real emails ─────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ── CORS — allow all in dev ───────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True

# ── Relax axes in dev so you don't lock yourself out accidentally ─────────────
AXES_FAILURE_LIMIT = 20

# ── django-csp — relaxed in dev to allow inline scripts ──────────────────────
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")   # Relax in dev for hot reload tools
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")
