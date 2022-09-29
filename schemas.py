from pydantic import BaseModel, Field
from typing_extensions import Annotated
from messages import MSG

class GetProdUser(BaseModel):
    id: Annotated[int | None, Field(description=MSG['id'])]
    title: Annotated[str | None, Field(description=MSG['title'])]
    photo: Annotated[str | None, Field(description=MSG['photo'])]
    description: Annotated[str | None, Field(description=MSG['desk'])]
    price: Annotated[float | None, Field(description=MSG['price'])]
    currency: Annotated[str | None, Field(description=MSG['currency'])]
    quantity: Annotated[int | None, Field(description=MSG['quantity'])]

    class Config:
        orm_mode = True


class Message(BaseModel):
    detail: Annotated[str | None, Field(description=MSG['desk_error'])]