import os
import sys
from datetime import timedelta

from celery.schedules import crontab
from dotenv import load_dotenv

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(override=True)  # ИСПОЛЬЗОВАТЬ ДАННЫЕ ИЗ ПЕРЕМЕННОГО ОКРУЖЕНИЯ ИЗ ФАЙЛА .ENV


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("DEBUG") == "True" else False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tracker",
    "rest_framework",
    "rest_framework_simplejwt",
    "users",
    "django_filters",
    "drf_spectacular",
    "django_celery_beat",
    # "corsheaders",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
]

# CORS_ALLOWED_ORIGINS = [
#     '<http://localhost:8000>',  # Замените на адрес вашего фронтенд-сервера
# ]
#
# CSRF_TRUSTED_ORIGINS = [
#     "https://read-and-write.example.com", #  Замените на адрес вашего фронтенд-сервера
#     # и добавьте адрес бэкенд-сервера
# ]
#
# CORS_ALLOW_ALL_ORIGINS = True # только если DEBUG=True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = os.getenv("TIME_ZONE")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = (BASE_DIR / "static",)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"  # Указываем кастомную модель для уинтификации
#
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")  # Настройки почты
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True if os.getenv("EMAIL_USE_TLS") == "True" else False
EMAIL_USE_SSL = True if os.getenv("EMAIL_USE_SSL") == "True" else False
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


if "test" in sys.argv:
    ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

    # Дополнительные настройки для тестов
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",  # Быстрее для тестов
    ]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "mailservices": {  # ← имя вашего приложения
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
#
# LOGIN_REDIRECT_URL = 'users:profile'# Редирект после логирования(имя приложения и имя в url)
# LOGOUT_REDIRECT_URL = 'mailservices:home'# Редирект после выхода(имя приложения и имя в url )
# LOGIN_URL = 'users:register'# Редирект на страницу регистрации, если вьюшка защищена миксином LoginRequiredMixin
#
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
    }
}


# Настройки Celery
if "test" in sys.argv:
    # Настройки для тестов
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    # Используем memory backend вместо Redis
    CELERY_RESULT_BACKEND = "cache"
    CELERY_CACHE_BACKEND = "memory"
else:
    # Реальные настройки
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Настройки Celery Beat (планировщик) каждые 6 часов, чтобы не "проморгать" момент отправки
CELERY_BEAT_SCHEDULE = {
    "check-habits-daily": {
        "task": "tracker.tasks.check_all_habits",
        "schedule": crontab(minute=0, hour="*/6"),
    },
}
TELEGRAM_URL = "https://api.telegram.org/bot"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
