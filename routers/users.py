from fastapi import (APIRouter, Depends, status, 
                    HTTPException, UploadFile, File, Form)
from fastapi.security import OAuth2PasswordRequestForm
from messages import MSG
from database import SessionLocal
from models import Customer
from security import PasswordToken
from schemas import (Token, Message, GetProfile, 
                    GetPhotoProfile, RegistrationCustomer)
from deps import get_active_user
from settings import BASE_DIR
from utils import FireBaseStorage
from pydantic import EmailStr
import os

router = APIRouter(
    prefix="/users",
    tags=[MSG['users']],
    
)

@router.post('/registration',
            # description=MSG['auth_token_access'], 
            # response_model=RegistrationCustomer,
            response_description=MSG['success_regist'], 
            summary=MSG['registration'],
            status_code=status.HTTP_201_CREATED,
            responses={status.HTTP_400_BAD_REQUEST: {'model': Message, 'description': MSG['error_reg']}},)
def registration(username: str = Form(description=MSG['username']),
                email: EmailStr = Form(description=MSG['email']),
                first_name: str = Form(description=MSG['first_name']), 
                last_name: str = Form(description=MSG['last_name']),
                password1: str = Form(description=MSG['password']),
                password2: str = Form(description=MSG['password'])):
    if password1 != password2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['not_eq_pass'])
    with SessionLocal() as session:
        user = session.query(Customer).filter_by(email=email).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['reapit_email'])
        user = session.query(Customer).filter_by(username=username).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['reapit_username'])
        customer = Customer(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=PasswordToken.get_password_hash(password1)
        )
        session.add(customer)
        session.commit()


@router.post('/token',
            description=MSG['auth_token_access'], 
            response_model=Token,
            response_description=MSG['success_auth'], 
            summary=MSG['auth'],
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}},)
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
            response_description=MSG['profile'],
            response_model=GetProfile, 
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}})
def get_me(user: Customer = Depends(get_active_user)):
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'photo': user.photo
    }

@router.put('/set-photo',
            summary=MSG['set_photo_profile'],
            response_description=MSG['link_photo'], 
            status_code=status.HTTP_202_ACCEPTED,
            response_model=GetPhotoProfile,
            responses={status.HTTP_400_BAD_REQUEST: {'model': Message, 'description': MSG['inccorect_file']},
                        status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}},)
def set_photo_profile(user: Customer = Depends(get_active_user),
                    photo: UploadFile = File(description=MSG['photo_profile'])):
    if not 'image' in photo.content_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['need_image'])
    
    file_size: int = photo.file.seek(0, os.SEEK_END) / 1024 #Kb
    if file_size > 1024*3: #если больше 3 Mb
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['error_size_photo'])

    with photo.file as file:
        dist = f"fastshop/{user.username}/{photo.filename}"
        url = FireBaseStorage.get_link_file(file.read(), dist, photo.content_type)
    with SessionLocal() as session:
        session.query(Customer).filter_by(id=user.id).update({Customer.photo: url})
        session.commit()
        return {
            'url_photo': url
        }
    


        
