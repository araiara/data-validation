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
FROM timesheet
WHERE attendance IS TRUE
  AND hours_worked = 0
  AND charge_hour = 0
  AND on_call_hour = 0;
