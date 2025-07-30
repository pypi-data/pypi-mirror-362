from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    nom: str
    email: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    is_owner: bool
    is_passenger: bool

class UserRegisterSchema(BaseModel):
    nom: str
    email: str
    phone: Optional[str] = None
    is_owner: bool
    is_passenger: bool

class UserLoginSchema(BaseModel):
    email: str
    password: str
