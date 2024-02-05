from sqlalchemy.orm import Session
from models.cart import CartItemModel
from schemas.cart import CartItemCreateSchema


def add_item_to_cart(db: Session, item: CartItemCreateSchema, user_id: int):
    item_data = item.model_dump()
    item_data["user_id"] = user_id
    db_item = CartItemModel(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_cart_items(db: Session, user_id: int):
    return db.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()


def remove_item_from_cart(db: Session, item_id: int, user_id: int):
    db_item = (
        db.query(CartItemModel)
        .filter(CartItemModel.id == item_id, CartItemModel.user_id == user_id)
        .first()
    )
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
