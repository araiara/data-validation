CREATE TABLE IF NOT EXISTS qa_result (
  test_id SERIAL PRIMARY KEY,
  test_case VARCHAR(255) NOT NULL,
  test_case_desc VARCHAR(1000) NOT NULL,
  test_db VARCHAR(255) NOT NULL,
  impacted_record_count INT NOT NULL,
  test_result VARCHAR(10) NOT NULL
);
