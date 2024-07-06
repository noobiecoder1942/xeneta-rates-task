from typing import Optional, Union, Tuple, Dict, List
import psycopg
from psycopg.rows import dict_row
from flask import current_app

def get_connection_string():
    """
    Generate the database connection string.

    Returns:
    -------
    str
        The PostgreSQL connection string.
    """
    user = current_app.config['DB_USER']
    password = current_app.config['DB_PASSWORD']
    host = current_app.config['DB_HOST']
    port = current_app.config['DB_PORT']
    name = current_app.config['DB_NAME']
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    return connection_string

def get_connection():
    """
    Establish a connection to the database.

    Returns:
    -------
    psycopg.Connection
        A new connection to the PostgreSQL database.
    """
    return psycopg.connect(get_connection_string())

def get_rows(query: str, params: Optional[Union[Tuple, Dict]] = None) -> List:
    """
    Execute a SQL query and fetch all rows.

    Parameters:
    ----------
    query : str
        The SQL query to be executed.
    params : tuple or dict, optional
        The parameters to be passed to the SQL query.

    Returns:
    -------
    list of dict
        A list of rows, where each row is represented as a dictionary.
    """
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return rows
