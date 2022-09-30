from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from schemas import TokenPayload
from models import Customer
from database import SessionLocal
from settings import (TOKEN_ALGORITHM, SECRET_KEY)
from messages import MSG

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_current_user(token: str = Depends(reusable_oauth2)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=MSG['api_401_desk'],
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise credentials_exception
    with SessionLocal() as session:
        user = session.query(Customer).get(token_data.id)
    if not user:
        raise credentials_exception
    return user