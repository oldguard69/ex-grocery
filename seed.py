from app.common.constants import RoleEnum
from app.common.database import Base, engine, new_session
from app.common.models import (
    CustomerCategory,
    Department,
    Discount,
    Product,
    ProductCategory,
    ProductProductCategory,
    Role,
    User,
    UserDepartment,
)
from app.common.password_hasher import hash_password

Base.metadata.create_all(engine)


with new_session() as session:
    session.add_all(
        [
            Role(role_id=RoleEnum.STAFF, description="Internal Staff"),
            Role(role_id=RoleEnum.CUSTOMER, description="Customer"),
        ]
    )
    session.add_all(
        [
            Department(department_id=1, description="First department"),
            Department(department_id=2, description="Second department"),
            Department(department_id=3, description="Third department"),
        ]
    )
    session.add_all(
        [
            ProductCategory(category_id=1, name="Fast Food", department_id=1),
            ProductCategory(category_id=2, name="Frozen Food", department_id=1),
            ProductCategory(category_id=3, name="Tools", department_id=2),
            ProductCategory(category_id=4, name="Cake and Candy", department_id=3),
        ]
    )
    session.add_all(
        [
            Product(product_id=1, name="Coffee", price="68.79", description=""),
            Product(product_id=2, name="Noddle", price="39", description=""),
            Product(product_id=3, name="Hammer", price="20", description=""),
        ]
    )
    session.add_all(
        [
            ProductProductCategory(product_id=1, category_id=1),
            ProductProductCategory(product_id=1, category_id=2),
            ProductProductCategory(product_id=2, category_id=4),
            ProductProductCategory(product_id=3, category_id=3),
        ]
    )
    session.add_all(
        [
            CustomerCategory(
                category_id=1, name="Bronze", lower_bound=0, upper_bound=20
            ),
            CustomerCategory(
                category_id=2, name="Silver", lower_bound=21, upper_bound=40
            ),
            CustomerCategory(
                category_id=3, name="Gold", lower_bound=41, upper_bound=None
            ),
        ]
    )
    session.add_all(
        [
            Discount(percentage=30, product_category_id=1, customer_category_id=1),
            Discount(percentage=40, product_category_id=1, customer_category_id=2),
            Discount(percentage=20, product_category_id=2, customer_category_id=3),
            Discount(percentage=10, product_category_id=3, customer_category_id=1),
        ]
    )
    session.add_all(
        [
            User(
                user_id=1,
                email="staff1@gmail.com",
                hashed_password=hash_password("abc@123"),
                role_id=RoleEnum.STAFF,
            ),
            User(
                user_id=2,
                email="staff2@gmail.com",
                hashed_password=hash_password("abc@123"),
                role_id=RoleEnum.STAFF,
            ),
        ]
    )
    session.add_all(
        [
            UserDepartment(user_id=1, department_id=1),
            UserDepartment(user_id=1, department_id=2),
            UserDepartment(user_id=2, department_id=1),
        ]
    )
    session.commit()

"""
user 1 => department={1, 2}
user 2 => department={1}

product 1 => category={1, 2}
product 2 => category={4}
product 3 => category={3}

category 1 => department 1
category 2 => department 1
category 3 => department 2
category 4 => department 3
"""
