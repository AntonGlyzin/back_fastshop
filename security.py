from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from settings import (TOKEN_ALGORITHM, 
                        ACCESS_TOKEN_EXPIRE_MINUTES,
                        SECRET_KEY)


class PasswordToken:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def create_access_token(data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expire, "id": str(data['id'])}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cla, password: str) -> str:
        return cla.pwd_context.hash(password)
