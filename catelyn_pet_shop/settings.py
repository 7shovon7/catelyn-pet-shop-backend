from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'https://www.catelynpetshop.com',
    'https://catelynpetshop.com',
    'https://*.catelynpetshop.com',
    'https://*.shovon.info',
]

CSRF_COOKIE_SECURE = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djoser',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
    'markdownx',
    'django_filters',

    'core',
    'product',
    'order',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'catelyn_pet_shop.urls'

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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'catelyn_pet_shop.wsgi.application'


if os.getenv('DB_TYPE', 'LOCAL') == 'LOCAL':
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT', '5432')
else:
    # REMOTE_* vars are not needed in production
    DB_NAME = os.environ.get('REMOTE_DB_NAME')
    DB_USER = os.environ.get('REMOTE_DB_USER')
    DB_PASSWORD = os.environ.get('REMOTE_DB_PASSWORD')
    DB_HOST = os.environ.get('REMOTE_DB_HOST')
    DB_PORT = os.environ.get('REMOTE_DB_PORT', '5432')


DATABASES = {
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database.sqlite3',
    },
    'sqlite3-prod-copy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'prod_db.sqlite3',
    },
}
# DB_KEY var is not needed in production
DB_KEY = os.getenv('DB_KEY') if (os.getenv('DB_KEY') is not None and os.getenv('DB_KEY') in DATABASES) else 'postgres'
DATABASES['default'] = DATABASES[DB_KEY]


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1800/hour',
        'user': '5000/day',
    },
}

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
   "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
   "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
   "TOKEN_OBTAIN_SERIALIZER": "core.serializers.TokenObtainPairSerializer"
}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',
        'current_user': 'core.serializers.UserSerializer',
        'user': 'core.serializers.UserSerializer',
        'password_reset': 'djoser.serializers.SendEmailResetSerializer',
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
        'password_change': 'djoser.serializers.SetPasswordSerializer',
    },
    'EMAIL': {
        'password_reset': 'djoser.email.PasswordResetEmail',
    },
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'LOGOUT_ON_PASSWORD_CHANGE': False,
}

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# # Amazon S3
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_FILE_OVERWRITE = False
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# MardownX
# MARKDOWNX_MEDIA_PATH = 'markdownx/uploads/'  # where uploaded images will be stored
# MARKDOWNX_URLS_PATH = '/markdownx/uploads/'  # URL path for accessing uploaded images

# Optional: Additional settings for Markdownx
MARKDOWNX_EDITOR_RESIZABLE = True
MARKDOWNX_UPLOAD_MAX_SIZE = 5242880  # 5MB
# MARKDOWNX_IMAGE_MAX_SIZE = {'size': (1000, 1000), 'quality': 90}  # max size for image uploads


# Global constants
# K_ADMIN_USER_ROLE = 'ADMIN'
K_MANAGER_USER_ROLE = 'MANAGER'
K_CUSTOMER_USER_ROLE = 'CUSTOMER'
# K_STAFF_USER_ROLE = 'STAFF'

K_CUSTOM_USER_ROLES = [
    # K_ADMIN_USER_ROLE,
    K_MANAGER_USER_ROLE,
    K_CUSTOMER_USER_ROLE,
    # K_STAFF_USER_ROLE,
]

K_STATUS_PENDING = 'PENDING'
K_STATUS_PROCESSING = 'PROCESSING'
K_STATUS_COMPLETED = 'COMPLETED'
K_STATUS_CANCELLED = 'CANCELLED'

K_ORDER_STATUS_LIST = [
    K_STATUS_PENDING,
    K_STATUS_PROCESSING,
    K_STATUS_COMPLETED,
    K_STATUS_CANCELLED,
]
