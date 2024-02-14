## Homework-Module3

```SQL
-- -- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `mage-deploy-413517.green_taxi.external_green_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://nyc-green-taxi-data/green_taxi_data/green_tripdata_2022-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE mage-deploy-413517.green_taxi.internal_green_tripdata AS
SELECT * FROM mage-deploy-413517.green_taxi.external_green_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE mage-deploy-413517.green_taxi.green_tripdata_partitoned
PARTITION BY
  DATE(lpep_pickup_datetime) AS
SELECT * FROM mage-deploy-413517.green_taxi.external_green_tripdata;

-- Question 1. What is count of records for the 2022 Green Taxi Data?
SELECT COUNT(*) FROM mage-deploy-413517.green_taxi.external_green_tripdata;

-- Question 2. What is the estimated amount of data in the tables?
SELECT COUNT(DISTINCT PULocationID) FROM mage-deploy-413517.green_taxi.external_green_tripdata;
SELECT COUNT(DISTINCT PULocationID) FROM mage-deploy-413517.green_taxi.internal_green_tripdata;

-- Question 3. How many records have a fare_amount of 0?
SELECT COUNT(*) FROM mage-deploy-413517.green_taxi.external_green_tripdata WHERE fare_amount=0;

-- Question 4. What is the best strategy to make an optimized table in Big Query?
-- Impact of partition
-- Scanning 12.82MB of data
SELECT DISTINCT(VendorID)
FROM mage-deploy-413517.green_taxi.internal_green_tripdata
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Scanning ~1.12MB of DATA
SELECT DISTINCT(VendorID)
FROM mage-deploy-413517.green_taxi.green_tripdata_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Question 5. What's the size of the tables?
SELECT DISTINCT PULocationID FROM mage-deploy-413517.green_taxi.internal_green_tripdata
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

SELECT DISTINCT PULocationID FROM mage-deploy-413517.green_taxi.green_tripdata_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

```