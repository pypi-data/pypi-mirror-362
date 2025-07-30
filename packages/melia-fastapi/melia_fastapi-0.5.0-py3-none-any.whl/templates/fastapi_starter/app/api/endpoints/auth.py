from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import authenticate_user, create_acess_token
from app.models.user import User
from app.schemas.user import UserLoginSchema

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login(
        user_data: UserLoginSchema,
        response: Response,
        db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    token = create_acess_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True
    )
    return {"message": "Login successful"}
