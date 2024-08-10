from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlmodel import select

from database.db import get_session
from models.equipments import Equipment


equipment_router = APIRouter(tags=['Equipment'])


@equipment_router.post('/add')
async def add_equipment(equipment: Equipment, session=Depends(get_session)) -> dict:
    statement = select(Equipment).where(Equipment.ip_address == equipment.ip_address)
    mac_exist = session.execute(statement).fetchall()

    if mac_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f" Equipment with IP address {equipment.ip_address} already exists."
        )

    session.add(equipment)
    session.commit()
    session.refresh(equipment)
    return {"message": "Equipment added successfully."}
    # hashed_password = hash_password.create_hash(user.password)
    # user.password = hashed_password
    # await user_database.save(user)


@equipment_router.get("/get_all", response_model=List[Equipment])
async def get_all_equipments(session=Depends(get_session)) -> List[Equipment]:
    return session.query(Equipment).all()


@equipment_router.get("/{id}", response_model=Equipment)
async def get_equipment_by_id(equipment_id: int, session=Depends(get_session)) -> Equipment:
    equipment = session.get(Equipment, equipment_id)
    if equipment:
        return equipment
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Equipment with supplied ID does not exist")


@equipment_router.delete("/delete/")
async def delete_all_equipments(session=Depends(get_session)) -> dict:
    session.query(Equipment).delete()
    session.commit()
    return {"message": "All equipments deleted successfully."}


@equipment_router.delete("/delete/{id}")
async def delete_equipment_by_id(equipment_id: int, session=Depends(get_session)) -> dict:
    equipment = session.get(Equipment, equipment_id)
    if equipment:
        session.delete(equipment)
        session.commit()
        return {
            "message": "Equipment with supplied ID deleted successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Equipment with supplied ID does not exist."
    )
