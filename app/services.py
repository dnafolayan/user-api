from psycopg.rows import dict_row

from .database import pool
from .exceptions import UserNotFound
from .models import User, UserCreate


def get_all_users() -> list[User]:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id, name, age, role FROM users;")
            recs = cur.fetchall()

            return [User(**rec) for rec in recs]


def get_user(user_id: int) -> User:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id, name, age, role FROM users WHERE id = %s;", (user_id,)
            )
            rec = cur.fetchone()

            if rec == None:
                raise UserNotFound(f"User with id: {user_id} does not exist")

            return User(**rec)


def create_user(user: UserCreate) -> User:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO users (name, age, role)
                VALUES (%s, %s, %s)
                RETURNING id, name, age, role;
                """,
                (user.name, user.age, user.role),
            )

            rec = cur.fetchone()
            conn.commit()

            return User(**rec)


def update_user(user_id: int, data: UserCreate) -> User:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE users
                SET name = %s, age = %s, role = %s
                WHERE id = %s
                RETURNING id, name, age, role;
                """,
                (data.name, data.age, data.role, user_id),
            )

            rec = cur.fetchone()
            if rec is None:
                raise UserNotFound(f"User with id: {user_id} does not exist")

            conn.commit()
            return User(**rec)


def delete_user(user_id: int) -> None:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM users
                WHERE id = %s
                RETURNING id;
                """,
                (user_id,),
            )

            rec = cur.fetchone()
            if rec is None:
                raise UserNotFound(f"User with id: {user_id} does not exist")

            conn.commit()
