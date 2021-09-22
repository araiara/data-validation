def create_table(conn, cursor, sql_create):
    """
    Create database table.
    params:
    param 'conn' database connection object
    type 'connection object'
    param 'cursor' database cursor object
    type 'cursor object'
    param 'sql_create' sql statement to create table
    """
    with open(sql_create) as create_file:
        create_query = "".join(create_file.readlines())
        cursor.execute(create_query)
        conn.commit()

def delete_table_records(conn, cursor, table_name):
    """
    Delete database table records.
    params:
    param 'conn' database connection object
    type 'connection object'
    param 'cursor' database cursor object
    type 'cursor object'
    param 'table_name' name of the table to delete
    type 'string'
    """
    delete_query = 'TRUNCATE TABLE {}'.format(table_name)
    cursor.execute(delete_query)
    conn.commit()   
