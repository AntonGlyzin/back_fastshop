from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing_extensions import Annotated
from messages import MSG


class GetListProd(BaseModel):
    id: Annotated[int | None, Field(description=MSG['id'])]
    title: Annotated[str | None, Field(description=MSG['title'])]
    photo: Annotated[str | None, Field(description=MSG['photo'])]
    price: Annotated[float | None, Field(description=MSG['price'])]
    currency: Annotated[str | None, Field(description=MSG['currency'])]
    class Config:
        orm_mode = True


class GetListBasket(GetListProd):
    quantity: Annotated[int | None, Field(description=MSG['quantity'])]
    amount: Annotated[int | None, Field(description=MSG['sum'])]
    class Config:
        orm_mode = True


class GetDetailProd(GetListProd):
    description: Annotated[str | None, Field(description=MSG['desk'])]
    quantity: Annotated[int | None, Field(description=MSG['quantity'])]
    class Config:
        orm_mode = True


class Message(BaseModel):
    detail: Annotated[str | None, Field(description=MSG['desk_error'])]


class Token(BaseModel):
    access_token: Annotated[str | None, Field(description=MSG['access_token'])]
    token_type: Annotated[str | None, Field(description=MSG['type_token'])]


class TokenPayload(BaseModel):
    id: int


class GetProfile(BaseModel):
    id: Annotated[int | None, Field(description=MSG['id'])]
    username: Annotated[str | None, Field(description=MSG['username'])]
    email: Annotated[EmailStr | None, Field(description=MSG['email'])]
    first_name: Annotated[str | None, Field(description=MSG['first_name'])]
    last_name: Annotated[str | None, Field(description=MSG['last_name'])]
    photo: Annotated[str | None, Field(description=MSG['photo'])]


class GetPhotoProfile(BaseModel):
    url_photo: Annotated[str, Field(description=MSG['photo'])]


class RegistrationCustomer(BaseModel):
    username: Annotated[str, Field(description=MSG['username'])]
    email: Annotated[EmailStr, Field(description=MSG['email'])]
    first_name: Annotated[str, Field(description=MSG['first_name'])]
    last_name: Annotated[str, Field(description=MSG['last_name'])]
    password1: Annotated[str, Field(description=MSG['password'])]
    password2: Annotated[str, Field(description=MSG['password'])]