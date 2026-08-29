from fastapi import FastAPI, HTTPException, status

from .exceptions import UserNotFound
from .models import UserCreate, UserResponse
from .services import create_user, delete_user, get_all_users, get_user, update_user

app = FastAPI()


@app.get("/users", response_model=list[UserResponse])
def get_users_endpoint():
    return get_all_users()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(user_id: int):
    try:
        return get_user(user_id)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate):
    return create_user(user)


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, data: UserCreate):
    try:
        return update_user(user_id, data)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


# @app.delete(
#     "/users/{user_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# def delete_user_endpoint(user_id: int):
#     try:
#         delete_user(user_id, users)
#     except UserNotFound:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
