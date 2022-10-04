import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
import firebase_admin
from firebase_admin import credentials
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
DATABASE_URL = 'sqlite:///fastshop.db'
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24 # 24 hours
CURRENCY = 'руб.'
LANGUAGE_CODE = 'ru'
