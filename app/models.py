from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class UserResponse(BaseModel):
    id: int
    name: str
