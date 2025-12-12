from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.parish import Parish


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    phone: str
    parish: Parish
    admin: bool


# Properties to receive via API on update
class UserUpdate(BaseModel):
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Properties shared by models stored in DB
class UserInDBBase(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
