import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


pool = ConnectionPool(DATABASE_URL, min_size=2, max_size=10, open=False)
