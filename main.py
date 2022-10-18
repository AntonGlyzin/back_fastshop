import os
from importlib.util import find_spec
from fastapi import FastAPI
from routers import products, basket, users, orders
from messages import MSG
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from settings import ORIGINS
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from django.core.wsgi import get_wsgi_application
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
app = FastAPI()
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", WSGIMiddleware(application))
app.mount("/static",
    StaticFiles(
         directory=os.path.normpath(
              os.path.join(find_spec("django.contrib.admin").origin, '..',"static/")
         )
   ),
   name="static",
)

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
app.include_router(orders.router)