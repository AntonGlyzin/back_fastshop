from fastapi import FastAPI
from routers import products, basket, users
from messages import MSG
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from settings import ORIGINS
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def custom_openapi():
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
        "url": "static/shop.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.include_router(products.router)
app.include_router(basket.router)
app.include_router(users.router)