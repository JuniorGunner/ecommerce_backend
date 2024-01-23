from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
