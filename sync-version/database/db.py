from sqlmodel import SQLModel, Session, create_engine

from .cfg import PATH


engine = create_engine(PATH, echo=False)


def conn():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
