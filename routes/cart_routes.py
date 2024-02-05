from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.cart import CartItemCreateSchema, CartItemDisplaySchema
from schemas.user import UserResponseSchema
from services import cart_service
from services.user_service import get_current_user
from database import get_db

router = APIRouter()


@router.post("/cart/add", response_model=CartItemDisplaySchema)
def add_to_cart(
    item: CartItemCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """Add a product to the user's shopping cart."""
    return cart_service.add_item_to_cart(db=db, item=item, user_id=current_user.id)


@router.get("/cart", response_model=list[CartItemDisplaySchema])
def view_cart(
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """Display all items in the user's cart."""
    return cart_service.get_cart_items(db=db, user_id=current_user.id)


@router.delete("/cart/remove", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponseSchema = Depends(get_current_user),
):
    """Remove an item from the shopping cart."""
    success = cart_service.remove_item_from_cart(
        db=db, item_id=item_id, user_id=current_user.id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item removed from cart"}
