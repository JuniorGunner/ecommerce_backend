# routes/cart_routes.py
from fastapi import APIRouter
from models.cart import CartItem

router = APIRouter()


@router.post("/cart/add")
def add_to_cart(item: CartItem):
    """ Add a product to the user's shopping cart. """
    # TODO: Implement add to cart logic
    return {"message": "Item added to cart"}


@router.get("/cart")
def view_cart():
    """ Display all items in the user's cart. """
    # TODO: Implement view cart logic
    return {"cart": []}


@router.delete("/cart/remove")
def remove_from_cart(item: CartItem):
    """ Remove an item from the shopping cart. """
    # TODO: Implement remove from cart logic
    return {"message": "Item removed from cart"}
