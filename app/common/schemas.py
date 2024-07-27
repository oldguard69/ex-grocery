from datetime import datetime
from pydantic import BaseModel


# region Product Category
class ProductCategoryCreateDto(BaseModel):
    name: str
    department_id: int


class ProductCategoryDto(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode: True
# endregion


# region Product
class ProductCreateUpdateDto(BaseModel):
    name: str
    description: str = ""
    price: float
    product_category_ids: list[int]


class ProductDto(BaseModel):
    product_id: int
    name: str
    description: str
    price: float
    created_at: datetime
    product_categories: list[ProductCategoryDto]

    class Config:
        orm_mode: True
# endregion


# region User
class RoleDto(BaseModel):
    role_id: int
    description: str


class UserDto(BaseModel):
    user_id: int
    email: str
    role: RoleDto
    success_order_count: int


class LoginDto(BaseModel):
    email: str
    password: str


class RegisterDto(BaseModel):
    email: str
    password: str
# endregion User