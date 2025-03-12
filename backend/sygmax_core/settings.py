import os
from pathlib import Path

# === БАЗОВЫЕ НАСТРОЙКИ ===

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-secret-key")

DEBUG = True  # Поменяй на False в продакшене

ALLOWED_HOSTS = ["*"]  # Измени на конкретные хосты в продакшене


# === УСТАНОВЛЕННЫЕ ПРИЛОЖЕНИЯ ===

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Микросервисы
    'apps.authentication',
    'apps.profiles',
    'apps.workspaces',
]

# === ПРОМЕЖУТОЧНОЕ ПО (MIDDLEWARE) ===

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === ОСНОВНЫЕ URL ===

ROOT_URLCONF = 'sygmax_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'sygmax_core.wsgi.application'

# === БАЗА ДАННЫХ ===

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# Для PostgreSQL (если используешь, раскомментируй)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv("POSTGRES_DB", "sygmax_db"),
#         'USER': os.getenv("POSTGRES_USER", "postgres"),
#         'PASSWORD': os.getenv("POSTGRES_PASSWORD", "password"),
#         'HOST': os.getenv("POSTGRES_HOST", "localhost"),
#         'PORT': os.getenv("POSTGRES_PORT", "5432"),
#     }
# }

# === АВТОРИЗАЦИЯ ===

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === ЛОКАЛИЗАЦИЯ ===

LANGUAGE_CODE = 'ru'  # Или 'en-us', если проект на английском
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === СТАТИКА И МЕДИА ===

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# === ЛОГИРОВАНИЕ (ОПЦИОНАЛЬНО) ===

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / "debug.log",
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

# === ПО DEFAULT ===

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
