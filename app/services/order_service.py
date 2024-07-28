from fastapi import HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.common.models import Discount, Order, OrderItem, Product, User
from app.common.permissions import is_customer
from app.common.responses import FORBIDDEN_RESPONSE
from app.common.schemas import OrderCreateDto


def create_order(session: Session, current_user: User, order: OrderCreateDto) -> Order:
    """
    Create order

    Todo:

    - Based on the input discount, check if the discount is valid for the user
    and the product.
    - Change the user category when order success.

    """
    if not is_customer(current_user):
        raise FORBIDDEN_RESPONSE

    if not order.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Order don't have any items"
        )

    product_ids = [i.product_id for i in order.items]
    db_products = session.scalars(
        select(Product).where(Product.product_id.in_(product_ids))
    ).all()
    db_product_ids = [d.product_id for d in db_products]
    if missing_product_ids := set(product_ids).difference(set(db_product_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid product ids: {missing_product_ids}",
        )

    if order.discount_id:
        db_discount = session.scalar(
            select(Discount).where(Discount.discount_id == order.discount_id)
        )
        if not db_discount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid discount id: {order.discount_id}",
            )

    product_id_to_db_product_dict = {d.product_id: d for d in db_products}
    db_order = Order(
        note=order.note, discount_id=order.discount_id, customer=current_user
    )
    session.add(db_order)
    for item in order.items:
        session.add(
            OrderItem(
                order=db_order,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product_id_to_db_product_dict[item.product_id].price,
            )
        )
    current_user.success_order_count += 1
    session.add(current_user)
    session.commit()
    session.refresh(db_order)
    return db_order


def _get_order_query(current_user: User) -> Select:
    return (
        select(
            func.sum(OrderItem.price * OrderItem.quantity),
            func.count(OrderItem.item_id),
            Order,
        )
        .select_from(Order)
        .join(Order.items)
        .where(Order.customer_id == current_user.user_id)
        .group_by(Order)
    )


def list_order(session: Session, current_user: User) -> list[Order]:
    query_result = session.execute(_get_order_query(current_user)).all()
    result = []
    for total_price, total_quantity, order in query_result:
        order.total_price = total_price
        order.total_items = total_quantity
        result.append(order)
    return result


def get_order(session: Session, current_user: User, order_id: int) -> Order:
    order_query = _get_order_query(current_user).where(Order.order_id == order_id)
    if query_result := session.execute(order_query).first():
        total_price, total_items, db_order = query_result
        db_order.total_price = total_price
        db_order.total_items = total_items
        return db_order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
