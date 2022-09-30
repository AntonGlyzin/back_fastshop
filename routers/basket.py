from fastapi import (APIRouter, Depends, 
                    HTTPException, Path, 
                    Query, status)
from sqlalchemy.orm import Session
from models import Product, ItemsBasket, Customer
from database import SessionLocal
from messages import MSG
from schemas import (GetListBasket, Message)
from typing import List
from deps import get_current_user, get_active_user

router = APIRouter(
    prefix="/basket",
    tags=[MSG['basket']],
    dependencies=[Depends(get_current_user)]
)

@router.get('/all', 
            description=MSG['desk_all_prod'], 
            response_model=List[GetListBasket],
            response_description=MSG['list_products'], 
            responses={status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']}},
            summary=MSG['list_products'],
            status_code=status.HTTP_200_OK, )
def all_items_basket(page: int = Query(description=MSG['page'], example=1), 
                limit: int = Query(example=30,description=MSG['limit_all_prod']),
                user: Customer = Depends(get_active_user)):
    with SessionLocal() as session:
        offset = (page-1) * limit
        products = session.query(ItemsBasket).filter_by(customer_id=user.id)\
                            .order_by(ItemsBasket.created.desc())\
                            .limit(limit).offset(offset).all()
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=MSG['products_not_found'])
        for prod in products:
            prod.title = prod.product.title
            prod.price = prod.product.price
            prod.photo = prod.product.photo
            prod.currency = prod.product.currency
            prod.amount = prod.quantity * prod.product.price
        return products