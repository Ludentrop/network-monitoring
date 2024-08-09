from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlmodel import select

from database.db import get_session
from models.users import User, UserSignIn, UserUpdate


user_router = APIRouter(tags=['User'])


@user_router.post('/signup')
async def sign_up(user: User, session=Depends(get_session)) -> dict:
    # print(dir(session))
    statement = select(User).where(User.username == user.username)
    user_exist = session.execute(statement).fetchall()

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user.username} already exists."
        )

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User signed up successfully."}
    # hashed_password = hash_password.create_hash(user.password)
    # user.password = hashed_password
    # await user_database.save(user)


@user_router.post('/signin')
async def sign_in(user: UserSignIn, session=Depends(get_session)) -> dict:  # : OAuth2PasswordRequestForm = Depends()
    user_exist = await User.find_one(User.username == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user.username} does not exist."
        )
    if user_exist.password == user.password:
        return {
            "message": "User signed in successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )


@user_router.get("/get_all", response_model=List[User])
async def get_all_users(session=Depends(get_session)) -> List[User]:
    statement = select(User)
    users = session.exec(statement).all()
    return users


@user_router.get("/{id}", response_model=User)
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


@user_router.delete("/delete/{id}")
async def delete_user(user_id: int, session=Depends(get_session)) -> dict:
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
