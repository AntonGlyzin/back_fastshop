from fastapi import (APIRouter, Path, 
                    Query, status)
from messages import MSG
from schemas import (Message, GetDetailProd, GetPageProd)
from logics.product import LogicProduct

router = APIRouter(
    prefix="/products",
    tags=[MSG['products']]
)

@router.get('/all', 
            description=MSG['desk_all_prod'], 
            response_model=GetPageProd,
            response_description=MSG['list_products'], 
            responses={status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']}},
            summary=MSG['list_products'],
            status_code=status.HTTP_200_OK, )
def all_products(page: int = Query(description=MSG['page'], example=1), 
                limit: int = Query(example=30,description=MSG['limit_all_prod'])):
    return LogicProduct.all_products(page,limit)


@router.get('/{id}', 
            response_model=GetDetailProd,
            response_description=MSG['product'], 
            responses={status.HTTP_404_NOT_FOUND: {'model': Message, 'description': MSG['api_desk_not_found']}},
            summary=MSG['product'],
            status_code=status.HTTP_200_OK,
            description=MSG['desk_detail_prod'])
def detail_product(id: int = Path(description=MSG['id'], example=1)):
    return LogicProduct.detail_product(id)


