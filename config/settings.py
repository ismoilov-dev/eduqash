import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps directory to python path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

try:
    import environ
    env = environ.Env(
        DEBUG=(bool, True),
        ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1', '0.0.0.0']),
        FAKE_PAYMENT=(bool, True),
    )
    env_file = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_file):
        environ.Env.read_env(env_file)
except ImportError:
    class DummyEnv:
        def __call__(self, key, default=None):
            return os.getenv(key, default)
        def bool(self, key, default=False):
            val = os.getenv(key, str(default))
            return val.lower() in ('true', '1', 'yes')
        def int(self, key, default=0):
            return int(os.getenv(key, default))
        def list(self, key, default=None):
            val = os.getenv(key)
            return val.split(',') if val else (default or [])
        def db(self, key, default=None):
            return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
    env = DummyEnv()

SECRET_KEY = env('SECRET_KEY', default='django-insecure-eduqash-pro-v2-super-secret-key')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition
INSTALLED_APPS = [
    'unfold',  # Unfold admin dashboard must be placed before django.contrib.admin
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'daphne',  # ASGI WebSocket support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # Third party packages
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'corsheaders',
    'channels',

    # Project local apps
    'apps.core',
    'apps.accounts',
    'apps.centers',
    'apps.courses',
    'apps.exams',
    'apps.quizzes',
    'apps.ai_assistant',
    'apps.payments',
    'apps.certificates',
    'apps.chat',
    'apps.reviews',
    'apps.notifications',
    'apps.analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
ASGI_APPLICATION = 'config.asgi.application'

# Database
# Default to PostgreSQL, with fallback to SQLite for local development
if hasattr(env, 'db'):
    DATABASES = {
        'default': env.db(
            'DATABASE_URL',
            default=f"postgres://{env('DB_USER', default='postgres')}:{env('DB_PASSWORD', default='postgres')}@{env('DB_HOST', default='localhost')}:{env('DB_PORT', default='5432')}/{env('DB_NAME', default='eduqash_db')}"
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# SimpleJWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# OpenAPI Swagger Settings (drf-spectacular)
SPECTACULAR_SETTINGS = {
    'TITLE': 'EDUQASH PRO V2.0 API',
    'DESCRIPTION': 'Production-ready REST API for EDUQASH PRO V2.0 educational platform.',
    'VERSION': '2.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# Channels Channel Layer (Redis)
REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}

# Celery Settings
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# CORS Config
CORS_ALLOW_ALL_ORIGINS = True

# Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='EDUQASH PRO <noreply@eduqash.com>')

# AI Provider Credentials
AI_PROVIDER = env('AI_PROVIDER', default='groq')
MEGALLM_API_URL = env('MEGALLM_API_URL', default='https://api.megallm.uz/v1')
MEGALLM_API_KEY = env('MEGALLM_API_KEY', default='')
GROQ_API_KEY = env('GROQ_API_KEY', default='')

# Telegram Bot API
TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN', default='')

# Payment Mock Setting
FAKE_PAYMENT = env.bool('FAKE_PAYMENT', default=True)

# Django Unfold Admin Configuration
UNFOLD = {
    "SITE_HEADER": "EDUQASH PRO V2.0 Admin",
    "SITE_TITLE": "EDUQASH PRO Admin",
    "SITE_SYMBOL": "school",
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": False,
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "238 242 255",
            "100": "224 231 255",
            "200": "199 210 254",
            "300": "165 180 252",
            "400": "129 140 248",
            "500": "99 102 241",
            "600": "79 70 229",
            "700": "67 56 202",
            "800": "55 48 163",
            "900": "49 46 129",
            "950": "30 27 75",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "User & Auth Management",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": lambda request: "/admin/accounts/user/",
                    },
                ],
            },
            {
                "title": "Learning Centers & Courses",
                "separator": True,
                "items": [
                    {
                        "title": "Learning Centers",
                        "icon": "store",
                        "link": lambda request: "/admin/centers/learningcenter/",
                    },
                    {
                        "title": "Courses",
                        "icon": "book",
                        "link": lambda request: "/admin/courses/course/",
                    },
                    {
                        "title": "Lessons",
                        "icon": "menu_book",
                        "link": lambda request: "/admin/courses/lesson/",
                    },
                    {
                        "title": "Homework Submissions",
                        "icon": "assignment",
                        "link": lambda request: "/admin/courses/homeworksubmission/",
                    },
                ],
            },
            {
                "title": "Exams & Quizzes",
                "separator": True,
                "items": [
                    {
                        "title": "Exams",
                        "icon": "quiz",
                        "link": lambda request: "/admin/exams/exam/",
                    },
                    {
                        "title": "Exam Attempts",
                        "icon": "assignment_turned_in",
                        "link": lambda request: "/admin/exams/examattempt/",
                    },
                    {
                        "title": "Quizzes",
                        "icon": "help",
                        "link": lambda request: "/admin/quizzes/quiz/",
                    },
                    {
                        "title": "Leaderboards",
                        "icon": "leaderboard",
                        "link": lambda request: "/admin/quizzes/leaderboard/",
                    },
                ],
            },
            {
                "title": "Payments & Certificates",
                "separator": True,
                "items": [
                    {
                        "title": "Payments",
                        "icon": "payments",
                        "link": lambda request: "/admin/payments/payment/",
                    },
                    {
                        "title": "Promo Codes",
                        "icon": "local_offer",
                        "link": lambda request: "/admin/payments/promocode/",
                    },
                    {
                        "title": "Certificates",
                        "icon": "verified",
                        "link": lambda request: "/admin/certificates/certificate/",
                    },
                ],
            },
            {
                "title": "Community & Support",
                "separator": True,
                "items": [
                    {
                        "title": "Conversations",
                        "icon": "forum",
                        "link": lambda request: "/admin/chat/conversation/",
                    },
                    {
                        "title": "Reviews",
                        "icon": "star",
                        "link": lambda request: "/admin/reviews/review/",
                    },
                    {
                        "title": "Notifications",
                        "icon": "notifications",
                        "link": lambda request: "/admin/notifications/notification/",
                    },
                ],
            },
        ],
    },
}
