from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.common import models, schemas
from app.common.database import create_new_session, engine
from app.services import (
    order_service,
    product_category_service,
    product_service,
    user_service,
)

models.Base.metadata.create_all(engine)


app = FastAPI()


@app.post("/register")
def register(
    register_dto: schemas.RegisterDto, session: Session = Depends(create_new_session)
) -> dict:
    return user_service.handle_register(session, register_dto)


@app.post("/login")
def login(
    register_dto: schemas.LoginDto, session: Session = Depends(create_new_session)
) -> dict:
    return user_service.handle_login(session, register_dto)


@app.get("/email-verification")
def send_email_verification_email(
    user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> dict:
    return user_service.send_verification_email(session, user)


@app.post("/email-verification")
def verify_email(
    body: schemas.VerifyEmailDto,
    user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> dict:
    return user_service.verify_email(session, user, body)


@app.get("/user/", response_model=schemas.UserDto)
def get_user(
    user: Annotated[models.User, Depends(user_service.get_current_user)],
) -> models.User:
    return user


@app.get("/product-categories/", response_model=list[schemas.ProductCategoryDto])
def list_product_categories(
    session: Session = Depends(create_new_session),
) -> list[models.ProductCategory]:
    return product_category_service.list_product_categories(session)


@app.post("/product-categories/")
def create_product_category(
    product_category: schemas.ProductCategoryCreateDto,
    user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> None:
    product_category_service.create_product_category(session, product_category, user)


@app.get("/products/", response_model=list[schemas.ProductDto])
def list_products(
    session: Session = Depends(create_new_session),
) -> list[models.Product]:
    return product_service.list_products(session)


@app.get("/products/{product_id}", response_model=schemas.ProductDto)
def get_product(
    product_id: int,
    session: Session = Depends(create_new_session),
) -> models.Product:
    return product_service.get_product(session, product_id)


@app.post("/products/", response_model=schemas.ProductDto)
def create_product(
    product: schemas.ProductCreateUpdateDto,
    user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> models.Product:
    return product_service.create_product(session, product, user)


@app.put("/products/{product_id}", response_model=schemas.ProductDto)
def update_product(
    product_id: int,
    product: schemas.ProductCreateUpdateDto,
    user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> models.Product:
    return product_service.update_product(session, product_id, product, user)


@app.post("/orders/", response_model=schemas.OrderDetailsDto)
def create_order(
    order: schemas.OrderCreateDto,
    current_user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> models.Order:
    return order_service.create_order(session, current_user, order)


@app.get("/orders/", response_model=list[schemas.OrderListDto])
def list_orders(
    current_user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> list[models.Order]:
    return order_service.list_order(session, current_user)


@app.get("/orders/{order_id}", response_model=schemas.OrderDetailsDto)
def get_order(
    order_id: int,
    current_user: Annotated[models.User, Depends(user_service.get_current_user)],
    session: Session = Depends(create_new_session),
) -> models.Order:
    return order_service.get_order(session, current_user, order_id)
