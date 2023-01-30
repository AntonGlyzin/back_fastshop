from datetime import datetime
from typing import List
import strawberry
from models import Product
from logicgraphql import get_product_by_title

@strawberry.type
class Products:
    id: int
    title: str
    photo: str
    description: str
    price: float
    currency: str
    quantity: int
    created: datetime
    updated: datetime


@strawberry.type
class Query:
    get_product_by_title: List[Products] = strawberry.field(resolver=get_product_by_title)


