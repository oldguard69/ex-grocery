from common.database import new_session, Base, engine
from common.models import ProductCategory, Department, Role, CustomerCategory
from common.constants import RoleEnum

Base.metadata.create_all(engine)


with new_session() as session:
    session.add_all(
        [
            Role(role_id=RoleEnum.STAFF, description="Internal Staff"),
            Role(role_id=RoleEnum.CUSTOMER, description="Customer"),
        ]
    )
    session.add_all([
        Department(department_id=1, description="First department"),
        Department(department_id=2, description="Second department"),
        Department(department_id=3, description="Third department"),
    ])
    session.add_all([
        ProductCategory(category_id=1, name="Fast Food", department_id=1),
        ProductCategory(category_id=2, name="Frozen Food", department_id=1),
        ProductCategory(category_id=3, name="Tools", department_id=2),
        ProductCategory(category_id=4, name="Cake and Candy", department_id=3),
    ])
    session.add_all([
        CustomerCategory(category_id=1, name="Bronze", lower_bound=0, upper_bound=20),
        CustomerCategory(category_id=2, name="Silver", lower_bound=21, upper_bound=40),
        CustomerCategory(category_id=3, name="Gold", lower_bound=41, upper_bound=None),
    ])
    session.commit()
