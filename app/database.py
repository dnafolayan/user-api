import os

from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


pool = AsyncConnectionPool(DATABASE_URL, min_size=2, max_size=10, open=False)
