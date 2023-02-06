from fastapi import (APIRouter, Depends, 
                    HTTPException, Path, 
                    Query, status)
from sqlalchemy.orm import Session
from models import Product
from database import SessionLocal
from messages import MSG
from schemas import (GetListProd, Message, 
                    GetDetailProd, GetPageProd)
from typing import List
import math

class LogicProduct:

    # получение всех товаров по странично
    @staticmethod
    def all_products(page, limit):
        with SessionLocal() as session:
            count_products = session.query(Product).count()     
            if not count_products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=MSG['products_not_found'])
            offset = (page-1) * limit
            products = (session.query(Product)
                                .filter(Product.is_active)
                                .order_by(Product.created.desc())
                                .limit(limit).offset(offset)
                                .all())    
            count_pages = math.ceil(count_products/limit)
        return {'pages': count_pages, 'products': products}

    # полусение товара по ИД
    @staticmethod
    def detail_product(id):
        with SessionLocal() as session:
            products = (session.query(Product)
                                .filter(Product.is_active, Product.id==id)
                                .first())
            if not products:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=MSG['products_not_found'])
        return products


