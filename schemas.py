from pydantic import EmailStr, BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr # EmailStr for email validation provided by Pydantic
    city: str
    interests: List[str]

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

