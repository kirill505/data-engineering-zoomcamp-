
# Week 2: Workflow Orchestration

This is Week 2 on the Data Engineering Zoomcamp! 🚀😤 This week, we'll be covering workflow orchestration with Mage.

Mage is an open-source, hybrid framework for transforming and integrating data. ✨

In this week, I'll learn how to use the Mage platform to author and share _magical_ data pipelines. This will all be covered in the course, a bit more about Mage, check out our docs [here](https://docs.mage.ai/introduction/overview). 

* [2.2.1 - 📯 Intro to Orchestration](#221----intro-to-orchestration)
* [2.2.2 - 🧙‍♂️ Intro to Mage](#222---%EF%B8%8F-intro-to-mage)
* [2.2.3 - 🐘 ETL: API to Postgres](#223----etl-api-to-postgres)
* [2.2.4 - 🤓 ETL: API to GCS](#224----etl-api-to-gcs)
* [2.2.5 - 🔍 ETL: GCS to BigQuery](#225----etl-gcs-to-bigquery)
* [2.2.6 - 👨‍💻 Parameterized Execution](#226----parameterized-execution)
* [2.2.7 - 🤖 Deployment (Optional)](#227----deployment-optional)
* [2.2.8 - 🧱 Advanced Blocks (Optional)](#228----advanced-blocks-optional)
* [2.2.9 - 🗒️ Homework](#229---%EF%B8%8F-homework)
* [2.2.10 - 👣 Next Steps](#2210----next-steps)

## 📕 Course Resources

### 2.2.1 - 📯 Intro to Orchestration

In this section, we'll cover the basics of workflow orchestration. We'll discuss what it is, why it's important, and how it can be used to build data pipelines.

Videos
- 2.2.1a - [What is Orchestration?](https://www.youtube.com/watch?v=Li8-MWHhTbo&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We will be using:
- Docker
- And Mage would be running in this Docker environment
- Python, pandas
- Postgres, SQL
- Apache Arrow
- GCP platform tools
- And NYC taxi dataset.

![Alt text](/images/Screenshot%20from%202024-01-31%2011-11-32.png)

ETL
![Alt text](/images/Screenshot%20from%202024-01-31%2011-22-44.png)

What is Orchestration?

A large part of data engineering is extracting, transforming, and loading data between sources. 

Orghcestration is a process of dependency management, facilitated through automation.

A good goal is automate as many process as possible. And orchestration is one way to do that.

The data orchestration manages scheduling, triggering, monitoring, and even resource allocation. 

Every workflow requires sequential steps.

Data Engineer Lifecycle:
![Alt text](/images/Screenshot%20from%202024-01-31%2011-44-34.png)

A good orchestration handles
- Workflow management
- Automation
- Error handling
- Recovery
- Monitoring, alerting
- Resource optimization
- Observability
- Debugging
- Compliance/Auditing

![Alt text](/images/Screenshot%20from%202024-01-31%2012-03-38.png)

![Alt text](/images/Screenshot%20from%202024-01-31%2012-04-52.png)


Resources
- [Slides](https://docs.google.com/presentation/d/17zSxG5Z-tidmgY-9l7Al1cPmz4Slh4VPK6o2sryFYvw/)

### 2.2.2 - 🧙‍♂️ Intro to Mage

In this section, we'll introduce the Mage platform. We'll cover what makes Mage different from other orchestrators, the fundamental concepts behind Mage, and how to get started. To cap it off, we'll spin Mage up via Docker 🐳 and run a simple pipeline.

Videos
- 2.2.2a - [What is Mage?](https://www.youtube.com/watch?v=AicKRcK3pa4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

Summary

What is Mage?
An open-source pipeline tool for orchestration, transforming, and integrating data.

![Alt text](/images/Screenshot%20from%202024-01-31%2012-59-50.png)

Mage Engineering best-practicies built-in:

🧪 In-line testing and debugging
- Familiar, notebook-style format

🔎 Fully-featured observability.
- Transformation in one place: dbt models, streaming, & more.

🏜️ DRY principles.
- No more 🍝 DAGs with duplicate functions and weird imports. 
- DEaaS (sorry, I had to 😅)

![Alt text](/images/Screenshot%20from%202024-01-31%2013-14-21.png)

Mage Projects:
- A project forms the basis for all the work you can do in Mage— you can think of it like a GitHub repo. 
- It contains the code for all of your pipelines, blocks, and other assets.
- A Mage instance has one or more projects

Mage Pipelines:
- A pipeline is a workflow that executes some data operation— maybe extracting, transforming, and loading data from an API. They’re also called DAGs on other platforms
- In Mage, pipelines can contain Blocks (written in SQL, Python, or R) and charts. 
- Each pipeline is represented by a YAML file in the “pipelines” folder of your project.

Mage Blocks:
- A block is a file that can be executed independently or within a pipeline. 
- Together, blocks form Directed Acyclic Graphs (DAGs), which we call pipelines. 
- A block won’t start running in a pipeline until all its upstream dependencies are met.
- Blocks are reusable, atomic pieces of code that perform certain actions. 
- Changing one block will change it everywhere it’s used, but don’t worry, it’s easy to detach blocks to separate instances if necessary.
- Blocks can be used to perform a variety of actions, from simple data transformations to complex machine learning models.


2.2.2b - [Configuring Mage](https://www.youtube.com/watch?v=tNiV7Wp08XE?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

Summary
You can start by cloning the repo:

```bash
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```

Navigate to the repo:
```bash
cd mage-data-engineering-zoomcamp
```
Rename dev.env to simply .env— this will ensure the file is not committed to Git by accident, since it will contain credentials in the future.

Now, let's build the container

```bash
docker compose build
```

Finally, start the Docker container:

```bash 
docker compose up
```
Now, navigate to http://localhost:6789 in your browser! Voila! You're ready to get started with the course.

2.2.2c - [A Simple Pipeline](https://www.youtube.com/watch?v=stI-gg4QBnI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

There is some example:

Data loader:
```python
import io
import pandas as pd
import requests
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Template for loading data from API
    """
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv?raw=True'

    return pd.read_csv(url)

    
@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'

```
Data transformer:

```python
from pandas import DataFrame
import math

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def select_number_columns(df: DataFrame) -> DataFrame:
    return df[['Age', 'Fare', 'Parch', 'Pclass', 'SibSp', 'Survived']]


def fill_missing_values_with_median(df: DataFrame) -> DataFrame:
    for col in df.columns:
        values = sorted(df[col].dropna().tolist())
        median_age = values[math.floor(len(values) / 2)]
        df[[col]] = df[[col]].fillna(median_age)
    return df


@transformer
def transform_df(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        df (DataFrame): Data frame from parent block.

    Returns:
        DataFrame: Transformed data frame
    """
    # Specify your transformation logic here

    return fill_missing_values_with_median(select_number_columns(df))


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'


```

Data export:
```python
from mage_ai.io.file import FileIO
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_file(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to filesystem.

    Docs: https://docs.mage.ai/design/data-loading#example-loading-data-from-a-file
    """
    filepath = 'titanic_clean.csv'
    FileIO().export(df, filepath)
```

Resources
- [Getting Started Repo](https://github.com/mage-ai/mage-zoomcamp)
- [Slides](https://docs.google.com/presentation/d/1y_5p3sxr6Xh1RqE6N8o2280gUzAdiic2hPhYUUD6l88/)

### 2.2.3 - 🐘 ETL: API to Postgres

Hooray! Mage is up and running. Now, let's build a _real_ pipeline. In this section, we'll build a simple ETL pipeline that loads data from an API into a Postgres database. Our database will be built using Docker— it will be running locally, but it's the same as if it were running in the cloud.

Videos
2.2.3a - [Configuring Postgres](https://www.youtube.com/watch?v=pmhI-ezd3BE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We have a new profile in io_config.yaml and define some variables:
```yaml
dev:
    # PostgresSQL
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{ env_var('POSTGRES_DBNAME') }}"
  POSTGRES_SCHEMA: "{{ env_var('POSTGRES_SCHEMA') }}" # Optional
  POSTGRES_USER: "{{ env_var('POSTGRES_USER') }}"
  POSTGRES_PASSWORD: "{{ env_var('POSTGRES_PASSWORD') }}"
  POSTGRES_HOST: "{{ env_var('POSTGRES_HOST') }}"
  POSTGRES_PORT: "{{ env_var('POSTGRES_PORT') }}"

```

We will create a new pipeline:
- Go to http://localhost:6789/pipelines
- And create a new New->Standart(Batch):

![Alt text](/images/Screenshot%20from%202024-01-31%2017-09-20.png)


Then we will create a new SQL Data Loader:

![Alt text](/images/Screenshot%20from%202024-01-31%2017-11-21.png)

Choose a connection (PostgreSQL), a profile (dev) and "Use a raw SQL". And we can make a simple query:

![Alt text](/images/Screenshot%20from%202024-01-31%2017-14-53.png)

We may see a Postgres connection is established!

2.2.3b - [Writing an ETL Pipeline](https://www.youtube.com/watch?v=Maidfe7oKLs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We have to start a new pipeline:
![Alt text](/images/Screenshot%20from%202024-01-31%2017-09-20.png)


Then we will create a new Python API Data Loader:

![Alt text](/images/Screenshot%20from%202024-01-31%2017-11-21.png)

To a start we have to declare data types:
```python
    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float, 
        'RatecCodeID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'payment_type': pd.Int64Dtype(),
        'fare_amount': float, 
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float, 
        'improvement_surcharge': float,
        'total_amount': float,
        'congestion_surcharge': float

    }
```

And we have to feed dates columns to parsing by pandas:
```python
parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
```

Finally our Data Loader would be:
```python
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float, 
        'RatecCodeID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'payment_type': pd.Int64Dtype(),
        'fare_amount': float, 
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float, 
        'improvement_surcharge': float,
        'total_amount': float,
        'congestion_surcharge': float

    }

    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    return pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

```

And then we'll be do some transformation block. We will clean data with zero "passenger_count"
```python
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    return data[data['passenger_count'] > 0]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'Ther are rides with zero passengers'

```

Then we will do some Export Block using profile created in previous step (dev), and declaring schema name and table name:

```python
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'ny_taxi'  # Specify the name of the schema to export data to
    table_name = 'yellow_cab_data'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )

```

For checking we did all right, we can add some SQL Data Loader and make query for counting columns amount:

![Alt text](/images/Screenshot%20from%202024-02-02%2013-33-35.png)

Beautiful, we know the data is there! Data is reading from API and written to a Postgres.


Resources
- [Taxi Dataset](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz)
- [Sample loading block](https://github.com/mage-ai/mage-zoomcamp/blob/solutions/magic-zoomcamp/data_loaders/load_nyc_taxi_data.py)


### 2.2.4 - 🤓 ETL: API to GCS

Ok, so we've written data _locally_ to a database, but what about the cloud? In this tutorial, we'll walk through the process of using Mage to extract, transform, and load data from an API to Google Cloud Storage (GCS). 

We'll cover both writing _partitioned_ and _unpartitioned_ data to GCS and discuss _why_ you might want to do one over the other. Many data teams start with extracting data from a source and writing it to a data lake _before_ loading it to a structured data source, like a database.

Videos
2.2.4a - [Configuring GCP](https://www.youtube.com/watch?v=00LP360iYvE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We are gonna to create a new bucket on GCP with default suggested settings:

![Alt text](/images/Screenshot%20from%202024-02-03%2010-12-00.png)

We've created a Cloud Storage bucket!

Next! We have to create Service Account and added Owner role, we would sure everything will work, but it's not secure!

![Alt text](/images/Screenshot%20from%202024-02-03%2010-18-32.png)

We've done our credentials.
Then we go inside just created credentials and we need to create new Keys

![Alt text](/images/Screenshot%20from%202024-02-03%2010-21-29.png)

And then we have to copy our credentials .json file into mage directory.
Further we will define credentials in io-config.yml:

```yaml
GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/dtc-342332-13422b3asdf48ed.json"
  GOOGLE_LOCATION: US # Optional
```
This credentials would be see by mage, because all files in mounted volume would be allow inside docker
```docker 
volumes:
    - .:/home/src/
```

And now mage would know about credentials

We can test our connection to BigQuery, creating new SQL Data Loader:
![Alt text](/images/Screenshot%20from%202024-02-03%2010-33-17.png)

What we actully gonna do, upload titanic dataset to GCP. But in this case we gonna copy just drag and drop file titanic_clean.csv into GCP bucket:

![Alt text](/images/Screenshot%20from%202024-02-03%2010-39-20.png)
We would be editing our test pipeline adding new Python Google Cloud Storage Data Loader:
![Alt text](/images/Screenshot%20from%202024-02-03%2010-41-44.png)

![Alt text](/images/Screenshot%20from%202024-02-03%2010-44-11.png)

We can see data are loaded from bucket. This connection is work.
![Alt text](/images/Screenshot%20from%202024-02-03%2010-44-53.png)


2.2.4b - [Writing an ETL Pipeline](https://www.youtube.com/watch?v=w0XmcASRUnc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

At this part we will create pipeline for uploading data to GCP.
Creating a new pipeline, and adding new Data Loader from previous steps load_api_data.py
![Alt text](/images/Screenshot%20from%202024-02-03%2015-47-38.png)

Also we adding a new Data Transform block:
![Alt text](/images/Screenshot%20from%202024-02-03%2015-48-52.png)

Then we creating new Python Google Cloud Data Exporter:
![Alt text](/images/Screenshot%20from%202024-02-03%2015-55-32.png)

Running all upstream block, and we can see data is uploaded to GCP bucket:
![Alt text](/images/Screenshot%20from%202024-02-03%2015-56-45.png)

What elese we wanna do? Create a more advance method to Export Data using partitioning and saving in .parquet. For that adding new Export block.
We will define credentials:
```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/dtc-de-406412-132b3ae748ed.json"
```

Define bucket_name, project id and table tame:
```python
bucket_name = 'mage-zoomcamp-2'
project_id = 'dtc-de-406412'

table_name = "nyx_taxi_data"

root_path = f"{bucket_name}/{table_name}"
```

We will use 'tpep_pickup_date' to partitioning:
```python
data['tpep_pickup_datetime'] = data['tpep_pickup_datetime'].dt.date
```

```python
Reading dataframe into PyArrow table
table = pa.Table.from_pandas(data)

Define FileSystem:
gcs = pa.fs.GcsFileSystem()

And write to dataset:
pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['tpep_pickup_datetime'],
        filesystem=gcs
    )
```

Finally the whole Data Exporter block:
![Alt text](/images/Screenshot%20from%202024-02-03%2018-26-58.png)

Resources
- [DTC Zoomcamp GCP Setup](../week_1_basics_n_setup/1_terraform_gcp/2_gcp_overview.md)

### 2.2.5 - 🔍 ETL: GCS to BigQuery

Now that we've written data to GCS, let's load it into BigQuery. In this section, we'll walk through the process of using Mage to load our data from GCS to BigQuery. This closely mirrors a very common data engineering workflow: loading data from a data lake into a data warehouse.

Videos
- 2.2.5a - [Writing an ETL Pipeline](https://www.youtube.com/watch?v=JKp_uzM-XsM)

We're going to to take the data that we wrote to Google Cloud Storage, process it and write it to Google BigQuery. So create a new batch pipeline
![Alt text](/images/Screenshot%20from%202024-01-31%2017-09-20.png)

So on create a new Python GCS Data Loader
![Alt text](/images/Screenshot%20from%202024-02-03%2022-44-57.png)

So now we're going to do a little transformation and standardize our column names:
![Alt text](/images/Screenshot%20from%202024-02-03%2022-48-29.png)

And now we'll export our data use a SQL Exporter 
![Alt text](/images/Screenshot%20from%202024-02-03%2022-52-02.png)

We've taken the data from GCS, read into Mage, and then exported it to bigquery!

And then we can scheduling our pipeline. We're going to create a new trigger:
![Alt text](/images/Screenshot%20from%202024-02-03%2023-04-40.png)

![Alt text](/images/Screenshot%20from%202024-02-03%2023-06-26.png)

### 2.2.6 - 👨‍💻 Parameterized Execution

By now you're familiar with building pipelines, but what about adding parameters? In this video, we'll discuss some built-in runtime variables that exist in Mage and show you how to define your own! We'll also cover how to use these variables to parameterize your pipelines. Finally, we'll talk about what it means to *backfill* a pipeline and how to do it in Mage.

Videos
2.2.6a - [Parameterized Execution](https://www.youtube.com/watch?v=H0hWjWxB-rg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We'll create a different .parquet file for each day using runtime variables

Every Mage block has keyword arguments and that contains a number of parameteres. Getting execrution date:
```python
now = kwargs.get('execution_date')
```

Sett up file name and confuguriation files:
```python
now_fpath = now.strftime("%Y/%m/%d")

config_path = path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'

bucket_name = 'mage-zoomcamp-2'
object_key = f'{now_fpath}/daily-trips.parquet'

GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )
```
Finally our Data Exporter look like:
![Alt text](/images/Screenshot%20from%202024-02-05%2011-02-23.png)

As we can see data is on GCS in apropriate folder:
![Alt text](/images/Screenshot%20from%202024-02-05%2011-01-02.png)


2.2.6b - [Backfills](https://www.youtube.com/watch?v=ZoeC6Ag5gQc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We can parameterized running our pipeline usind data execution:

![Alt text](/images/Screenshot%20from%202024-02-05%2013-36-56.png)


Resources
- [Mage Variables Overview](https://docs.mage.ai/development/variables/overview)
- [Mage Runtime Variables](https://docs.mage.ai/getting-started/runtime-variable)

### 2.2.7 - 🤖 Deployment (Optional)

In this section, we'll cover deploying Mage using Terraform and Google Cloud. This section is optional— it's not *necessary* to learn Mage, but it might be helpful if you're interested in creating a fully deployed project. If you're using Mage in your final project, you'll need to deploy it to the cloud.

Videos
2.2.7a - [Deployment Prerequisites](https://www.youtube.com/watch?v=zAwAX5sxqsg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

#### Install Terraform
Ensure that your system is up to date and you have installed the gnupg, software-properties-common, and curl packages installed. You will use these packages to verify HashiCorp's GPG signature and install HashiCorp's Debian package repository.
```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
```

Install the HashiCorp GPG key.
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
```

Verify the key's fingerprint.
```bash
gpg --no-default-keyring \
--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
--fingerprint
```

Add the official HashiCorp repository to your system. The lsb_release -cs command finds the distribution release codename for your current system, such as buster, groovy, or sid.
```bash
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list
```

Download the package information from HashiCorp.
```bash
sudo apt update
```

Install Terraform from the new repository.
```bash
sudo apt-get install terraform
```

Verify that the installation worked by opening a new terminal session and listing Terraform's available subcommands.
```bash
terraform -help
```

#### Install the gcloud CLI
Import the Google Cloud public key.
```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
```

Add the gcloud CLI distribution URI as a package source.
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
```

Update and install the gcloud CLI:
```bash
sudo apt-get update && sudo apt-get install google-cloud-cli
```

Run gcloud init to get started
```bash
gcloud init
```

2.2.7b - [Google Cloud Permissions](https://www.youtube.com/watch?v=O_H7DCmq2rA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

We're going to setup permissions for Service Account:
![Alt text](/images/Screenshot%20from%202024-02-06%2014-38-25.png)

2.2.7c - [Deploying to Google Cloud - Part 1](https://www.youtube.com/watch?v=9A872B5hb_0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

Preparing Google Cloud:
- Set `GOOGLE_APPLICATION_CREDENTIALS` to point to the file

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json
```

- Now authenticate:

```bash
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

2.2.7d - [Deploying to Google Cloud - Part 2](https://www.youtube.com/watch?v=0YExsb2HgLI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

```bash
git clone https://github.com/mage-ai/mage-ai-terraform-templates

cd mage-ai-terraform-templates
```

Project ID (REQUIRED):

Before running any Terraform commands, please change the default value of the variable named project_id in the ./gcp/variables.tf file.


```yaml
variable "project_id" {
  type        = string
  description = "The name of the project"
  default     = "unique-gcp-project-id"
}
```


Creating secrets:

1. Go to Google Secret Manager UI.
2. Click the button at the top labeled + CREATE SECRET.
3. Fill in the name of your secret; e.g. bigquery_credentials.
4. Under Secret value, upload your service account credentials JSON file or paste the JSON into the text area labeled Secret value.
5. Scroll all the way down and click the button CREATE SECRET.

You can mount secrets from Google Secret Manager through Terraform configurations or through the Google Console UI.

Secrets Terraform configurations:

1. Once you save a secret in Google Secret Manager, click on the PERMISSIONS tab.
2. Click the button + GRANT ACCESS.
3. Under the field labeled New principles, add the service account that is associated to your Google Cloud Run
4. Under the field labeled Select a role, enter the value Secret Manager Secret Accessor.
5. Click the button SAVE.
6. Mount secrets to Google Cloud Run via Terraform in the file ./gcp/main.tf:

```yaml
resource "google_cloud_run_service" "run_service" {
  ...

  template {
    spec {
      containers {
        ...
        env {
          name = "path_to_keyfile"
          value = "/secrets/bigquery/bigquery_credentials"
        }
        volume_mounts {
          name       = "secrets-bigquery_credentials"
          mount_path = "/secrets/bigquery"
        }
      }
      volumes {
        name = "secrets-bigquery_credentials"
        secret {
          secret_name  = "bigquery_credentials"
          items {
            key  = "latest"
            path = "bigquery_credentials"
          }
        }
      }
    }
  }
}
```

Deploy:

1. Change directory into scripts folder:

```bash
cd gcp
```

2. Initialize Terraform:

```bash
terraform init

```
A sample output could look like this:


```bash
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/google versions matching ">= 3.3.0"...
- Finding latest version of hashicorp/http...
- Installing hashicorp/google v4.38.0...
- Installed hashicorp/google v4.38.0 (signed by HashiCorp)
- Installing hashicorp/http v3.1.0...
- Installed hashicorp/http v3.1.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

3. Deploy:

```bash
terraform apply
```

A sample output could look like this:

```bash
Apply complete! Resources: 7 added, 1 changed, 0 destroyed.

Outputs:

service_ip = "34.107.187.208"
```

It’ll take a few minutes for GCP Cloud Run to start up and be ready to receive requests.


After a few minutes, open a browser and go to http://[IP_address]

Resources
- [Installing Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- [Installing `gcloud` CLI](https://cloud.google.com/sdk/docs/install)
- [Mage Terraform Templates](https://github.com/mage-ai/mage-ai-terraform-templates)

Additional Mage Guides
- [Terraform](https://docs.mage.ai/production/deploying-to-cloud/using-terraform)
- [Deploying to GCP with Terraform](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)

### 2.2.8 - 🗒️ Homework 

My homework [here](/02-workflow-orchestration/homework)

### 📑 Additional Resources

- [Mage Docs](https://docs.mage.ai/)
- [Mage Guides](https://docs.mage.ai/guides)
- [Mage Slack](https://www.mage.ai/chat)
