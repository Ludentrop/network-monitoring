from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlmodel import select
import uuid

from database.db import get_session
from models.users import User, UserSignIn, UserUpdate, UserResponse, TokenResponse
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token

user_router = APIRouter(tags=['User'])

hash_password = HashPassword()


@user_router.post('/signup')
async def sign_up(user: User, session=Depends(get_session)) -> dict:
    statement = select(User).where(User.username == user.username)
    user_exist = session.execute(statement).fetchall()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user.username} already exists."
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User signed up successfully."}
    # hashed_password = hash_password.create_hash(user.password)
    # user.password = hashed_password
    # await user_database.save(user)


@user_router.post('/signin')
async def sign_in(user: OAuth2PasswordRequestForm = Depends(),
                  session=Depends(get_session)) -> dict:  # : OAuth2PasswordRequestForm = Depends()
    statement = select(User).where(User.username == user.username)
    user_exist = session.execute(statement).scalar_one_or_none()
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user.username} does not exist."
        )
    elif hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.username)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid details passed."
        )


@user_router.get("/get_all", response_model=List[User])
async def get_all_users(session=Depends(get_session)) -> List[User]:
    return session.query(User).all()


@user_router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with supplied ID does not exist")


@user_router.put("/edit/{id}", response_model=User)
async def update_user(user_id: int, new_data: UserUpdate, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if user:
        user_data = new_data.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User with supplied ID does not exist."
                        )


@user_router.delete("/delete/")
async def delete_all_users(session=Depends(get_session)) -> dict:
    session.query(User).delete()
    session.commit()
    return {"message": "All users deleted successfully."}


@user_router.delete("/delete/{id}")
async def delete_user_by_id(user_id: int, session=Depends(get_session)) -> dict:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return {
            "message": "User with supplied ID deleted successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with supplied ID does not exist."
    )
