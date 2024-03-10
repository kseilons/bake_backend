import uvicorn

from app.routers import users, categories, property_info, change_product
from fastapi import FastAPI

app = FastAPI()

app.include_router(users.router)
app.include_router(categories.router,
                   prefix="/categories")
app.include_router(property_info.router,
                   prefix="/property_info")
app.include_router(change_product.router,
                   prefix="/schem_product")
# app.include_router(offers_property.router,
#                    prefix="/offers-props")
