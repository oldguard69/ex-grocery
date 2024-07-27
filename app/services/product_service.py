from sqlalchemy import select, delete
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status

from app.common.models import Product, ProductCategory, ProductProductCategory
from app.common.schemas import ProductCreateUpdateDto


def list_products(session: Session):
    return session.scalars(
        select(Product).options(selectinload(Product.product_categories))
    )


def get_product(session: Session, product_id: int):
    product = session.scalar(select(Product).where(Product.product_id == product_id))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


def _check_invalid_product_category_ids(
    session: Session, product: ProductCreateUpdateDto
):
    db_product_category_ids = session.scalars(
        select(ProductCategory.category_id).where(
            ProductCategory.category_id.in_(product.product_category_ids)
        )
    )
    invalid_product_category_ids = set(product.product_category_ids).difference(
        set(db_product_category_ids)
    )
    if invalid_product_category_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid product category ids {invalid_product_category_ids}",
        )


def create_product(session: Session, product: ProductCreateUpdateDto):
    _check_invalid_product_category_ids(session, product)
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
    )
    session.add(db_product)
    for product_category_ids in product.product_category_ids:
        session.add(
            ProductProductCategory(product=db_product, category_id=product_category_ids)
        )
    session.commit()
    session.refresh(db_product)
    return db_product


def update_product(session: Session, product_id: int, product: ProductCreateUpdateDto):
    db_product = session.scalar(select(Product).where(Product.product_id == product_id))
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    _check_invalid_product_category_ids(session, product)
    db_product.name = product.name
    db_product.price = product.price
    db_product.description = product.description
    session.add(db_product)
    session.execute(
        delete(ProductProductCategory).where(
            ProductProductCategory.product_id == product_id
        )
    )
    for product_category_ids in product.product_category_ids:
        session.add(
            ProductProductCategory(product=db_product, category_id=product_category_ids)
        )
    session.commit()
    session.refresh(db_product)
    return db_product

