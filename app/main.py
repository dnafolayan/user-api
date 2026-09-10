from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from .database import pool
from .exceptions import UserNotFound
from .models import UserCreate, UserResponse
from .services import create_user, delete_user, get_all_users, get_user, update_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()


app = FastAPI(lifespan=lifespan)


@app.get("/users", response_model=list[UserResponse])
async def get_users_endpoint():
    users: list[UserResponse] = await get_all_users()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id_endpoint(user_id: int):
    try:
        user: UserResponse = await get_user(user_id)
        return user
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate):
    user: UserResponse = await create_user(user)
    return user


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, data: UserCreate):
    try:
        user: UserResponse = await update_user(user_id, data)
        return user
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_endpoint(user_id: int):
    try:
        await delete_user(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
