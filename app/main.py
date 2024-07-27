from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, new_session
from .services import product_category_service, product_service


models.Base.metadata.create_all(engine)


def create_new_session():
    session = new_session()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/product-categories/", response_model=list[schemas.ProductCategoryDto])
def list_product_categories(session: Session = Depends(create_new_session)):
    prod_categories = product_category_service.list_product_categories(session)
    return prod_categories


@app.post("/product-categories/")
def create_product_category(
    product_category: schemas.ProductCategoryCreateDto,
    session: Session = Depends(create_new_session),
):
    product_category_service.create_product_category(session, product_category)


@app.get("/products/", response_model=list[schemas.ProductDto])
def list_products(
    session: Session = Depends(create_new_session),
):
    return product_service.list_products(session)
    