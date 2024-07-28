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
    product_1 = Product(name="Coffee", price="68.79", description="")
    product_2 = Product(name="Noddle", price="39", description="")
    product_3 = Product(name="Hammer", price="20", description="")
    session.add_all([product_1, product_2, product_3])
    session.add_all(
        [
            ProductProductCategory(product=product_1, category_id=1),
            ProductProductCategory(product=product_1, category_id=2),
            ProductProductCategory(product=product_2, category_id=4),
            ProductProductCategory(product=product_3, category_id=3),
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
    user_1 = User(
        email="staff1@gmail.com",
        hashed_password=hash_password("abc@123"),
        role_id=RoleEnum.STAFF,
    )
    user_2 = User(
        email="staff2@gmail.com",
        hashed_password=hash_password("abc@123"),
        role_id=RoleEnum.STAFF,
    )
    user_3 = User(
        email="customer@gmail.com",
        hashed_password=hash_password("abc@123"),
        role_id=RoleEnum.CUSTOMER,
    )
    session.add_all([user_1, user_2, user_3])
    session.add_all(
        [
            UserDepartment(user=user_1, department_id=1),
            UserDepartment(user=user_1, department_id=2),
            UserDepartment(user=user_2, department_id=1),
            UserDepartment(user=user_3, department_id=3),
        ]
    )
    session.commit()

"""
staff 1 => department={1, 2}
staff 2 => department={1}
customer => department={3}

product 1 => category={1, 2}
product 2 => category={4}
product 3 => category={3}

category 1 => department 1
category 2 => department 1
category 3 => department 2  (staff 1 can modify, but not staff 2)
category 4 => department 3
"""
