from fastapi import APIRouter, Depends, HTTPException, Security
from schemas.user import UserSchema, UserResponseSchema
from schemas.token import Token
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    oauth2_scheme,
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register")
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    new_user = create_user(db=db, user=user)

    if new_user:
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Error registering user")


@router.post("/login", response_model=Token)
def login_user(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticate a user and return an access token
    """
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/profile")
def get_user_profile(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    # current_user: UserSchema = Security(get_current_user, scopes=[])
):
    """
    Retrieve the profile information of the logged-in user.
    """
    user = get_current_user(db=db, token=token)
    return user
