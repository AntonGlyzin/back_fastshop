from fastapi import Depends, FastAPI, HTTPException
from routers import products
from messages import MSG
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=MSG['shop_name'],
        description=MSG['shop_desk'],
        version="2.5.0",
        routes=app.routes,
        contact={
            "url": "http://127.0.0.1:8000/redoc",
        },
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(products.router)