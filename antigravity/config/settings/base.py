"""
base.py — Settings shared across ALL environments.
Never put environment-specific values here.
Secrets must always come from the .env file via python-decouple.
"""

from pathlib import Path
from decouple import config, Csv

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ── Secret key — NEVER hardcode; read from .env ───────────────────────────────
SECRET_KEY = config('SECRET_KEY')

# ── Application definition ────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Security
    'axes',             # Brute-force login protection
    'corsheaders',      # CORS headers

    # Our apps
    'apps.core',
    'apps.accounts',
    'apps.dashboard',
]

# ── Middleware — ORDER MATTERS ─────────────────────────────────────────────────
# corsheaders must be above CommonMiddleware
# axes must be the LAST in AUTHENTICATION_BACKENDS but here in middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    # Secure static files
    'corsheaders.middleware.CorsMiddleware',         # CORS — must be high up
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',     # CSRF — do NOT remove
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',                # Brute-force — must be last
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media (user uploads) ──────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Authentication backends ───────────────────────────────────────────────────
# axes.backends.AxesStandaloneBackend must be first for brute-force to work
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'auth.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ── Password hashing — bcrypt is stronger than default PBKDF2 ─────────────────
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',     # fallback for old hashes
]

# ── Password strength validators ─────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        # Reject passwords that contain the username
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Minimum 10 chars (stricter than Django's default 8)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 10},
    },
    {
        # Reject common passwords (checks against 20,000 known bad ones)
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Reject passwords that are entirely numeric
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ── Session security ──────────────────────────────────────────────────────────
SESSION_COOKIE_HTTPONLY = True      # JS cannot read the session cookie
SESSION_COOKIE_SAMESITE = 'Lax'    # Prevents CSRF via cookie on cross-site requests
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week

# ── CSRF ──────────────────────────────────────────────────────────────────────
CSRF_COOKIE_HTTPONLY = True         # JS cannot read the CSRF cookie
CSRF_COOKIE_SAMESITE = 'Lax'

# ── Clickjacking protection ───────────────────────────────────────────────────
X_FRAME_OPTIONS = 'DENY'           # Prevents your pages being embedded in iframes

# ── django-axes (brute-force protection) ──────────────────────────────────────
AXES_FAILURE_LIMIT = 5             # Lock after 5 failed login attempts
AXES_COOLOFF_TIME = 0.25           # Unlock after 15 minutes (0.25 hours)
AXES_LOCKOUT_TEMPLATE = 'accounts/locked.html'
AXES_RESET_ON_SUCCESS = True       # Reset fail count on successful login
AXES_ENABLE_ACCESS_FAILURE_LOG = True

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'apps': {
            # Capture all app-level logging (login events, security events, etc.)
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
