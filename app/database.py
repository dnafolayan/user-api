import psycopg

DATABASE_URL = "dbname=user_api user=aethr"


def get_connection():
    return psycopg.connect(DATABASE_URL)
