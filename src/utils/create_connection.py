import psycopg2 as pg2
from dotenv import load_dotenv
import os

load_dotenv() 

def connect(database):
    """
    Create database connection.
    params:
    param 'database' name of the database
    type 'string'
    """
    conn = pg2.connect(
        host = os.getenv('HOST'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        port = os.getenv('PORT'),
        database = database
    )
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn, cursor):
    """
    Close database connection.
    params:
    param 'conn' connection to the database
    type 'connection object'
    param 'cursor' cursor of the connection
    type 'cursor object'
    """
    cursor.close()
    conn.close()
