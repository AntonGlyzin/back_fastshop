import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
import firebase_admin
from firebase_admin import credentials

import dj_database_url

load_dotenv(dotenv_path)
BASE_DIR = dirname(__file__)

FIREBASE_STORAGE = credentials.Certificate(os.path.join(BASE_DIR, 'google-service.json'))
firebase_admin.initialize_app(FIREBASE_STORAGE, {
    'storageBucket': os.environ.get('BUCKET_STORAGE_NAME')
})

SECRET_KEY = os.environ.get("SECRET_KEY")
ORIGINS = [
    'http://localhost'
]
# DATABASE_URL = 'sqlite:///fastshop.db'
DATABASE_URL = os.environ.get('DATABASE_URL') 
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24 # 24 hours
CURRENCY = 'руб.'
CALLBACK_MAIL = os.environ.get('MAIL_ADMIN') # предупреждение для продавца о заказе

CONFIG_EMAIL ={
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
    'MAIL_FROM': os.environ.get('MAIL_FROM'),
    'MAIL_PORT': 465,
    'MAIL_SERVER': 'smtp.yandex.ru',
    'CALLBACK_SITE': 'http://127.0.0.1:8083',
}


DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8083',
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8083',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'shop.apps.ShopConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

DATABASES = {
    'default': dj_database_url.parse(url=os.environ.get('DATABASE_URL'))
}

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

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = 'utils.FireBase'
FIREBASE_URL = 'https://storage.googleapis.com/' + os.environ.get('BUCKET_STORAGE_NAME') 