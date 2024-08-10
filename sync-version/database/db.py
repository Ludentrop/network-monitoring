from sqlmodel import SQLModel, Session, create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# from .cfg import PATH


class Settings(BaseSettings):
    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


settings = Settings()


engine = create_engine(settings.DB_URL, echo=False)


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
