from .exceptions import UserNotFound
from .models import User, UserCreate

users: list[User] = [
    User(id=1, name="Divine"),
    User(id=2, name="Alex"),
    User(id=3, name="Sarah"),
]


def get_user(user_id: int, users: list[User]) -> User:
    for user in users:
        if user.id == user_id:
            return user

    raise UserNotFound(f"User with id: {user_id} does not exist")


def create_user(name: str) -> User:
    new_id: int = users[-1].id + 1
    new_user: User = User(id=new_id, name=name)
    users.append(new_user)

    return new_user


def update_user(user_id: int, data: UserCreate, users: list[User]) -> User:
    for user in users:
        if user.id == user_id:
            user.name = data.name
            return user

    raise UserNotFound(f"User with id: {user_id} does not exist")


def delete_user(user_id: int, users: list[User]) -> None:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return

    raise UserNotFound(f"User with id: {user_id} does not exist")
