from pydantic import BaseModel, Field
from typing import Optional


# Pydantic schema for token data, used for type checking the payload within the JWT
class TokenData(BaseModel):
    username: Optional[str] = Field(
        None, description="The username extracted from the token"
    )


class Token(BaseModel):
    access_token: str
    token_type: str
