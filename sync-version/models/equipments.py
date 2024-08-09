from sqlmodel import SQLModel, Field


class Equipment(SQLModel, table=True, tablename="equipments"):
    id: int = Field(primary_key=True, default=None)
    ip_address: str

    class Config:
        schema_extra = {
            "example": {
                "ip_address": "192.168.0.1"
            }
        }
