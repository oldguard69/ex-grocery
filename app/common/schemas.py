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
