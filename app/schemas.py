from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name cannot be empty")
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: int
    date_joined: date

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str