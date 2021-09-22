from src.utils.create_connection import *
from src.utils.db_table import *

def create_db_table(create_table_info):
    """
    Send the required info to create database table.
    params:
    param 'create_table_info' create table info
    type 'list'
    """
    for create_info in create_table_info:
        if create_info['create_flag'] is True:
            try:
                conn, cursor = connect(create_info['database'])
                create_table(conn, cursor, create_info['sql_create'])                
                close_connection(conn, cursor)
            except Exception as e:
                print("An error has occured.", e)
            else:
                print("{} table successfully created in {} database.".format(create_info['table'], create_info['database']))
        else:
            print("Table already created!")
