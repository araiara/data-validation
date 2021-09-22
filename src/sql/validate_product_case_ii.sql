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
  SELECT product_name, brand, COUNT(DISTINCT price) 
  FROM product
  GROUP BY product_name, brand
  HAVING COUNT(DISTINCT price) > 1
) test_result;
