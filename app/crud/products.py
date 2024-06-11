import datetime
import json
from math import ceil
from typing import List, Type, Optional

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models import products as model
from app.categories.models import Category 

from app.schemas import products as schemas
from fastapi import HTTPException, status

from app.utils.update_list_field import update_list_field


async def create_product(db: Session,
                         product_data: schemas.ProductCreate):

    db_product = model.Product(
        title=product_data.title,
        category_id=product_data.category_id,
        short_description=product_data.short_description,
        preview_img=product_data.preview_img,
        sort=product_data.sort,
        price=product_data.price,
        old_price=product_data.old_price,
        is_hit=product_data.is_hit,
        brand=product_data.brand,
        create_date=datetime.datetime.now(),
        rating_count=0,
        rating_avg=0.0
    )
        # Сохранение в базе данных
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except IntegrityError as e:
        db.rollback()  # Откатываем изменения, если произошла ошибка
        raise HTTPException(status_code=400,
                            detail="Ошибка создания продукта: продукт с таким названием уже существует")

    
    db_product_info = model.ProductInfo(description=product_data.description, article=product_data.article, product_id=db_product.id)
    db.add(db_product_info)
    db.commit()
    db_product.info.description = product_data.description
    db_product.info.article = product_data.article

    # Добавление свойств продукта
    if product_data.properties:
        for prop in product_data.properties:
            db_product.properties.append(model.ProductProperty(name=prop.name, value=prop.value))

    # Добавление изображений продукта
    if product_data.images:
        for image in product_data.images:
            db_product.images.append(model.ProductImage(image_url=image.image_url, alt=image.alt))

    # Добавление файлов продукта
    if product_data.files:
        for file in product_data.files:
            db_product.files.append(model.ProductFile(file=file))

    db.commit()

    # Добавляем свойства продукта, изображения, файлы и т.д.
    # (Остальной код для добавления свойств продукта, изображений и файлов)

    return db_product




async def get_product_by_id(db: Session, product_id: int):
    return db.query(model.Product).filter_by(id=product_id).first()


async def update_product(db: Session, db_obj: model.Product, obj_in=schemas.ProductUpdate):
    if obj_in.title:
        db_obj.title = obj_in.title
    if obj_in.preview_img:
        db_obj.preview_img = obj_in.preview_img
    if obj_in.category_id:
        db_obj.category_id = obj_in.category_id
    if obj_in.short_description:
        db_obj.short_description = obj_in.short_description
    if obj_in.description:
        db_obj.description = obj_in.description
    if obj_in.sort:
        db_obj.sort = obj_in.sort

    # Обновление свойств продукта
    if obj_in.properties:
        await update_list_field(db_obj, obj_in, "properties")

    # Обновление изображений продукта
    if obj_in.images:
        await update_list_field(db_obj, obj_in, "images")

    # Обновление файлов продукта
    if obj_in.files:
        await update_list_field(db_obj, obj_in, "files")

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


async def delete_product(db: Session, product_id: int):
    try:
        product = await get_product_by_id(db, product_id)
        if not product:
            return {"error": "Product not found"}

        for info in product.info:
            db.delete(info)

        for property in product.properties:
            db.delete(property)
        for image in product.images:
            db.delete(image)
        for file in product.files:
            db.delete(file)
        for review in product.reviews:
            db.delete(review)
            
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"An error occurred while deleting product: {str(e)}"}

async def get_products(
            db: Session,
            min_price: float = None,
            max_price: float = None,
            brands: List[str] = None,
            categories: List[int] = None,
            page: int = 1,
            page_limit: int = 10,
            sort_by: str = None,
            sort_order: str = "asc",
            is_hit: bool = None,
            is_new: bool = None
    ) -> List[schemas.ProductPreview]:
    query = db.query(model.Product)

    # Фильтрация по минимальной цене
    if min_price is not None:
        query = query.filter(model.Product.price >= min_price)

    # Фильтрация по максимальной цене
    if max_price is not None:
        query = query.filter(model.Product.price <= max_price)

    # Фильтрация по бренду
    if brands:
        query = query.filter(model.Product.brand.in_(brands))

    #Фильтр по хиту
    if is_hit is not None:
        query = query.filter(model.Product.is_hit == is_hit)
    if is_new is not None:
        query = query.filter(model.Product.is_hit == is_hit)
        
    # Фильтрация по категории
    if categories:
        categories = await get_categories_with_children(db, categories)
        print(categories)
        query = query.filter(model.Product.category_id.in_(categories))

    # Сортировка
    if sort_by == "price":
        if sort_order == "asc":
            query = query.order_by(model.Product.price)
        elif sort_order == "desc":
            query = query.order_by(model.Product.price.desc())
    elif sort_by == "popularity":
        if sort_order == "asc":
            query = query.order_by(model.Product.popularity)
        elif sort_order == "desc":
            query = query.order_by(model.Product.popularity.desc())
    elif sort_by == "date":
        if sort_order == "asc":
            query = query.order_by(model.Product.create_date)
        elif sort_order == "desc":
            query = query.order_by(model.Product.create_date.desc())


        
    total_count = query.count()

    offset = (page - 1) * page_limit
    query = query.offset(offset).limit(page_limit)

    total_pages = ceil(total_count / page_limit)
    products = query.all()
    return total_pages, total_count, products
    
async def search_products(db: Session, query: str, limit: int = 10, offset: int = 0):
    search = f"%{query}%"
    query = db.query(model.Product).join(model.ProductInfo) \
        .filter(
            or_(
                model.Product.title.ilike(search),
                model.Product.short_description.ilike(search),
                model.ProductInfo.description.ilike(search),
                model.ProductInfo.article.ilike(search),
                model.Product.brand.ilike(search),
            )
        ).options(joinedload(model.Product.category))
    total_count = query.count()

    query = query.offset(offset).limit(limit)

    total_pages = ceil(total_count / limit)
    products = query.all()
    product_previews = [
        schemas.ProductSearch(
            id=product.id,
            preview_img=product.preview_img,
            title=product.title,
            category_name=product.category.name,
            short_description=product.short_description,
            rating_avg=product.rating_avg,
            rating_count=product.rating_count,
            brand=product.brand,
            old_price=product.old_price,
            price=product.price,
            is_hit=product.is_hit,
            article=product.info[0].article if product.info[0] else None,
            description=product.info[0].description if product.info[0] else None
        ) for product in products
    ]
    
    return total_pages, total_count, product_previews
    
async def get_categories_with_children(db: Session, categories: List[int]) -> List[Category]:
    result_categories = []

    def find_children(category_id):
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            result_categories.append(category.id)
            children = db.query(Category).filter(Category.parent_id == category.id).all()
            for child in children:
                find_children(child.id)

    for category_id in categories:
        find_children(category_id)

    return result_categories