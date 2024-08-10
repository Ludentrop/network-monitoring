from sqlmodel import SQLModel, Field


class Terminal(SQLModel, table=True, tablename="terminals"):
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


class TerminalResponse(SQLModel):
    mac: str
    model: str
