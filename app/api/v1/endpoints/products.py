import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.auth import current_active_user, current_superuser
from app.products.deps import is_valid_product, is_valid_product_id, product_valid, product_valid_by_parser
from app.products.schemas import IProductCreate, IProduct, IProductFilterParams, IProductList, IProductPreview, IProductUpdate
from app.products import service
from app.products.utils import get_product_filter_params
from app.products.crud import crud_product
router = APIRouter(tags=['products'])


logger = logging.getLogger(__name__)


@router.post("/", status_code=201)
async def create_product(prod: IProductCreate = Depends(product_valid),
                        current_user: User = Depends(current_superuser)
                        ) -> IProduct:
    """
    Создает новый продукт в базе данных. В preview_img, images, files передаются
    фотки из input. Images и files не являются обязательными.
    """
    result = await service.create(prod)
    logger.info(f"Продукт успешно создан: {result}")
    return result

@router.post("/parser", status_code=201)
async def create_product_by_parser(prod: IProductCreate = Depends(product_valid_by_parser),
                        current_user: User = Depends(current_superuser)
                        ) -> IProduct:
    """
    Метод для создания продукта из парсера с сайта.
    """
    result = await service.create(prod)
    logger.info(f"Продукт успешно создан: {result}")
    return result


@router.patch("/{product_id}")
async def update_product_details(
    product_new: IProductUpdate,
    product: int = Depends(is_valid_product),
    current_user: User = Depends(current_superuser)
) -> IProduct:
    return await service.update(product, product_new)


@router.delete("/{product_id}")
async def delete_product(product_id: int = Depends(is_valid_product_id),
                        current_user: User = Depends(current_superuser)):

    return await service.delete(product_id)


@router.get("/")
async def get_products(
    params: IProductFilterParams = Depends(get_product_filter_params)
) -> IProductList:
    return await service.get_multi_filtered(params)


@router.get("/{product_id}")
async def get_product(product_id: int = Depends(is_valid_product_id)) -> IProduct:
    return await service.get_by_id(product_id)


# @router.get("/search/", response_model=schemas.ProductSearchList)
# async def search(query: str, db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
#     total_pages, total_count, products = await controller.search_products(db, query, limit, offset)
#     if products:
#         return schemas.ProductSearchList(
#             total_pages=total_pages,
#             total_count=total_count,
#             products=products)
#     else:
#         raise HTTPException(status_code=404, detail="No products found")