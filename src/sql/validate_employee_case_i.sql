INSERT INTO qa_result (test_case, test_case_desc, test_db, impacted_record_count, test_result)
SELECT
  %s,
  %s,
  %s,
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM (
  SELECT DISTINCT e.client_employee_id
  FROM employee e
  JOIN employee m
    ON e.client_employee_id = m.manager_employee_id
  WHERE e.role <> 'Manager'
) test_result;
