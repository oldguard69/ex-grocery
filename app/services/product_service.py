from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Product
from ..schemas import ProductCategoryDto, ProductCategoryCreateDto


def list_products(session: Session):
    return session.scalars(select(Product))
