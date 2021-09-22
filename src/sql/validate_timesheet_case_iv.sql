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
  SELECT COUNT(employee_id), shift_date
  FROM timesheet
  GROUP BY shift_date
  HAVING AVG(num_teammates_absent) > COUNT(employee_id)
) test_result;
