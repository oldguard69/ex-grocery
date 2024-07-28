from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.common.constants import RoleEnum
from app.common.models import Product, ProductCategory, User, UserDepartment


def is_staff(user: User) -> bool:
    return user.role_id == RoleEnum.STAFF


def is_customer(user: User) -> bool:
    return user.role_id == RoleEnum.CUSTOMER


def is_staff_can_modify_product(session: Session, user: User, product_id: int) -> bool:
    """
    Check if staff can modify the product

    We check that the department of the product category that the
    product is linked to, is also the department of the user.
    """
    return session.scalar(
        select(
            exists().where(
                UserDepartment.department_id.in_(
                    (
                        select(ProductCategory.department_id)
                        .join(ProductCategory.products)
                        .where(Product.product_id == product_id)
                    ).subquery()
                ),
                UserDepartment.user_id == user.user_id,
            )
        )
    )
