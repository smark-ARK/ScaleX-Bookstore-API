from fastapi.exceptions import HTTPException
from fastapi import status
from fastapi.params import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List

from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings


users = [
    {"id": 1, "username": "sampleuser", "password": "samplepass", "type": "user"},
    {"id": 2, "username": "sampleadmin", "password": "samplepass", "type": "admin"},
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_Key = settings.secret_key
REFRESH_SECRET_KEY = settings.refresh_secret_key
ALGORITHM = settings.algorithm
ACCESS_EXPIRE_MINUTES = settings.access_expire_minutes
REFRESH_EXPIRE_MINUTES = settings.refresh_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_Key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(Token: str, credentials_exception):
    try:
        payload = jwt.decode(Token, SECRET_Key, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def verify_refresh_token(refresh_token: str) -> bool:
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        # Perform additional checks if needed
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.JWTError, KeyError):
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized credentials",
        headers={"WWW-AUTHENTICATE": "BEARER"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = next((x for x in users if x["id"] == token_data.user_id), None)
    print("AUTHENTICATED")
    return schemas.User.parse_obj(user)
