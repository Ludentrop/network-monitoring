import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlmodel import select

from database.db import get_session
from models.terminals import Terminal, TerminalResponse


terminal_router = APIRouter(tags=['Terminal'])


@terminal_router.post('/add')
async def add_terminal(terminal: Terminal, session=Depends(get_session)) -> dict:
    statement = select(Terminal).where(Terminal.mac == terminal.mac)
    mac_exist = session.execute(statement).fetchall()

    if mac_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f" Terminal with MAC {terminal.mac} already exists."
        )

    session.add(terminal)
    session.commit()
    session.refresh(terminal)
    return {"message": "Terminal added successfully."}
    # hashed_password = hash_password.create_hash(user.password)
    # user.password = hashed_password
    # await user_database.save(user)


@terminal_router.get("/get_all", response_model=List[Terminal])
async def get_all_terminals(session=Depends(get_session)) -> List[Terminal]:
    return session.query(Terminal).all()


@terminal_router.get("/{id}", response_model=TerminalResponse)
async def get_terminal_by_id(terminal_id: int, session=Depends(get_session)) -> Terminal:
    terminal = session.get(Terminal, terminal_id)
    if terminal:
        return terminal
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=" Terminal with supplied ID does not exist")


@terminal_router.delete("/delete/")
async def delete_all_terminals(session=Depends(get_session)) -> dict:
    session.query(Terminal).delete()
    session.commit()
    return {"message": "All terminals deleted successfully."}


@terminal_router.delete("/delete/{id}")
async def delete_terminal_by_id(terminal_id: int, session=Depends(get_session)) -> dict:
    terminal = session.get(Terminal, terminal_id)
    if terminal:
        session.delete(terminal)
        session.commit()
        return {
            "message": "Terminal with supplied ID deleted successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Terminal with supplied ID does not exist."
    )
