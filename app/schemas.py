from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, List
from datetime import datetime


class ResponseToken(BaseModel):
    access_token: str
    token_type: str


class UserType(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    username: str
    password: str
    type: UserType


class User(UserBase):
    id: int


class TokenData(BaseModel):
    user_id: int


class Book(BaseModel):
    name: str = Field(..., title="Book Name", min_length=1)
    author: str = Field(..., title="Author", min_length=1)
    publication_year: int = Field(..., title="Publication Year")

    @validator("publication_year")
    def validate_publication_year(cls, year):
        current_year = datetime.now().year
        if year < 1000 or year > current_year:
            raise ValueError("Invalid publication year")
        return year
