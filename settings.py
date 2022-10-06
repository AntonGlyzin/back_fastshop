import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
import firebase_admin
from firebase_admin import credentials
from fastapi_mail import ConnectionConfig

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
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastshop'
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24 # 24 hours
CURRENCY = 'руб.'
LANGUAGE_CODE = 'ru'

CONFIG_EMAIL ={
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD'),
    'MAIL_FROM': os.environ.get('MAIL_FROM'),
    'MAIL_PORT': 465,
    'MAIL_SERVER': 'smtp.yandex.ru',
    'CALLBACK_SITE': 'http://127.0.0.1:8000'
}
