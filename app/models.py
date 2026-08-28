from typing import Literal

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=125)
    role: Literal["admin", "user"]


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=125)
    role: Literal["admin", "user"]


class UserResponse(BaseModel):
    id: int
    name: str
    age: int = Field(ge=0, le=125)
    role: Literal["admin", "user"]
