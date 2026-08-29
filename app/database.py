from psycopg_pool import ConnectionPool

DATABASE_URL = "dbname=user_api user=aethr"


pool = ConnectionPool(DATABASE_URL)
