import psycopg

with psycopg.connect("dbname=user_api user=aethr") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s;", (2,))
        rec = cur.fetchone()

        print(rec)
