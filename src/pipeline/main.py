# from src.utils.create_connection import *
# from src.utils.db_table import *
from create_db_table import create_db_table
from validate_data import validate_data

def create_table_info():
    """"
    Returns create table information.
    """
    return [
        {
            'database': 'data_validation',
            'table': 'qa_result',
            'sql_create': '../../schema/create_qa_result.sql',
            'create_flag': False
        }
    ]

def validate_data_info():
    return [
        {
            'database': 'data_validation',
            'table': 'qa_result',
            'test_table': 'employee',
            'test_case': [
                'Check if the manager employee has been assigned other role then manager.',
                'Check if any manager has been assigned to a manager employee itself.',
                'Check if manager role is assigned to a non-manager employee.',
                'Check if any manager has other work status than full time.'
            ],
            'sql_validate': [
                '../sql/validate_employee_case_i.sql',
                '../sql/validate_employee_case_ii.sql',
                '../sql/validate_employee_case_iii.sql',
                '../sql/validate_employee_case_iv.sql'
            ]
        },
        {
            'database': 'data_validation',
            'table': 'qa_result',
            'test_table': 'timesheet',
            'test_case': [
                'Check if a terminated employee has timesheet record after being terminated.',
                'Check if there are multiple timesheet record of an employee in a day.',
                'Check if the attendance is true for employee whose work, charge, and on call hour is 0.',
                'Check if the number of absent teammates is greater than the number of employees for a day.'
            ],
            'sql_validate': [
                '../sql/validate_timesheet_case_i.sql',
                '../sql/validate_timesheet_case_ii.sql',
                '../sql/validate_timesheet_case_iii.sql',
                '../sql/validate_timesheet_case_iv.sql'
            ]
        },
        {
            'database': 'data_validation',
            'table': 'qa_result',
            'test_table': 'product',
            'test_case': [
                'Check if the price is greater than MRP.',
                'Check if the duplicate product names do not have same price.',
                'Check if the product quantity in the sales table is more than the product quantity.',
                'Check if the price in the sales table do not match with the product price.'
            ],
            'sql_validate': [
                '../sql/validate_product_case_i.sql',
                '../sql/validate_product_case_ii.sql',
                '../sql/validate_product_case_iii.sql',
                '../sql/validate_product_case_iv.sql'
            ]
        },
        {
            'database': 'data_validation',
            'table': 'qa_result',
            'test_case': [
                'Check if the gross price is not equal to the product of price and sales quantity.',
                'Check if a bill number has different bill dates.',
                'Check if a bill has multiple customers.',
                'Check if the tax percent do not match with the tax percent in the product table.'
            ],
            'test_table': 'sales',
            'sql_validate': [
                '../sql/validate_sales_case_i.sql',
                '../sql/validate_sales_case_ii.sql',
                '../sql/validate_sales_case_iii.sql',
                '../sql/validate_sales_case_iv.sql'
            ]
        }
    ]

def main():
    create_db_table(create_table_info())
    validate_data(validate_data_info())

main()