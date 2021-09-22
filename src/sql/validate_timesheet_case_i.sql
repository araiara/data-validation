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
  SELECT t.employee_id, e.term_date, shift_date
  FROM timesheet t
  JOIN employee e
    ON t.employee_id = e.client_employee_id
  WHERE e.is_active IS FALSE
    AND t.shift_date > e.term_date
) test_result;
