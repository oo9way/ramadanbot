import logging
import os
import sys

import dj_database_url
import dotenv

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load env variables from file
dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    'x%#3&%giwv8f0+%r946en7z&d@9*rc$sl0qoql56xr%bh^w2mj',
)

if os.environ.get('DJANGO_DEBUG', default=False) in ['True', 'true', '1', True]:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["*",]  # since Telegram uses a lot of IPs for webhooks


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',
    'debug_toolbar',

    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.common.CommonMiddleware',
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'dtb.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'dtb.wsgi.application'
ASGI_APPLICATION = 'dtb.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, default="sqlite:///db.sqlite3"),
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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"


# -----> CELERY
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
BROKER_URL = REDIS_URL
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_DEFAULT_QUEUE = 'default'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# -----> TELEGRAM
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    logging.error(
        "Please provide TELEGRAM_TOKEN in .env file.\n"
        "Example of .env file: https://github.com/ohld/django-telegram-bot/blob/main/.env_example"
    )
    sys.exit(1)

TELEGRAM_LOGS_CHAT_ID = os.getenv("TELEGRAM_LOGS_CHAT_ID", default=None)

# -----> SENTRY
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.celery import CeleryIntegration
# from sentry_sdk.integrations.redis import RedisIntegration

# sentry_sdk.init(
#     dsn="INPUT ...ingest.sentry.io/ LINK",
#     integrations=[
#         DjangoIntegration(),
#         CeleryIntegration(),
#         RedisIntegration(),
#     ],
#     traces_sample_rate=0.1,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )



JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Ramadan",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Ramadan",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Ramadan days",

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "books/img/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Ramadan days admin",

    # Copyright on the footer
    "copyright": "Acme Library Ltd",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": [],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # model admin to link to (Permissions checked against model)
        {"model": "users.User"},
        {"model": "users.Application"},

    ],

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth", "django_celery_beat"],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],


    # for the full list of 5.13.0 free icon classes
    "icons": {
        "users.user": "fas fa-user",
        "users.application": "fas fa-book",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"users.user": "collapsible", "users.application": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}