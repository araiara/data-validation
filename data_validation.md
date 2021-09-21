## Data Validation
### Create and Populated Database Tables
#### Table customer
~~~~ sql
CREATE TABLE IF NOT EXISTS customer (
  customer_id INT PRIMARY KEY,
  user_name VARCHAR(10) UNIQUE,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  town VARCHAR(255) NOT NULL,
  is_active BOOL NOT NULL
);

COPY customer
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\customer.csv'
DELIMITER ','
CSV HEADER;
~~~~
#### Table product
~~~~ sql
CREATE TABLE IF NOT EXISTS product (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(500) NOT NULL,   
  description VARCHAR(500) NOT NULL,
  price FLOAT NOT NULL,
  mrp FLOAT NOT NULL,
  pieces_per_case INT NOT NULL,
  weight_per_case FLOAT NOT NULL,
  uom CHAR(2) NOT NULL,
  brand VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  tax_percent FLOAT NOT NULL,
  active CHAR(1) NOT NULL,
  created_by VARCHAR(10) NULL,
  created_date TIMESTAMP NOT NULL,
  updated_by VARCHAR(10) NOT NULL,
  updated_date TIMESTAMP NOT NULL
);

COPY product
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\product.csv'
DELIMITER ','
CSV HEADER;
~~~~
#### Table sales
~~~~ sql
CREATE TABLE IF NOT EXISTS sales (
  id INT PRIMARY KEY,
  transaction_id INT NOT NULL,
  bill_no INT NOT NULL,
  bill_date TIMESTAMP NOT NULL,
  bill_location VARCHAR(255) NOT NULL,
  customer_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  uom CHAR(5) NOT NULL,
  price FLOAT NOT NULL,
  gross_price FLOAT NOT NULL,
  tax_pc FLOAT NOT NULL,
  tax_amt FLOAT NOT NULL,
  discount_pc FLOAT NOT NULL,
  discount_amt FLOAT NOT NULL,
  net_bill_amt FLOAT NOT NULL,
  created_by VARCHAR(255) NOT NULL,
  updated_by VARCHAR(255),
  created_date TIMESTAMP NOT NULL,  
  updated_date TIMESTAMP,
  CONSTRAINT fk_sales_customer_id
  FOREIGN KEY (customer_id)
  REFERENCES customer(customer_id),
  CONSTRAINT fk_sales_product_id
    FOREIGN KEY (product_id)
    REFERENCES product(product_id)
);

COPY sales
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\sales.csv'
DELIMITER ','
CSV HEADER;
~~~~
#### Create table employee_raw
~~~~ sql
CREATE TABLE IF NOT EXISTS employee_raw (
  employee_id VARCHAR(500),
  first_name VARCHAR(500),
  last_name VARCHAR(500),
  department_id VARCHAR(500),
  department_name VARCHAR(500),
  manager_employee_id VARCHAR(500),
  employee_role VARCHAR(500),
  salary VARCHAR(500),
  hire_date VARCHAR(500),
  terminated_date VARCHAR(500),
  terminated_reason VARCHAR(500),
  dob VARCHAR(500),
  fte VARCHAR(500),
  location VARCHAR(500)
);

COPY employee_raw
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\employee_raw.csv'
DELIMITER ','
CSV HEADER;
~~~~
#### Create table employee
~~~~ sql
CREATE TABLE IF NOT EXISTS employee (
  client_employee_id VARCHAR(255) PRIMARY KEY,
  department_id VARCHAR(255) NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  manager_employee_id VARCHAR(255),
  salary FLOAT NOT NULL,
  hire_date DATE NOT NULL,
  term_date DATE,
  term_reason VARCHAR(255),
  dob DATE NOT NULL,
  fte FLOAT NOT NULL,
  fte_status VARCHAR(255) NOT NULL,
  weekly_hours FLOAT NOT NULL,
  role VARCHAR(255) NOT NULL,
  is_active BOOL NOT NULL
);

COPY employee
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\employee.csv'
DELIMITER ','
CSV HEADER;
~~~~
#### Create table timesheet_raw
~~~~ sql
CREATE TABLE IF NOT EXISTS timesheet_raw (
  employee_id VARCHAR(500),
  cost_center VARCHAR(500),
  punch_in_time VARCHAR(500), 
  punch_out_time VARCHAR(500),
  punch_apply_date VARCHAR(500),
  hours_worked VARCHAR(500),
  paycode VARCHAR(500)
);

