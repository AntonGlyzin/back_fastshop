from fastapi import (APIRouter, Depends, 
                    HTTPException, Path, 
                    Query, status)
from models import Product, ItemsBasket, Customer
from database import SessionLocal
from messages import MSG
from schemas import (GetListBasket, Message, GetDetailProd)
from typing import List
from deps import (get_current_user, 
                    get_active_user, 
                    get_current_product)
from decimal import Decimal


router = APIRouter(
    prefix="/basket",
    tags=[MSG['basket']],
    responses={
        status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']},
        status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['not_access']}
    },
)

def get_item_product(prod):
    prod.title = prod.product.title
    prod.price = prod.product.price
    prod.photo = prod.product.photo
    prod.currency = prod.product.currency
    prod.amount = Decimal(prod.quantity) * prod.product.price

@router.get('/all', 
            description=MSG['desk_all_prod'], 
            response_model=List[GetListBasket],
            response_description=MSG['list_products'], 
            summary=MSG['list_products'],
            status_code=status.HTTP_200_OK, )
def all_items_basket(page: int = Query(description=MSG['page'], example=1), 
                    limit: int = Query(example=30,description=MSG['limit_all_prod']),
                    user: Customer = Depends(get_active_user)):
    with SessionLocal() as session:
        offset = (page-1) * limit
        products = session.query(ItemsBasket).filter_by(customer=user)\
                            .order_by(ItemsBasket.created.desc())\
                            .limit(limit).offset(offset).all()
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=MSG['products_not_found'])
        for prod in products:
            get_item_product(prod)
        return products


@router.post('/add', 
            response_model=GetListBasket,
            response_description=MSG['product'], 
            responses={status.HTTP_400_BAD_REQUEST: {'model': Message, 'description': MSG['error_add_prod']},},
            summary=MSG['desk_add_prod'],
            status_code=status.HTTP_201_CREATED,
            description=MSG['desk_add_prod'])
def add_product_basket(user: Customer = Depends(get_active_user),
                       product: Product = Depends(get_current_product),):
    with SessionLocal() as session:
        item_product = session.query(ItemsBasket).filter_by(customer=user, product=product).first()
        if product.quantity < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail=MSG['products_not_found'])
        if item_product is None:
            item_product = ItemsBasket(customer=user, product=product, quantity=1)
            session.add(item_product)
        else:
            item_product.quantity = item_product.quantity + 1

        session.commit()
        get_item_product(item_product)
        return item_product


@router.put('/minus', 
            response_model=GetListBasket,
            response_description=MSG['product'], 
            responses={status.HTTP_400_BAD_REQUEST: {'model': Message, 'description': MSG['minimum_product']},},
            summary=MSG['minus_product'],
            status_code=status.HTTP_202_ACCEPTED,
            description=MSG['minus_product'])
def minus_product_basket(user: Customer = Depends(get_active_user),
                       product: Product = Depends(get_current_product),):
    with SessionLocal() as session:
        item_product = session.query(ItemsBasket).filter_by(customer=user, product=product).first()
        if item_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MSG['not_product'])
        else:
            if item_product.quantity == 1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=MSG['minimum_product_basket'])
            item_product.quantity = item_product.quantity - 1
        session.commit()
        get_item_product(item_product)
        return item_product


@router.delete('/delete',
            response_description=MSG['product_delete_basket'], 
            responses={status.HTTP_400_BAD_REQUEST: {'model': Message, 'description': MSG['not_product']}},
            summary=MSG['delete_product'],
            status_code=status.HTTP_200_OK,
            description=MSG['delete_product'])
def delete_product_basket(user: Customer = Depends(get_active_user),
                       product: Product = Depends(get_current_product),):
    with SessionLocal() as session:
        item_product = session.query(ItemsBasket).filter_by(customer=user, product=product).first()
        if item_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MSG['not_product'])
        else:
            session.query(ItemsBasket).filter_by(customer=user, product=product).delete(synchronize_session=False)
            session.commit()
            return {
                'detail': MSG['product_delete_basket']
            }