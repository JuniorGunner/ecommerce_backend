from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):
    id: Optional[int] = None
    user_id: int
    product_id: int
    quantity: int
    status: str
