from sqlmodel import SQLModel, Field
from typing import Optional


class Equipment(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    ip_address: str = Field(nullable=False)

    class Config:
        schema_extra = {
            "example": {
                "ip_address": "192.168.0.1"
            }
        }


class UpdateEquipment(SQLModel):
    ip_address: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "ip_address": "192.168.0.1"
            }
        }
