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
  SELECT employee_id
  FROM timesheet
  GROUP BY employee_id, shift_start_time, shift_end_time, shift_date
  HAVING COUNT(department_id) > 1
) test_result;
