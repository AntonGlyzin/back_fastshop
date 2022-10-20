from fastapi import (APIRouter, Depends, status, 
                    HTTPException, UploadFile, File, Form)
from fastapi.security import OAuth2PasswordRequestForm
from messages import MSG
from database import SessionLocal
from models import Customer
from security import PasswordToken
from schemas import (Token, Message, GetProfile, 
                    GetPhotoProfile, SuccessMessage)
from deps import get_active_user
from settings import BASE_DIR
from utils import FireBaseStorage, EmailWorked
from pydantic import EmailStr, SecretStr
import os
import uuid


router = APIRouter(
    prefix="/users",
    tags=[MSG['users']],
    
)

@router.get('/confirm-registration', 
            status_code=status.HTTP_200_OK, 
            include_in_schema=False)
def confirm_registration(key: str):
    with SessionLocal() as session:
        user = session.query(Customer).filter_by(key=key, type_key='registration').first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['not_user'])
        session.query(Customer).filter_by(id=user.id).update({
            Customer.key: None,
            Customer.is_active: True,
            Customer.type_key: None
        })
        session.commit()
    return {
        'detail': MSG['success_confirm_registration']
    }


@router.get('/reset-password', 
            status_code=status.HTTP_200_OK, 
            include_in_schema=False)
def reset_password(key: str):
    with SessionLocal() as session:
        user = session.query(Customer).filter_by(key=key, type_key='reset_password').first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['not_user'])
        key = uuid.uuid4().hex[0:5]
        session.query(Customer).filter_by(id=user.id).update({
            Customer.key: None,
            Customer.password: PasswordToken.get_password_hash(key),
            Customer.type_key: None
        })
        session.commit()
        EmailWorked.send_password(user.email, key)    
    return {
        'detail': MSG['success_reset_pass']
    }


@router.post('/registration',
            response_description=MSG['success_regist'], 
            summary=MSG['registration'],
            status_code=status.HTTP_201_CREATED,
            response_model=SuccessMessage,
            responses={status.HTTP_400_BAD_REQUEST: {'model': Message, 'description': MSG['error_reg']}},)
def registration(username: str = Form(description=MSG['username']),
                email: EmailStr = Form(description=MSG['email']),
                first_name: str = Form(description=MSG['first_name']), 
                last_name: str = Form(description=MSG['last_name']),
                password1: str = Form(description=MSG['password']),
                password2: str = Form(description=MSG['password'])):
    key = uuid.uuid4().hex
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
            password=PasswordToken.get_password_hash(password1),
            key=key,
            type_key='registration'
        )
        session.add(customer)
        session.commit()
    EmailWorked.send_confirm_registration(email, key)    
    return {
        'detail': MSG['send_message_email']
    }

    
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
        user: Customer = session.query(Customer).filter_by(username=request.username, is_banned=False, is_active=True).first()
    if not user:
        raise credentials_exception
    if not PasswordToken.verify_password(request.password, user.password):
        raise credentials_exception
    access_token = PasswordToken.create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.put('/confirm-reset-password',
            response_description=MSG['success_message'], 
            summary=MSG['reset_password'],
            status_code=status.HTTP_200_OK,
            response_model=SuccessMessage)
def confirm_reset_password(email: EmailStr = Form(description=MSG['email'])):
    with SessionLocal() as session:
        user = session.query(Customer).filter_by(email=email, is_banned=False, is_active=True).first()
        if user:
            key = uuid.uuid4().hex
            session.query(Customer).filter_by(email=email, id=user.id).update({
                Customer.key: key,
                Customer.type_key: 'reset_password'
            })
            session.commit()
            EmailWorked.send_reset_password(email, key)
    return {
        'detail': MSG['return_confirm_reset_pass']
    }


@router.put('/change-password',
            response_description=MSG['success_message'], 
            summary=MSG['change_password'],
            status_code=status.HTTP_200_OK,
            response_model=SuccessMessage,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}})
def change_password(user: Customer = Depends(get_active_user),
                    old_password: str = Form(description=MSG['old_password']),
                    new_password1: str = Form(description=MSG['new_password']),
                    new_password2: str = Form(description=MSG['new_password'])):
    if new_password2 != new_password2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['not_eq_pass'])
    with SessionLocal() as session:
        if not PasswordToken.verify_password(old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['error_old_password'])
        session.query(Customer).filter_by(id=user.id).update({
            Customer.password: PasswordToken.get_password_hash(new_password1)
        })
        session.commit()
            
        EmailWorked.confirm_change_password(user.email)
    return {
        'detail': MSG['return_change_pass']
    }


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
    
    with photo.file as file:
        file_buffer = file.read()
        file_size: int = len(file_buffer) / 1024#Kb
        if file_size > 1024*3: #если больше 3 Mb
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['error_size_photo'])

        dist = f"fastshop/users/{user.username}/{photo.filename}"
        url = FireBaseStorage.get_link_file(file_buffer, dist, photo.content_type)
        with SessionLocal() as session:
            session.query(Customer).filter_by(id=user.id).update({Customer.photo: url})
            session.commit()
            return {
                'url_photo': url
            }
    

@router.put('/change-name-user',
            response_description=MSG['success_message'], 
            summary=MSG['change_name_user'],
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}},)
def change_name_user(user: Customer = Depends(get_active_user),
                    first_name: str = Form(description=MSG['first_name']),
                    last_name: str = Form(description=MSG['last_name'])):
    with SessionLocal() as session:
        session.query(Customer).filter_by(id=user.id).update({
            Customer.first_name: first_name,
            Customer.first_name: last_name,
        })
        session.commit()


@router.post('/add-point-peace',
            response_description=MSG['success_message'], 
            summary=MSG['add_point_paece'],
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}},)
def add_point_paece(user: Customer = Depends(get_active_user),
                    desc_peace: str = Form(description=MSG['point_peace'])):
    with SessionLocal() as session:
        ...


@router.put('/change-point-peace',
            response_description=MSG['success_message'], 
            summary=MSG['change_point_peace'],
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}},)
def change_point_peace(user: Customer = Depends(get_active_user),
                    id_peace: int = Form(description=MSG['id_point_peace']),
                    new_desc_peace: str = Form(description=MSG['point_peace'])):
    with SessionLocal() as session:
        ...


@router.delete('/delete-point-peace',
            response_description=MSG['success_message'], 
            summary=MSG['delete_point_peace'],
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['no_auth']}},)
def change_point_peace(user: Customer = Depends(get_active_user),
                    id_peace: int = Form(description=MSG['id_point_peace'])):
    with SessionLocal() as session:
        ...