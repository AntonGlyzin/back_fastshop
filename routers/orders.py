from fastapi import (APIRouter, Depends, 
                    HTTPException, Path, 
                    Query, status)
from models import Product, ItemsBasket, Customer, Order, ProductOrder
from database import SessionLocal
from messages import MSG
from schemas import (Message, GetItemOrder, GetOrders)
from typing import List
from deps import (get_active_user, get_current_product)
from decimal import Decimal

router = APIRouter(
    prefix="/orders",
    tags=[MSG['orders']],
    responses={
        status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['not_access']}
    },
)

def create_orders(orders):
    list_orders = []
    for ord1 in orders:
        o = dict(
            id = ord1.id,
            amount =  ord1.amount,
            payd =  ord1.payd,
            currency = ord1.currency,
            created = ord1.created
        )
        list_prod = []
        for prod in ord1.products:
            p = dict(
                id = prod.id,
                title = prod.product.title,
                quantity = prod.quantity,
                currency = prod.currency,
                amount = prod.amount,
                price = prod.product.price,
                photo = prod.product.photo,
            )
            list_prod.append(p)
        o['products'] = list_prod
        o['customer'] = dict(
            id = ord1.customer.id,
            username = ord1.customer.username,
            email = ord1.customer.email,
            first_name = ord1.customer.first_name,
            last_name = ord1.customer.last_name,
            photo = ord1.customer.photo,
        )
        list_orders.append(o)
    return list_orders


@router.get('/my-orders', 
            response_model=List[GetOrders],
            description=MSG['desk_orders'], 
            summary=MSG['my_orders'],
            status_code=status.HTTP_200_OK, 
            response_description=MSG['orders'],
            responses={
                status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']}},)
def all_active_orders(page: int = Query(description=MSG['page'], example=1), 
                    limit: int = Query(example=30,description=MSG['limit_all_prod']),
                    user: Customer = Depends(get_active_user),
                    order_status: int = Query(description=MSG['status_orders'])):
    offset = (page-1) * limit
    with SessionLocal() as session:
        orders = session.query(Order).filter_by(customer_id=user.id, status=order_status)\
                            .order_by(Order.created.desc())\
                            .limit(limit).offset(offset).all()
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=MSG['api_desk_not_found'])
        return create_orders(orders)


@router.post('/create-orders', 
            response_model=GetOrders,
            description=MSG['desk_order_create'], 
            summary=MSG['create_order'],
            status_code=status.HTTP_201_CREATED, 
            response_description=MSG['order'],
            responses={
                status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']}},)
def create_order(user: Customer = Depends(get_active_user)):
    with SessionLocal() as session:
        items_basket = session.query(ItemsBasket).filter_by(customer=user).all()
        if not items_basket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=MSG['api_desk_not_found_basket'])
        order = Order(
            customer_id=user.id,
            amount=0
        )
        all_sum = 0
        for item in items_basket:
            p = ProductOrder(
                product_id=item.product.id,
                currency=item.product.currency,
                amount=item.product.price*item.quantity,
                quantity=item.quantity,
            )
            all_sum += item.product.price*item.quantity
            order.products.append(p)
        order.amount = all_sum
        session.add_all([order, ])
        session.query(ItemsBasket).filter_by(customer_id=user.id).delete()
        session.commit()
        return create_orders([order]).pop()