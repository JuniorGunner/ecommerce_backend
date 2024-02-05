from pydantic import BaseModel


class CartItemSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class CartItemCreateSchema(CartItemSchema):
    pass


class CartItemDisplaySchema(CartItemSchema):
    id: int
    user_id: int
