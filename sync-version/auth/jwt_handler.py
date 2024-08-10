import time
from datetime import datetime
from fastapi import HTTPException, status
from pydantic_settings import BaseSettings, SettingsConfigDict
import jwt


class Settings(BaseSettings):
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()


def create_access_token(user: str) -> str:
    payload = {'user': user, 'expires': time.time() + 3600}
    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
    return token


def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        
        expire = data.get('expires')
        
        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No access token supplied')
        
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token expired')
        
        return data
    
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')
