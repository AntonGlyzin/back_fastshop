from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from messages import MSG
from database import SessionLocal
from models import Customer
from security import PasswordToken
from schemas import Token, Message
from deps import get_active_user

router = APIRouter(
    prefix="/users",
    tags=[MSG['users']]
)


@router.post('/token',
            description=MSG['auth_token_access'], 
            response_model=Token,
            response_description=MSG['success_auth'], 
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['not_access']}},
            summary=MSG['auth'],
            status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends()):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=MSG['incorrect_email_pass'])
    with SessionLocal() as session:
        user: Customer = session.query(Customer).filter_by(username=request.username).first()
    if not user:
        raise credentials_exception
    if not PasswordToken.verify_password(request.password, user.password):
        raise credentials_exception
    access_token = PasswordToken.create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get('/me',
            summary=MSG['profile'],
            status_code=status.HTTP_200_OK,
            response_description=MSG['profile'], )
def get_me(user: Customer = Depends(get_active_user)):
    ...