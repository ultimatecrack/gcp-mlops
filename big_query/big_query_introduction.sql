SELECT
  Sex,
  avg(Age) avg_age
FROM `mlop-gcp.my_test_db.titanic`
group by 1


-- Check schemas
SELECT schema_name FROM
INFORMATION_SCHEMA.SCHEMATA;

-- Check tables
SELECT table_name FROM
`mlop-gcp.my_test_db.INFORMATION_SCHEMA.TABLES`;


-- Check table schema: 
SELECT * 
FROM `mlop-gcp.my_test_db.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'titanic';

-- DB statistics: 
SELECT 
  *
FROM `mlop-gcp.my_test_db.__TABLES__`
-- WHERE table_name = 'titanic'

-- Create non-partitioned table from CSV file: 
CREATE OR REPLACE EXTERNAL TABLE `mlop-gcp.my_test_db.titanic_external`
OPTIONS (
  format = 'CSV',
  uris = ['gs://mlops-gcp-1/titanic_data/titanic.csv']
);

-- Create parquet external table 
CREATE OR REPLACE EXTERNAL TABLE `mlop-gcp.my_test_db.titanic_external_with_partition` (
  Passengerid	INTEGER,
  Age FLOAT64,
  Fare FLOAT64,
  Sex	INTEGER,
  sibsp INTEGER,
  Parch INTEGER,
  Pclass INTEGER,
  Embarked INTEGER,
  Survived INTEGER	
  )
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mlops-gcp-1/titanic_partition_data/']
);

-- Create material view
CREATE OR REPLACE MATERIALIZED VIEW `mlop-gcp.my_test_db.titanic_material_view` AS
SELECT *
FROM `mlop-gcp.my_test_db.titanic`
WHERE Fare <= 50;

-- Check external table details
SELECT * FROM `project_id.INFORMATION_SCHEMA.TABLES`
WHERE table_name = 'titanic_external' AND table_schema = 'my_test_db';

-- Drop table
drop table if exists `mlop-gcp.my_test_db.titanic_external`


-- Big Query ML
-- Create Model
CREATE OR REPLACE MODEL
  `mlop-gcp.my_test_db.my_classification_model`
OPTIONS
  ( MODEL_TYPE='LOGISTIC_REG',
    AUTO_CLASS_WEIGHTS=TRUE ,
    input_label_cols=['Survived']) AS
SELECT 
Survived,
  Age,
  Fare,
  Sex,
  sibsp,
  Parch,
  Pclass,
  Embarked
FROM `mlop-gcp.my_test_db.titanic`
WHERE Passengerid <= 1150;

-- Evaluate 
SELECT * FROM ML.EVALUATE(MODEL `mlop-gcp.my_test_db.my_classification_model`, 
(SELECT
  Survived,
  Age,
  Fare,
  Sex,
  sibsp,
  Parch,
  Pclass,
  Embarked
  FROM `mlop-gcp.my_test_db.titanic` limit 100))

-- Predict
SELECT * FROM ML.PREDICT(MODEL `mlop-gcp.my_test_db.my_classification_model`, 
(SELECT
  Survived,
  Age,
  Fare,
  Sex,
  sibsp,
  Parch,
  Pclass,
  Embarked
  FROM `mlop-gcp.my_test_db.titanic` limit 100))