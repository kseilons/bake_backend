import logging
from typing import List

from app.crud.categories import get_category_id
from app.schemas import products as schemas
from app.crud import products as controller
from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.auth.schemas import User
from app.utils.dependecies import verify_admin_user

router = APIRouter(tags=['products'])


logger = logging.getLogger(__name__)


@router.post("/", status_code=201)
async def create_product(prod: schemas.ProductCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(verify_admin_user)):
    """
    Создает новый продукт в базе данных. В preview_img, images, files передаются
    фотки из input. Images и files не являются обязательными. Если не заполнить
    short_desctiption, поле возьмется из desctiption первые 150 символов.
    """
    db_product = await controller.create_product(db, prod)
    logger.info(f"Продукт успешно создан: {db_product}")
    return db_product

@router.post("/parser", status_code=201)
async def create_product_parser(prod: schemas.ProductCreateParser,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(verify_admin_user)):
    """
    Метод для парсера, делает то же самое, но создает категорию, если ее нет, и делает это по category_name, а не по id
    """
    prod.category_id = await get_category_id(db, prod.category_name)
    db_product = await controller.create_product(db, prod)
    logger.info(f"Продукт успешно создан: {db_product}")
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
async def update_product_details(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_admin_user)
):
    db_product = await controller.get_product_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return await controller.update_product(db=db, db_obj=db_product, obj_in=product_update)


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(verify_admin_user)):

    return await controller.delete_product(db, product_id)


@router.get("/", response_model=schemas.ProductList)
async def get_products(
    min_price: float = Query(None, description="Минимальная цена для фильтрации"),
    max_price: float = Query(None, description="Максимальная цена для фильтрации"),
    brands: List[str] = Query(None, description="Список брендов для фильтрации"),
    categories: List[int] = Query(None, description="Список категорий для фильтрации принимает их id"),
    page: int = Query(1, description="Номер страницы пагинации"),
    page_limit: int = Query(12, description="Лимит страницы"),
    sort_by: str = Query(None, description="Параметр сортировки (price, popularity, date)"),
    sort_order: str = Query("asc", description="Порядок сортировки (asc - по возрастанию, desc - по убыванию)"),
    is_hit: bool = Query(None, description="Возвращает хит продукты"),
    db: Session = Depends(get_db)
):
    total_pages, total_count, products = await controller.get_products(
        db=db,
        min_price=min_price,
        max_price=max_price,
        brands=brands,
        categories=categories,
        page=page,
        page_limit=page_limit,
        sort_by=sort_by,
        sort_order=sort_order,
        is_hit=is_hit,
    )
    products_preview = [schemas.ProductPreview.from_product(product) for product in products]
    return schemas.ProductList(
        total_pages=total_pages,
        total_count=total_count,
        products=products_preview)

@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = await controller.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="No products found")
    return product


@router.get("/search/", response_model=schemas.ProductSearchList)
async def search(query: str, db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    total_pages, total_count, products = await controller.search_products(db, query, limit, offset)
    if products:
        return schemas.ProductSearchList(
            total_pages=total_pages,
            total_count=total_count,
            products=products)
    else:
        raise HTTPException(status_code=404, detail="No products found")