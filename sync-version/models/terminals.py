from pydantic import BaseModel, Field
from typing import Optional


class Terminal(BaseModel, table=True):
    id: int = Field(primary_key=True, default=None)
    mac: str
    model: str

    class Config:
        schema_extra = {
            "example": {
                "mac": "00:11:22:33:44:55",
                "model": "A"
            }
        }


class UpdateTerminal(BaseModel):
    mac: Optional[str]
    model: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "mac": "00:11:22:33:44:55",
                "model": "A"
            }
        }
