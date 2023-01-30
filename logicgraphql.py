from database import SessionLocal
from fastapi import (HTTPException, status)
from models import Product
from database import SessionLocal
from messages import MSG

def get_product_by_title(title: str):
    with SessionLocal() as session:
        products = (session.query(Product)
                            .filter(Product.title.like('%{}%'.format(title)))
                            .all())
    return products
