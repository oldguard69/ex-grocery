from fastapi import HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.common.models import (
    CustomerCategory,
    Department,
    Discount,
    ProductCategory,
    User,
)
from app.common.permissions import is_staff
from app.common.responses import FORBIDDEN_RESPONSE
from app.common.schemas import DiscountCreateUpdateDto


def _is_customer_category_valid(session: Session, customer_category_id: int) -> bool:
    """Return true if the customer_category_id exists in the database"""
    return session.scalar(
        select(exists().where(CustomerCategory.category_id == customer_category_id))
    )


def _is_product_category_valid(session: Session, product_category_id: int) -> bool:
    """Return true if the product_category_id exists in the database"""
    return session.scalar(
        select(exists().where(ProductCategory.category_id == product_category_id))
    )


def _has_access_on_product_category(
    session: Session, user: User, product_category_id: int
) -> bool:
    return session.scalar(
        select(
            exists()
            .select_from(ProductCategory)
            .where(
                ProductCategory.category_id == product_category_id,
                ProductCategory.department_id.in_(
                    select(Department.department_id)
                    .join(Department.users)
                    .where(User.user_id == user.user_id)
                    .subquery()
                ),
            )
        )
    )


def _discount_create_update_common_validation(
    session: Session, discount: DiscountCreateUpdateDto, user: User
) -> None:
    if not _is_customer_category_valid(session, discount.customer_category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid customer_category_id {discount.customer_category_id}",
        )
    if not _is_product_category_valid(session, discount.product_category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid product_category_id {discount.product_category_id}",
        )

    if not _has_access_on_product_category(session, user, discount.product_category_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Don't have permission on product_category_id {discount.product_category_id}",
        )

    if discount.percentage > 100 or discount.percentage <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Percentage must greater than 0 and less than 100",
        )


def list_discount(session: Session, user: User) -> list[Discount]:
    """Only return discount of product category that has department user linked to."""
    if not is_staff(user):
        raise FORBIDDEN_RESPONSE
    return session.scalars(
        select(Discount)
        .join(Discount.product_category)
        .where(
            ProductCategory.department_id.in_(
                select(Department.department_id)
                .join(Department.users)
                .where(User.user_id == user.user_id)
                .subquery()
            )
        )
    ).all()


def create_discount(
    session: Session, discount: DiscountCreateUpdateDto, user: User
) -> Discount:
    if not is_staff(user):
        raise FORBIDDEN_RESPONSE

    _discount_create_update_common_validation(session, discount, user)

    db_discount = Discount(
        percentage=discount.percentage,
        product_category_id=discount.product_category_id,
        customer_category_id=discount.customer_category_id,
    )
    session.add(db_discount)
    session.commit()
    session.refresh(db_discount)
    return db_discount


def update_discount(
    session: Session, discount_id: int, discount: DiscountCreateUpdateDto, user: User
) -> Discount:
    if not is_staff(user):
        raise FORBIDDEN_RESPONSE

    db_discount = session.scalar(
        select(Discount).where(Discount.discount_id == discount_id)
    )
    if not db_discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found"
        )

    if not _has_access_on_product_category(
        session, user, db_discount.product_category_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Don't have permission on product_category_id {db_discount.product_category_id}",
        )

    _discount_create_update_common_validation(session, discount, user)

    for field in [
        "percentage",
        "is_active",
        "product_category_id",
        "customer_category_id",
    ]:
        setattr(db_discount, field, getattr(discount, field))

    session.add(db_discount)
    session.commit()
    session.refresh(db_discount)
    return db_discount
