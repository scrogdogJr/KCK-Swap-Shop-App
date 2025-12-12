from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str