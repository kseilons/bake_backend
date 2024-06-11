from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    # baskets,
    # call,
    categories,
    # products,
    users
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(categories.router, prefix="/categories")
# api_router.include_router(products.router, prefix="/products")
# api_router.include_router(baskets.router, prefix="/baskets")
# api_router.include_router(call.router)

