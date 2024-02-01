from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.order import OrderSchema
from schemas.user import UserResponseSchema
from services import order_service
from services.user_service import oauth2_scheme, get_current_user

router = APIRouter()


@router.post("/orders/create", response_model=OrderSchema)
def create_order(
    order: OrderSchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """
    Endpoint to place a new order for a product.
    """
    order.user_id = current_user.id
    created_order = order_service.create_order(db=db, order=order)
    return created_order


@router.get("/orders/{order_id}", response_model=OrderSchema)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """
    Endpoint to retrieve details of a specific order.
    """
    order = order_service.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    current_user = get_current_user(db=db, token=token)
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    return order


@router.get("/orders/user/{user_id}", response_model=list[OrderSchema])
def list_user_orders(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """
    Endpoint to list all orders for a user.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view these orders"
        )
    orders = order_service.list_user_orders(db=db, user_id=user_id)
    return orders


@router.get("/orders/update/{order_id}", response_model=OrderSchema)
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """
    Endpoint to update the status of an order.
    """
    order = order_service.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this order"
        )
    updated_order = order_service.update_order_status(
        db=db, order_id=order_id, status=status
    )
    return updated_order
