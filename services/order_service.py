from sqlalchemy.orm import Session
from models.order import OrderModel
from schemas.order import OrderSchema


def create_order(db: Session, order: OrderSchema) -> OrderModel:
    """
    Service to create a new order in the database.
    """
    new_order = OrderModel(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        status=order.status,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_order(db: Session, order_id: int) -> OrderModel:
    """
    Service to get order details from the database.
    """
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()


def list_user_orders(db: Session, user_id: int) -> list[OrderModel]:
    """
    Service to list all orders for a user.
    """
    return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()


def update_order_status(db: Session, order_id: int, status: str) -> OrderModel:
    """
    Service to update the status of an order.
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

    if order:
        order.status = status
        db.commit()
        db.refresh(order)
        return order
    return None
