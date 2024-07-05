import psycopg
from psycopg.rows import dict_row
from flask import current_app

def get_connection_string():
    USER = current_app.config['DB_USER']
    PASSWORD = current_app.config['DB_PASSWORD']
    PORT = current_app.config['DB_PORT']
    NAME = current_app.config['DB_NAME']

    CONNECTION_STRING = f"postgresql://{USER}:{PASSWORD}@localhost:{PORT}/{NAME}"
    return CONNECTION_STRING

def get_connection():
    return psycopg.connect(get_connection_string())

def get_rows(query, params=None):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return rows
    