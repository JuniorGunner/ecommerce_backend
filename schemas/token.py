from pydantic import BaseModel
from typing import Optional

# Pydantic schema for token data, used for type checking the payload within the JWT
class TokenData(BaseModel):
    username: Optional[str] = None
