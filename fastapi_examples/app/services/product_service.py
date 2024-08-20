from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.common.models import Product, ProductCategory, ProductProductCategory, User
from app.common.permissions import is_staff, is_staff_can_modify_product
from app.common.responses import FORBIDDEN_RESPONSE
from app.common.schemas import ProductCreateUpdateDto


def list_products(session: Session) -> list[Product]:
    return session.scalars(
        select(Product).options(selectinload(Product.product_categories))
    )


def get_product(session: Session, product_id: int) -> Product:
    product = session.scalar(select(Product).where(Product.product_id == product_id))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


def _check_invalid_product_category_ids(
    session: Session, product: ProductCreateUpdateDto, user: User
) -> None:
    # Check if there are category ids that are not exist in the database
    db_product_categories = session.scalars(
        select(ProductCategory).where(
            ProductCategory.category_id.in_(product.product_category_ids)
        )
    ).all()
    db_product_category_ids = [d.category_id for d in db_product_categories]
    invalid_product_category_ids = set(product.product_category_ids).difference(
        set(db_product_category_ids)
    )
    if invalid_product_category_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid product category ids {invalid_product_category_ids}",
        )

    # Check if the user is using category from department they are not linked to.
    user_department_ids = {d.department_id for d in user.departments}
    cannot_access_product_category_ids = [
        category.category_id
        for category in db_product_categories
        if category.department_id not in user_department_ids
    ]
    if cannot_access_product_category_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot access category ids {cannot_access_product_category_ids}",
        )


def create_product(
    session: Session, product: ProductCreateUpdateDto, user: User
) -> Product:
    if not is_staff(user):
        raise FORBIDDEN_RESPONSE

    _check_invalid_product_category_ids(session, product, user)
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


def update_product(
    session: Session, product_id: int, product: ProductCreateUpdateDto, user: User
) -> Product:
    if not (is_staff(user) and is_staff_can_modify_product(session, user, product_id)):
        raise FORBIDDEN_RESPONSE

    db_product = session.scalar(select(Product).where(Product.product_id == product_id))
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    _check_invalid_product_category_ids(session, product, user)
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
