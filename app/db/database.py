import psycopg
from psycopg.rows import dict_row

user = "postgres"
password = "ratestask"
port = "5432"
dbname = "postgres"

CONNECTION_STRING = f"postgresql://{user}:{password}@localhost:{port}/{dbname}"

def get_connection():
    return psycopg.connect(CONNECTION_STRING)

def get_rows(query, params=None):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return rows
    