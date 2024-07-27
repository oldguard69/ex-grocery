from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .common import models
from .common import schemas
from .common.database import engine, create_new_session
from .services import product_category_service, product_service, user_service


models.Base.metadata.create_all(engine)




app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register")
def register(
    register_dto: schemas.RegisterDto, session: Session = Depends(create_new_session)
):
    return user_service.handle_register(session, register_dto)


@app.post("/login")
def login(
    register_dto: schemas.LoginDto, session: Session = Depends(create_new_session)
):
    return user_service.handle_login(session, register_dto)


@app.get("/user/", response_model=schemas.UserDto)
def get_user(
    user: Annotated[models.User, Depends(user_service.get_current_user)],
):
    return user


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
