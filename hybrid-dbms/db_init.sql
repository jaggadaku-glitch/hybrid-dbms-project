USE hybriddb;

CREATE TABLE IF NOT EXISTS records (
  id CHAR(36) PRIMARY KEY,
  title TEXT,
  structured_json JSON,
  mongo_doc_id VARCHAR(64),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
