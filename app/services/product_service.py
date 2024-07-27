from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.models import Product


def list_products(session: Session):
    return session.scalars(select(Product))