COPY timesheet_raw
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\timesheet_raw.csv'
DELIMITER ','
CSV HEADER;
~~~~
#### Create table timesheet
~~~~ sql
CREATE TABLE IF NOT EXISTS timesheet (
  id SERIAL PRIMARY KEY,
  employee_id VARCHAR(255) NOT NULL,
  department_id VARCHAR(255) NOT NULL,
  shift_start_time TIME,
  shift_end_time TIME,  
  shift_date DATE NOT NULL,
  shift_type VARCHAR(255) NOT NULL,
  hours_worked FLOAT NOT NULL,
  attendance BOOL NOT NULL,
  has_taken_break BOOL NOT NULL,
  break_hour FLOAT NOT NULL,
  was_charge BOOL NOT NULL,
  charge_hour FLOAT NOT NULL,
  was_on_call BOOL NOT NULL,
  on_call_hour FLOAT NOT NULL,
  num_teammates_absent INT NOT NULL,
  CONSTRAINT fk_timesheet_employee_id
    FOREIGN KEY (employee_id)
    REFERENCES employee(client_employee_id)
);

COPY timesheet (employee_id, department_id, shift_start_time, shift_end_time, shift_date, shift_type, hours_worked, attendance, has_taken_break, break_hour, was_charge, charge_hour, was_on_call, on_call_hour, num_teammates_absent)
FROM 'F:\lf-data-engineering-internship\week-4-validation\dataset\timesheet.csv'
DELIMITER ','
CSV HEADER;
~~~~

### Data Validation
#####  1. Check if a single employee is listed twice with multiple ids.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM (
  SELECT client_employee_id
  FROM employee
  EXCEPT
  SELECT DISTINCT client_employee_id
  FROM employee
) AS test_result;
~~~~
> Remarks: Test passed!
##### 2. Check if part time employees are assigned other fte_status.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM employee
where fte < 1 and fte_status <> 'Part Time';
~~~~
> Remarks: Test failed!
> 6 Part time employees assigned to other fte_status were found.
##### 3. Check if termed employees are marked as active.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM employee
WHERE term_date IS NULL AND is_active IS FALSE;
~~~~
> Remarks: Test passed!
##### 4. Check if the same product is listed more than once in a single bill.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM (
  SELECT COUNT(product_id) 
  FROM sales
  GROUP BY product_id, bill_no
  HAVING COUNT(product_id) <> 1
) AS test_result;
~~~~
> Remarks: Test passed!
##### 5. Check if the customer_id in the sales table does not exist in the customer table.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM (
  SELECT customer_id FROM sales
  EXCEPT
  SELECT customer_id FROM customer
) test_result;
~~~~
> Remarks: 6. Test passed!
##### Check if there are any records where updated_by is not empty but updated_date is empty.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM sales
WHERE updated_by IS NOT NULL 
AND updated_date IS NULL;
~~~~
> Remarks: Test failed!
> 57 records having updated_by value but NULL updated_date was found.
##### 7. Check if there are any hours worked that are greater than 24 hours.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM timesheet
WHERE hours_worked > 24;
~~~~
> Remarks: Test passed!
##### 8. Check if non on-call employees are set as on-call.
~~~~ sql
SELECT 
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM timesheet t
JOIN timesheet_raw tr
ON t.employee_id = tr.employee_id
AND t.shift_date = CAST(tr.punch_apply_date AS DATE)
AND tr.paycode = 'ON_CALL'
AND t.was_on_call IS NOT TRUE;
~~~~
> Remarks: Test passed!
##### 9. Check if the break is true for employees who have not taken a break at all.
~~~~ sql
SELECT 
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM timesheet t
JOIN timesheet_raw tr
ON t.employee_id = tr.employee_id
AND t.shift_date = CAST(tr.punch_apply_date AS DATE)
AND tr.paycode <> 'BREAK'
AND t.shift_start_time = CAST(tr.punch_in_time AS TIME)
AND t.shift_end_time = CAST(tr.punch_out_time AS TIME)
AND t.has_taken_break IS TRUE;
~~~~
> Remarks: Test passed!
##### 10. Check if the night shift is not assigned to the employees working on the night shift.
~~~~ sql
SELECT 
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM timesheet
WHERE shift_start_time BETWEEN '22:00' AND '6:00'
AND shift_type <> 'Night';
~~~~
> Remarks: Test passed!
#### 11. Check if username contains other than alphanumeric and underscore characters.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM customer
WHERE user_name NOT SIMILAR TO '[a-z]+/_*[a-z]+' ESCAPE '/';
~~~~
> Remarks: Test passed!
#### 12. Check if all the product_id in sales are present in the product table.
~~~~ sql
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM (
  SELECT product_id FROM sales
  EXCEPT
  SELECT product_id FROM product
) test_result;
~~~~
> Remarks: Test passed!
