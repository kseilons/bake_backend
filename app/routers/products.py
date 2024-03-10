from typing import List

from app.schemas import products as schemas
from app.controllers import products as prod_control
from app.models.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

router = APIRouter(tags=['products'])


@router.post("/", response_model=schemas.ProductWithProperty, status_code=201)
async def create_product(prod: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
          Создает сущность продукта. В "section_id" передается id связанного с ним заказа, не существующие id не примет.
        Так что сначала нужно создать catalog, а потом уже добавлять продукты. old_id нужен для связи с Bitrix
    """
    prod = await prod_control.create_product(db, prod)
    return prod


@router.get("/", response_model=schemas.ProductsResponse)
async def get_products(filters: schemas.ProductFilter = Depends(), page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """
            Получает список продуктов. В "section_id" передается id связанного с ним заказа не из Bitrix.
            old_id - id связанные с Bitrix. Чтобы получить все свойства продукта, воспользуйтесь /products/{prod_id} запросом
      """
    total_count = await prod_control.get_product_count_by_order(db, filters)
    products = await prod_control.get_products(db, filters, page, limit)
    return {"total_count": total_count, "results": products}


@router.get("/by_ids", response_model=schemas.ProductsResponseByIds)
async def get_products_by_ids(
    product_ids: list[int] = Query(..., description="Список идентификаторов продуктов"),
    db: Session = Depends(get_db)
):
    """
    Получает список продуктов по указанным идентификаторам - id.
    """
    products = await prod_control.get_products_by_ids(db, product_ids)
    return {"total_count": len(products), "results": products}


@router.get("/{prod_id}", response_model=schemas.ProductWithProperty)
async def get_product(prod_id: int, db: Session = Depends(get_db)):
    return await prod_control.get_product(db, prod_id)


@router.put("/{prod_id}", response_model=schemas.ProductWithProperty)
async def update_product(
    prod_id: int, prod_data: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    """
              Обновляет значения указанные в теле запроса. Если вы не указывали поле, оно не обновится.
   """
    await prod_control.update_product(db, prod_id=prod_id, update_data=prod_data)
    return await prod_control.get_product(db, prod_id)

@router.delete("/{prod_id}" )
async def delete_product(
    prod_id: int,
    db: Session = Depends(get_db)
):
    """
              Удаляет продукт по id.
   """
    return await prod_control.delete_product(db, product_id=prod_id)

@router.post("/insert-bitrix", response_model=schemas.ProductWithProperty, status_code=201)
async def insert_product_from_bitrix(catalog: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
        Создает или обновляет сущность каталога. в id передается old_id из bitrix, section_id тоже из битрикса,
        возвращается новый section_id, указывающий на id родителя в базе дынных
    """
    result = await prod_control.insert_product(db, catalog)
    return result




