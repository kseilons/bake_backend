import uvicorn

from app.routers import users, categories, products
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

app = FastAPI()

app.include_router(users.router)
app.include_router(categories.router,
                   prefix="/categories")
app.include_router(products.router,
                   prefix="/products")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь можно указать список разрешенных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)