from fastapi import (APIRouter, Depends, 
                    HTTPException, Path, 
                    Query, status)
from models import Product, ItemsBasket, Customer, Order, ProductOrder
from database import SessionLocal
from messages import MSG
from schemas import (Message, GetItemOrder)
from typing import List
from deps import (get_active_user, get_current_product)
from decimal import Decimal

router = APIRouter(
    prefix="/orders",
    tags=[MSG['orders']],
    responses={
        status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']},
        status.HTTP_401_UNAUTHORIZED: {'model': Message, 'description': MSG['not_access']}
    },
)

@router.get('/my-orders', 
            response_model=List[GetItemOrder],
            description=MSG['desk_orders'], 
            summary=MSG['my_orders'],
            status_code=status.HTTP_200_OK, 
            response_description=MSG['orders'])
def all_active_orders(page: int = Query(description=MSG['page'], example=1), 
                    limit: int = Query(example=30,description=MSG['limit_all_prod']),
                    user: Customer = Depends(get_active_user),
                    status: bool = Query(description=MSG['status_orders'])):
    ...

# @router.get('/my-orders', 
#             response_model=List[GetItemOrder],
#             response_description=MSG['archive_orders'], 
#             summary=MSG['archive_orders'],
#             status_code=status.HTTP_200_OK, )
# def all_active_orders(page: int = Query(description=MSG['page'], example=1), 
#                     limit: int = Query(example=30,description=MSG['limit_all_prod']),
#                     user: Customer = Depends(get_active_user)):
#     ...