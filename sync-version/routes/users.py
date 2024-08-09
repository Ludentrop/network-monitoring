from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn


user_router = APIRouter(tags=['User'])


@user_router.post('/signup/', response_model=User)
async def sign_up(user: User):
    user_exist = await User.find_one(User.username == user.username)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )
    # hashed_password = hash_password.create_hash(user.password)
    # user.password = hashed_password
    # await user_database.save(user)
    return {
        "message": "User created successfully"
    }


@user_router.post('/signin/', response_model=UserSignIn)
async def sign_in(user: UserSignIn):
    user_exist = await User.find_one(User.username == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    if user_exist.password == user.password:
        return {
            "message": "User signed in successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )

