from os import truncate
from src.utils.create_connection import *
from src.utils.db_table import *

def validate_data(validate_data_info):
    """
    Run the test cases.
    params:
    param 'validate_table_info' create table info
    type 'list'
    """
    flag = True
    for validate_info in validate_data_info:
        try:            
            conn, cursor = connect(validate_info['database'])

            if flag:
                delete_table_records(conn, cursor, validate_info['table'])
                flag = False
            print("Successfully deleted the existing table records from {}.".format(validate_info['table']))

            for index, sql_validate_query in enumerate(validate_info['sql_validate']): 
                test_case = validate_info['test_table'] + '_' + str(index + 1)
                test_info = [test_case, validate_info['test_case'][index], validate_info['test_table']] 

                with open(sql_validate_query) as validate_file:
                    validate_query = "".join(validate_file.readlines())
                    cursor.execute(validate_query, test_info)
                    print("Successfully executed the test case {} of test database {}.".format(test_case, validate_info['test_table']))
                    conn.commit()
            close_connection(conn, cursor)
            
        except Exception as e:
            print("An error has occurred: ", e) 
              