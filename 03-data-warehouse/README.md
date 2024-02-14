# Data Warehouse and BigQuery

- [Slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit?usp=sharing)  
- [Big Query basic SQL](big_query.sql)

# Videos

## Data Warehouse

- Data Warehouse and BigQuery

[![](https://markdown-videos-api.jorgenkh.no/youtube/jrHljAoD6nM)](https://youtu.be/jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=34)


#### What is OLTP? 
Exploring transactional data processing
Online transactional processing (OLTP) is used for real-time execution of large volumes of database transactions by large numbers of people. OLTP systems are used for everyday transactions like ATMs, ecommerce purchases, online banking, text messages, and account changes, among many other day-to-day transactions.

These transactions use a relational database or SQL database to handle extensive volumes of simple transactions, enable multi-user access to the same data, process data quickly, provide index datasets for fast searches, and are available continually.

An OLTP system captures and maintains transaction data in a database. Each transaction involves individual database records made up of multiple fields or columns. This process can be challenging without the right tools.

In OLTP, the emphasis is on fast processing, because OLTP databases are read, written, and updated frequently. If a transaction fails, built-in system logic ensures data integrity.

OLTP systems can be used to provide data for their OLAP systems, as the two work together to optimize the value of data.

#### What is OLAP? Delving into multidimensional data analysis
Data analysts and data engineers use online analytical processing (OLAP) for data mining, analytics, and business intelligence. OLAP is used to process multidimensional analysis on large volumes of data at very high speeds (milliseconds). An OLTP system often processes and stores data in repositories, which OLAP then sources for analysis. Many businesses use OLAP for financial analysis, forecasting, budgeting, reporting, marketing and sales optimization, and decision making.

OLAP applies complex queries to large amounts of historical data aggregated from OLTP databases and other sources. In OLAP, the emphasis is on response time to these complex queries. Each query involves one or more columns of data aggregated from many rows. Examples include year-over-year financial performance or marketing lead generation trends. OLAP databases and data warehouses give analysts and decision-makers the ability to use custom reporting tools to turn data into information. Query failure in OLAP does not interrupt or delay transaction processing for customers, but it can delay or impact the accuracy of business intelligence insights.

#### Diferencies bewtween OLTP & OLAP:

![Alt text](/images/Screenshot%20from%202024-02-09%2012-07-50.png)

![Alt text](/images/Screenshot%20from%202024-02-09%2012-09-54.png)

#### What is a data warehouse
- OLAP solution
- Used for reporting and data analysis 

![Alt text](/images/Screenshot%20from%202024-02-09%2013-45-55.png)

#### BigQuery

- Serverless data warehouse 
-- There are no servers to manage or database software to install
- Software as well as infrastructure including 
    - scalability and high-availability
- Built-in features like 
    - machine learning
    - geospatial analysis
    - business intelligence
- BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage

#### Examples

Create a dataset in BigQuery and uploading .csv data to external table. And we'll comparing cost of quering different types of tables (partitioned, non-partitioned and clustered).

Let's to upload taxi data to GCS:

![Alt text](/images/Screenshot%20from%202024-02-10%2022-16-24.png)

```SQL
-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `mage-deploy-413517.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data11/trip_data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data11/trip_data/yellow_tripdata_2020-*.csv']
);

-- Check yello trip data
SELECT * FROM mage-deploy-413517.nytaxi.external_yellow_tripdata limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE mage-deploy-413517.nytaxi.yellow_tripdata_non_partitoned AS
SELECT * FROM mage-deploy-413517.nytaxi.external_yellow_tripdata;


-- Create a partitioned table from external table
CREATE OR REPLACE TABLE mage-deploy-413517.nytaxi.yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM mage-deploy-413517.nytaxi.external_yellow_tripdata;

-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM mage-deploy-413517.nytaxi.yellow_tripdata_non_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM mage-deploy-413517.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `mage-deploy-413517.nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE mage-deploy-413517.nytaxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM mage-deploy-413517.nytaxi.external_yellow_tripdata;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM mage-deploy-413517.nytaxi.yellow_tripdata_partitoned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM mage-deploy-413517.nytaxi.yellow_tripdata_partitoned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
  
```

## :movie_camera: Partitoning and clustering

- Partioning and Clustering

[![](https://markdown-videos-api.jorgenkh.no/youtube/-CqXf7vhhDs)](https://youtu.be/-CqXf7vhhDs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=35)

#### BigQuery partition

- Time-unit column
- Ingestion time (_PARTITIONTIME)
- Integer range partitioning
- When using Time unit or ingestion time
    - Daily (Default)
    - Hourly
    - Monthly or yearly
- Number of partitions limit is 4000

#### BigQuery Clustering

- Columns you specify are used to colocate related data
- Order of the column is important
- The order of the specified columns determines the sort order of the data.
- Clustering improves
    - Filter queries
    - Aggregate queries
- Table with data size < 1 GB, don’t show significant improvement with partitioning and clustering
- You can specify up to four clustering columns

#### BigQuery Clustering
Clustering columns must be top-level, non-repeated columns
- DATE
- BOOL
- GEOGRAPHY
- INT64
- NUMERIC
- BIGNUMERIC
- STRING
- TIMESTAMP
- DATETIME

#### Partitioning vs Clustering

![Alt text](/images/Screenshot%20from%202024-02-11%2015-53-41.png)

#### Clustering over paritioning

- Partitioning results in a small amount of data per partition (approximately less than 1 GB)
- Partitioning results in a large number of partitions beyond the limits on partitioned tables
- Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (for example, every few minutes)

#### Automatic reclustering
As data is added to a clustered table
- the newly inserted data can be written to blocks that contain key ranges that overlap with the key ranges in previously written blocks
- These overlapping keys weaken the sort property of the table

To maintain the performance characteristics of a clustered table
- BigQuery performs automatic re-clustering in the background to restore the sort property of the table
- For partitioned tables, clustering is maintained for data within the scope of each partition.

## :movie_camera: Best practices

[![](https://markdown-videos-api.jorgenkh.no/youtube/k81mLJVX08w)](https://youtu.be/k81mLJVX08w&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=36)

- Cost reduction
    - Avoid SELECT *
    - Price your queries before running them
    - Use clustered or partitioned tables
    - Use streaming inserts with caution
    - Materialize query results in stages
- Query performance
    - Filter on partitioned columns
    - Denormalizing data
    - Use nested or repeated columns
    - Use external data sources appropriately
    - Don't use it, in case u want a high query performance
    - Reduce data before using a JOIN
    - Do not treat WITH clauses as prepared statements
    - Avoid oversharding tables
    - Query performance
    - Avoid JavaScript user-defined functions
    - Use approximate aggregation functions (HyperLogLog++)
    - Order Last, for query operations to maximize performance
    - Optimize your join patterns
        - As a best practice, place the table with the largest number of rows first, followed by the table with the fewest rows, and then place the remaining tables by decreasing size.


## :movie_camera: Internals of BigQuery

[![](https://markdown-videos-api.jorgenkh.no/youtube/eduHi1inM4s)](https://youtu.be/eduHi1inM4s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=37)

A high-level architecture for BigQuery service:
![Alt text](/images/Screenshot%20from%202024-02-12%2018-51-14.png)

The difference between storing a record in record-oriented format:
![Alt text](/images/Screenshot%20from%202024-02-12%2018-53-01.png)

An example of Dremel serving tree:
![Alt text](/images/Screenshot%20from%202024-02-12%2018-54-05.png)



![Alt text](/images/Screenshot)



## Advanced topics

### :movie_camera: Machine Learning in Big Query

[![](https://markdown-videos-api.jorgenkh.no/youtube/B-WtpB0PuG4)](https://youtu.be/B-WtpB0PuG4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=34)

* [SQL for ML in BigQuery](big_query_ml.sql)

**Important links**

- [BigQuery ML Tutorials](https://cloud.google.com/bigquery-ml/docs/tutorials)
- [BigQuery ML Reference Parameter](https://cloud.google.com/bigquery-ml/docs/analytics-reference-patterns)
- [Hyper Parameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-glm)
- [Feature preprocessing](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-preprocess-overview)

### :movie_camera: Deploying Machine Learning model from BigQuery

[![](https://markdown-videos-api.jorgenkh.no/youtube/BjARzEWaznU)](https://youtu.be/BjARzEWaznU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=39)

- [Steps to extract and deploy model with docker](extract_model.md)  



# Homework

* [My Homework](/03-data-warehouse/homework/homework.md)

