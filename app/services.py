from psycopg.rows import dict_row

from .database import pool
from .exceptions import UserNotFound
from .models import User, UserCreate


async def get_all_users() -> list[User]:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("SELECT id, name, age, role FROM users;")
            recs = await cur.fetchall()

            return [User(**rec) for rec in recs]


async def get_user(user_id: int) -> User:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                "SELECT id, name, age, role FROM users WHERE id = %s;", (user_id,)
            )
            rec = await cur.fetchone()

            if rec is None:
                raise UserNotFound(f"User with id: {user_id} does not exist")

            return User(**rec)


async def create_user(user: UserCreate) -> User:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                INSERT INTO users (name, age, role)
                VALUES (%s, %s, %s)
                RETURNING id, name, age, role;
                """,
                (user.name, user.age, user.role),
            )

            rec = await cur.fetchone()
            await conn.commit()

            return User(**rec)


async def update_user(user_id: int, data: UserCreate) -> User:
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                UPDATE users
                SET name = %s, age = %s, role = %s
                WHERE id = %s
                RETURNING id, name, age, role;
                """,
                (data.name, data.age, data.role, user_id),
            )

            rec = await cur.fetchone()
            if rec is None:
                raise UserNotFound(f"User with id: {user_id} does not exist")

            await conn.commit()
            return User(**rec)


async def delete_user(user_id: int) -> None:
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM users
                WHERE id = %s
                RETURNING id;
                """,
                (user_id,),
            )

            rec = await cur.fetchone()
            if rec is None:
                raise UserNotFound(f"User with id: {user_id} does not exist")

            await conn.commit()
