from pydantic import BaseModel, Field, EmailStr, HttpUrl, StrictBool
from typing_extensions import Annotated
from typing import List
from messages import MSG
from decimal import Decimal
from datetime import datetime

class GetListProd(BaseModel):
    id: Annotated[int | None, Field(description=MSG['id'])]
    title: Annotated[str | None, Field(description=MSG['title'])]
    photo: Annotated[str | None, Field(description=MSG['photo'])]
    price: Annotated[Decimal | None, Field(description=MSG['price'])]
    currency: Annotated[str | None, Field(description=MSG['currency'])]
    class Config:
        orm_mode = True


class GetPageProd(BaseModel):
    pages: Annotated[Decimal | None, Field(description=MSG['count_pages'])]
    products: Annotated[List[GetListProd], Field(description=MSG['products'])]


class GetListBasket(GetListProd):
    quantity: Annotated[int | None, Field(description=MSG['quantity'])]
    amount: Annotated[Decimal | None, Field(description=MSG['sum'])]
    class Config:
        orm_mode = True


class GetDetailProd(GetListProd):
    description: Annotated[str | None, Field(description=MSG['desk'])]
    quantity: Annotated[int | None, Field(description=MSG['quantity'])]
    class Config:
        orm_mode = True


class Message(BaseModel):
    detail: Annotated[str | None, Field(description=MSG['desk_error'])]

class SuccessMessage(BaseModel):
    detail: Annotated[str | None, Field(description=MSG['success_message'])]


class Token(BaseModel):
    access_token: Annotated[str | None, Field(description=MSG['access_token'])]
    token_type: Annotated[str | None, Field(description=MSG['type_token'])]


class TokenPayload(BaseModel):
    id: int
    exp: int


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


class GetItemOrder(BaseModel):
    id: Annotated[int | None, Field(description=MSG['id'])]
    title: Annotated[str | None, Field(description=MSG['title'])]
    photo: Annotated[str | None, Field(description=MSG['photo'])]
    quantity: Annotated[int | None, Field(description=MSG['quantity'])]
    price: Annotated[Decimal | None, Field(description=MSG['price'])]
    currency: Annotated[str | None, Field(description=MSG['currency'])]
    amount: Annotated[Decimal | None, Field(description=MSG['sum'])]


class GetOrders(BaseModel):
    id: Annotated[int | None, Field(description=MSG['id'])]
    products: Annotated[List[GetItemOrder] | None, Field(description=MSG['products'])]
    customer: Annotated[GetProfile | None, Field(description=MSG['profile'])]
    amount: Annotated[Decimal | None, Field(description=MSG['sum'])]
    payd: Annotated[Decimal | None, Field(description=MSG['payd'])]
    currency: Annotated[str | None, Field(description=MSG['currency'])]
    created: Annotated[datetime | None, Field(description=MSG['date'])]
    