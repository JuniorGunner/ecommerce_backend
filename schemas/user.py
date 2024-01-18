from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
