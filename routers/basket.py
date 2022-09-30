from fastapi import (APIRouter, Depends, 
                    HTTPException, Path, 
                    Query, status)
from sqlalchemy.orm import Session
from models import Product, ItemsBasket
from database import SessionLocal
from messages import MSG
from schemas import (GetListProd, Message, 
                    GetDetailProd)
from typing import List

router = APIRouter(
    prefix="/basket",
    tags=[MSG['basket']]
)

@router.get('/all', 
            description=MSG['desk_all_prod'], 
            response_model=List[GetListProd],
            response_description=MSG['list_products'], 
            responses={status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']}},
            summary=MSG['list_products'],
            status_code=status.HTTP_200_OK, )
def all_items_basket(page: int = Query(description=MSG['page'], example=1), 
                limit: int = Query(example=30,description=MSG['limit_all_prod'])):
    with SessionLocal() as session:
        offset = (page-1) * limit
        products = session.query(ItemsBasket).order_by(ItemsBasket.created.desc()).limit(limit).offset(offset).all()
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=MSG['products_not_found'])
        return products