from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.models import ProductCategory
from app.common.schemas import ProductCategoryCreateDto, ProductCategoryDto


def create_product_category(
    session: Session, product_category: ProductCategoryCreateDto
) -> None:
    session.add(
        ProductCategory(
            name=product_category.name, department_id=product_category.department_id
        )
    )
    session.commit()


def list_product_categories(session: Session) -> list[ProductCategoryDto]:
    return session.scalars(select(ProductCategory))
