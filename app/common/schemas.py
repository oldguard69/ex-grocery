from datetime import datetime

from pydantic import BaseModel, computed_field


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
class DepartmentDto(BaseModel):
    department_id: int
    description: str


class RoleDto(BaseModel):
    role_id: int
    description: str


class UserDto(BaseModel):
    user_id: int
    email: str
    role: RoleDto
    success_order_count: int
    departments: list[DepartmentDto]
    email_verified: bool


class LoginDto(BaseModel):
    email: str
    password: str


class RegisterDto(BaseModel):
    email: str
    password: str


class VerifyEmailDto(BaseModel):
    otp: str


# endregion User


# region order
class OrderItemCreateDto(BaseModel):
    product_id: int
    quantity: int


class OrderCreateDto(BaseModel):
    note: str
    discount_id: int | None = None
    items: list[OrderItemCreateDto]


class OrderItemDto(BaseModel):
    product: ProductDto
    quantity: int
    price: float


class DiscountDto(BaseModel):
    discount_id: int
    percentage: float


class OrderListDto(BaseModel):
    order_id: int
    note: str
    discount: DiscountDto | None
    total_items: int = 0
    total_price: float = 0

    class Config:
        orm_mode: True

    @computed_field
    @property
    def discount_price(self) -> float:
        if self.discount:
            return (self.discount.percentage / 100) * self.total_price
        return 0.0

    @computed_field
    @property
    def price(self) -> float:
        return self.total_price - self.discount_price


class OrderDetailsDto(OrderListDto):
    items: list[OrderItemDto]
