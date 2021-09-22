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
  SELECT bill_no, COUNT(DISTINCT bill_date)
  FROM sales
  GROUP BY bill_no
  HAVING COUNT(DISTINCT bill_date) > 1
) test_result;
