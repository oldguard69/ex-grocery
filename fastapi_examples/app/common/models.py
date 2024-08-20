"""Define the ORM for models in the database"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    false,
    func,
    literal,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.database import Base


class Role(Base):
    __tablename__ = "roles"
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String)


class Department(Base):
    __tablename__ = "department"
    department_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String)

    users: Mapped["User"] = relationship(
        secondary="user_departments", back_populates="departments", viewonly=True
    )


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.role_id"))
    email_verified: Mapped[bool] = mapped_column(Boolean, server_default=false())
    success_order_count: Mapped[int] = mapped_column(
        Integer, server_default=literal("0")
    )
    customer_category_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("customer_categories.category_id"), nullable=True
    )
    otp_secret: Mapped[str | None] = mapped_column(String, nullable=True)
    otp_expired_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    otp_random_int: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    role: Mapped[Role] = relationship("Role")
    departments: Mapped[list[Department]] = relationship(
        secondary="user_departments", back_populates="users", viewonly=True
    )
    customer_category: Mapped["CustomerCategory"] = relationship()


class UserDepartment(Base):
    __tablename__ = "user_departments"
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), primary_key=True
    )
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("department.department_id"), primary_key=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    user: Mapped[User] = relationship("User")
    department: Mapped[Department] = relationship("Department")


class CustomerCategory(Base):
    __tablename__ = "customer_categories"
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    lower_bound: Mapped[int | None] = mapped_column(Integer, nullable=True)
    upper_bound: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())


class ProductCategory(Base):
    __tablename__ = "product_categories"
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    department_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("department.department_id")
    )

    department: Mapped[Department] = relationship("Department")
    products: Mapped[list["Product"]] = relationship(
        secondary="product_product_categories",
        back_populates="product_categories",
        viewonly=True,
    )


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    product_categories: Mapped[list["ProductCategory"]] = relationship(
        secondary="product_product_categories", back_populates="products", viewonly=True
    )


class ProductProductCategory(Base):
    __tablename__ = "product_product_categories"
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.product_id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_categories.category_id"), primary_key=True
    )

    product: Mapped[Product] = relationship("Product")
    product_category: Mapped[ProductCategory] = relationship("ProductCategory")


class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    note: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"))
    discount_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("discounts.discount_id"), nullable=True
    )

    customer: Mapped[User] = relationship("User")
    discount: Mapped["Discount"] = relationship("Discount")
    items: Mapped[list["OrderItem"]] = relationship(viewonly=True)


class OrderItem(Base):
    __tablename__ = "order_items"
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"))
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.order_id"))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)

    product: Mapped[Product] = relationship("Product")
    order: Mapped[Order] = relationship("Order")


class Discount(Base):
    __tablename__ = "discounts"
    discount_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    percentage: Mapped[float] = mapped_column(Float)
    product_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_categories.category_id")
    )
    customer_category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customer_categories.category_id")
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=true())

    product_category: Mapped[ProductCategory] = relationship("ProductCategory")
    customer_category: Mapped[CustomerCategory] = relationship("CustomerCategory")
