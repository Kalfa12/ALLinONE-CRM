"""Django settings for the Marketing CRM project."""
from pathlib import Path
import os

from django.utils.translation import gettext_lazy as _

try:
    from decouple import config
except ImportError:  # fallback when python-decouple is not installed
    def config(key, default=None, cast=None):
        val = os.environ.get(key, default)
        if cast and val is not None:
            return cast(val)
        return val

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY', default='dev-insecure-key-change-me')
DEBUG = config('DJANGO_DEBUG', default='True', cast=lambda v: str(v).lower() in ('1', 'true', 'yes'))
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'apps.core',
    'apps.pipeline',
    'apps.assets',
    'apps.finance',
    'apps.chatbot',
    'apps.prediction',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crm_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.nav',
            ],
        },
    },
]

WSGI_APPLICATION = 'crm_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- i18n / l10n ---
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('ar', _('Arabic')),
]
USE_I18N = True
USE_TZ = True
TIME_ZONE = 'UTC'
LOCALE_PATHS = [BASE_DIR / 'locale']

# --- Static / Media ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'pipeline:kanban'
LOGOUT_REDIRECT_URL = 'login'

# --- DeepSeek ---
DEEPSEEK_API_KEY = config('DEEPSEEK_API_KEY', default='')
DEEPSEEK_BASE_URL = config('DEEPSEEK_BASE_URL', default='https://api.deepseek.com/v1')
DEEPSEEK_MODEL = config('DEEPSEEK_MODEL', default='deepseek-chat')

# --- ML model path ---
ML_MODEL_PATH = BASE_DIR / 'ml' / 'model.pkl'
