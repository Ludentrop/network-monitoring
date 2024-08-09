from pydantic import BaseModel


class User(BaseModel):
    username: str  # login
    password: str
    fullname: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin12345",
                "fullname": "Adminov Admin Adminovich"
            }
        }


class UserSignIn(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin12345",
            }
        }
