from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True, tablename="users"):
    id: int = Field(default=None, primary_key=True)
    username: str  # login
    password: str
    fullname: str

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin12345",
                "fullname": "Adminov Admin Adminovich"
            }
        }


class UserSignIn(SQLModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin12345",
            }
        }


class UserUpdate(SQLModel):
    username: Optional[str]
    password: Optional[str]
    fullname: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin12345",
            }
        }


class UserResponse(SQLModel):
    username: str
    fullname: str

