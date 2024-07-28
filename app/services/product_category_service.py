from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.models import ProductCategory, User
from app.common.permissions import is_staff
from app.common.responses import FORBIDDEN_RESPONSE
from app.common.schemas import ProductCategoryCreateDto, ProductCategoryDto


def create_product_category(
    session: Session, product_category: ProductCategoryCreateDto, user: User
) -> None:
    if not is_staff(user):
        raise FORBIDDEN_RESPONSE

    session.add(
        ProductCategory(
            name=product_category.name, department_id=product_category.department_id
        )
    )
    session.commit()


def list_product_categories(session: Session) -> list[ProductCategoryDto]:
    return session.scalars(select(ProductCategory))
