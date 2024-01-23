# Docker + Postgres

## Docker

- Docker allows you to put everything an application needs inside a container - sort of a box that contains everything: OS, system-level libraries, python, etc.
- You run this box on a host machine. The container is completely isolated from the host machine env.
- In the container you can have Ubuntu 18.04, while your host is running on Windows.
- You can run multiple containers on one host and they won’t have any conflict.
- An image = set of instructions that were executed + state. All saved in “image”
- Installing docker: [https://docs.docker.com/get-docker/](https://www.google.com/url?q=https://docs.docker.com/get-docker/&sa=D&source=editors&ust=1700517631232261&usg=AOvVaw3Haqlkw0GAhFb8vrMcnsc0)

Why should data engineers care about containerization and docker?

- Setting up things locally for experiments
- Integration tests, CI/CD
- Batch jobs (AWS Batch, Kubernetes jobs, etc — outside of the scope)
- Spark
- Serverless (AWS Lambda)
- So containers are everywhere

Simple example

- Python 3.9
- Extend it - install some libraries like pandas
- More - next

Run hello-world:
```
docker run hello-world
```
Run containter in interactive mode:
```
docker run -it ubuntu bash
-it -- parameter for interactive mode
-ubuntu --container name
-bash -- entrypoint
```
Example of Dockerfile:
```
FROM python:3.9

RUN pip install pandas

ENTRYPOINT ["bash"]
```
And then we have to build:
```
docker build -t test:pandas
```
## Postgres

- For practicing with SQL, we’ll use Postgres
- It’s a general purpose database - for transitions, not for analytics
- But it’s powerful enough and sometimes also used as a data warehouse - a special database for analytical queries (more in week 3)
- We can set it up locally to practice SQL and test things before doing this in the cloud

**NY Trips Dataset**

- [https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)

> According to the TLC data website, from 05/13/2022, the data will be in .parquet format instead of .csv The website has provided a useful link with sample steps to read .parquet file and convert it to Pandas data frame.
> 
> 
> You can use the csv backup located here, [https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz), to follow along with the video.
> 

Downloading the data

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

Running postgres with Docker (taken from Airflow’s environment - you’ll see it later in the next week)

```docker
docker run -it \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxi" \
	-v "./ny-taxi-volume:/var/lib/postgresql/data" \
	-p 5432:5432 \
	postgres:13
```

It’s running, now let’s test it

I assume you have Python. If you don’t, I recommend Anaconda - [https://www.anaconda.com/products/individual](https://www.google.com/url?q=https://www.anaconda.com/products/individual&sa=D&source=editors&ust=1700517631235009&usg=AOvVaw19wki-_byuPmxWoq-jJBoz). It’s simpler to install than other Python distributions + it already has a lot of useful libraries

```bash
pip install pgcli
```

This installs a client for postgres that we’ll use

Let’s connect to it:

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

And check what’s there

```bash
\dt
```

Not much. Let’s put some data

## Taxi Rides dataset + putting data to Postgres

Download the dataset: [https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page](https://www.google.com/url?q=https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page&sa=D&source=editors&ust=1700517631236710&usg=AOvVaw39NzQAh1dg0tNHqXgBKDXd)

[https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv](https://www.google.com/url?q=https://s3.amazonaws.com/nyc-tlc/trip%2Bdata/yellow_tripdata_2021-01.csv&sa=D&source=editors&ust=1700517631237164&usg=AOvVaw11SnbvFaf4lUArrsouiIH4)

Let’s take a look at the data.

- Less
- Libre office calc or excel
- Python: Pandas + Jupyter
- How to install pandas and jupyter if you’re not on anaconda
- “Data dictionary” - [https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf](https://www.google.com/url?q=https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf&sa=D&source=editors&ust=1700517631237883&usg=AOvVaw1UuR9hnj9aJlhuVRwJrwYm)
- Zones - [https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv](https://www.google.com/url?q=https://s3.amazonaws.com/nyc-tlc/misc/taxi%2B_zone_lookup.csv&sa=D&source=editors&ust=1700517631238126&usg=AOvVaw3Ekc7YRc2psYbzKBi4zhdF)

We’ll have a simple Python script for doing that (based on [https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table](https://www.google.com/url?q=https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table&sa=D&source=editors&ust=1700517631238418&usg=AOvVaw0SPdASoLtSg-UG3c8Xtefg))

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```

Looking at types + DDL

```python
print(pd.io.sql.get_schema(df, 'yellow_taxi', con=engine))
```

```sql
CREATE TABLE yellow_taxi (
        "VendorID" BIGINT,
        tpep_pickup_datetime TEXT,
        tpep_dropoff_datetime TEXT,
        passenger_count BIGINT,
        trip_distance FLOAT(53),
        "RatecodeID" BIGINT,
        store_and_fwd_flag TEXT,
        "PULocationID" BIGINT,
        "DOLocationID" BIGINT,
        payment_type BIGINT,
        fare_amount FLOAT(53),
        extra FLOAT(53),
        mta_tax FLOAT(53),
        tip_amount FLOAT(53),
        tolls_amount FLOAT(53),
        improvement_surcharge FLOAT(53),
        total_amount FLOAT(53),
        congestion_surcharge FLOAT(53)
)
```

- Types - not optimal
- Also, dates as text (pd.to_datetime)
- Better types: https://www.singlestore.com/blog/nyc-taxi-data-ingested-into-memsql/

Create table:

```python
df.head(0).to_sql('yellow_taxi', engine, if_exists='replace', index=False)
```

Insert data:

```python
df.to_sql('yellow_taxi', engine, if_exists='append', index=False)
```

## pgAdmin

- It’s not convenient to use pgcli for data exploration and querying
- pgAdmin - the standard graphical tool for postgres for that - [https://www.pgadmin.org/](https://www.google.com/url?q=https://www.pgadmin.org/&sa=D&source=editors&ust=1700517631241341&usg=AOvVaw3XyQwr6LGFVyYK6d132SFZ)
- Let’s also run it with docker

```bash
docker run -it \
	-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
	-e PGADMIN_DEFAULT_PASSWORD="root" \
	-p 8080:80 \
	dpage/pgadmin4
```

However, this docker container can’t access the postgres container. We need to link them

### Data ingestion

Running locally

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```

Build the image

`docker build -t taxi_ingest:v001 .`

## Docker network

Create a network

```bash
docker network create pg-network
```

Run Postgres (change the path):

```bash
docker run -it \
	-e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxi" \
	-v "./ny-taxi-volume:/var/lib/postgresql/data" \
	-p 5432:5432 \
	--name pgdatabase \
	--net pg \
	postgres:13
```

Run pgAdmin

```bash
docker run -it \
	-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
	-e PGADMIN_DEFAULT_PASSWORD="root" \
	-p 8080:80 \
	--name pgadmin \
	--net pg \
	dpage/pgadmin4
```

It works, but we need to keep two terminal tabs running, manually create a network - and a bunch of other things. Let’s use compose that will take care of that.

## Docker compose

It lets us run multiple containers and link them in a network

If you have docker desktop (windows and mac), you already have docker compose

On Linux, you need to install it [https://docs.docker.com/compose/install/](https://www.google.com/url?q=https://docs.docker.com/compose/install/&sa=D&source=editors&ust=1700517631243724&usg=AOvVaw00vUvp6wxojEE-qPSrgDRG)

Let’s create docker-compose.yaml

```yaml
services:
	pgdatabase:
		image: postgres:13
		restart: always
		environment:
			POSTGRES_USER: root
			POSTGRES_PASSWORD: root
			POSTGRES_DB: ny_taxi
		volumes:
			- "./ny-taxi-volume:/var/lib/postgresql/data:rw"
		ports:
			- "5432:5432"
	pgadmin:
		image: dpage/pgadmin4
		restart: always
		environment:
			PGADMIN_DEFAULT_EMAIL: admin@admin.com
			PGADMIN_DEFAULT_PASSWORD: root
		ports:
			- "8080:80"
```

And then do 

### Docker-Compose

Run it:

```bash
docker-compose up
```

Run in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```

And then create a database connection using pgdatabase

## SQL

Finally let’s do SQL

(To be updated)

Vic’s queries:

[https://lh7-us.googleusercontent.com/YQmzF00scc5Q-cT7A5MGYnWb5U9nc3pUxeIX3fXXoZyICPghoUCQLEW98fQGG4RUl13g9Y8UTGA8qHWTiBsxaQT4_ja6uHgqPsXzvpnkr4wVmHKjRvw7XwqhGcJUjuGPKxGeArCgtRemjwn_X7T90Q](https://lh7-us.googleusercontent.com/YQmzF00scc5Q-cT7A5MGYnWb5U9nc3pUxeIX3fXXoZyICPghoUCQLEW98fQGG4RUl13g9Y8UTGA8qHWTiBsxaQT4_ja6uHgqPsXzvpnkr4wVmHKjRvw7XwqhGcJUjuGPKxGeArCgtRemjwn_X7T90Q)

[https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_analytics_engineering/taxi_rides_ny/models/data-marts/dm_monthly_zone_revenue.sql](https://www.google.com/url?q=https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_analytics_engineering/taxi_rides_ny/models/data-marts/dm_monthly_zone_revenue.sql&sa=D&source=editors&ust=1700517631247517&usg=AOvVaw0SLeTmGxho72zmUEn4NEtz)

[https://lh7-us.googleusercontent.com/LcOpIvHExQtlOqGQCzOOHeb-akJ6x_fRIqKpZO5AWlUu1QexrpZx0I5gXl6S-Wchk7_IepWkSUE15sYPbv3TxTuIyEbDBnEIaVWzV13K-hpxMRse-ilQD-W_51e2X_iYCQWNj6VjJhMSUCZAnMkcyw](https://lh7-us.googleusercontent.com/LcOpIvHExQtlOqGQCzOOHeb-akJ6x_fRIqKpZO5AWlUu1QexrpZx0I5gXl6S-Wchk7_IepWkSUE15sYPbv3TxTuIyEbDBnEIaVWzV13K-hpxMRse-ilQD-W_51e2X_iYCQWNj6VjJhMSUCZAnMkcyw)

[https://lh7-us.googleusercontent.com/6ujVcHkshu6hWqoRqTSX6amHdAiMs1GqWWs0rxuiqMCJQTuke270soX5vNIOGouW6ii_xfdWQrSZhonqpThrFKuRONhOnr1jK36BDgfK6c2zPDAksZtKMrYdPnQ4ZDn98gPzlprmZ9qBwBrfg5pyCw](https://lh7-us.googleusercontent.com/6ujVcHkshu6hWqoRqTSX6amHdAiMs1GqWWs0rxuiqMCJQTuke270soX5vNIOGouW6ii_xfdWQrSZhonqpThrFKuRONhOnr1jK36BDgfK6c2zPDAksZtKMrYdPnQ4ZDn98gPzlprmZ9qBwBrfg5pyCw)

[https://lh7-us.googleusercontent.com/3__ODPrnIvBbUpvhZGKz6YEgJ6WSILiCOER5N8dYbBV8iJoKuVYaODx03GSCRRrpcwf7rpFTaXQbJsRs5VjKBr2arl7u9DncVK5gU07CQIjCl5fKly0QrX60p9Sy3smjbtcMbQJ_EAqIjlsGbqonag](https://lh7-us.googleusercontent.com/3__ODPrnIvBbUpvhZGKz6YEgJ6WSILiCOER5N8dYbBV8iJoKuVYaODx03GSCRRrpcwf7rpFTaXQbJsRs5VjKBr2arl7u9DncVK5gU07CQIjCl5fKly0QrX60p9Sy3smjbtcMbQJ_EAqIjlsGbqonag)


# Terraform&GCP

## GCP Overview

[Video](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=2)

### Project infrastructure modules in GCP:

- Google Cloud Storage (GCS): Data Lake
- BigQuery: Data Warehouse

(Concepts explained in Week 2 - Data Ingestion)

### Initial Setup

For this course, we'll use a free version (upto EUR 300 credits).

1. Create an account with your Google email ID
2. Setup your first [project](https://console.cloud.google.com/) if you haven't already
    - eg. "DTC DE Course", and note down the "Project ID" (we'll use this later when deploying infra with TF)
3. Setup [service account & authentication](https://cloud.google.com/docs/authentication/getting-started) for this project
    - Grant `Viewer` role to begin with.
    - Download service-account-keys (.json) for auth.
4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup

### Google Cloud SDK Authentication

- Now create a service account and generate keys like shown in the videos
- Download the key and put it to some location, e.g. `.gc/ny-rides.json`
- Set `GOOGLE_APPLICATION_CREDENTIALS` to point to the file

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json
```

Now authenticate:

```bash
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

Alternatively, you can authenticate using OAuth like shown in the video

`gcloud auth application-default login`

### Setup for Access

1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
    - Go to the *IAM* section of *IAM & Admin* [https://console.cloud.google.com/iam-admin/iam](https://console.cloud.google.com/iam-admin/iam)
    - Click the *Edit principal* icon for your service account.
    - Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
2. Enable these APIs for your project:
    - [https://console.cloud.google.com/apis/library/iam.googleapis.com](https://console.cloud.google.com/apis/library/iam.googleapis.com)
    - [https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)

### Terraform Workshop to create GCP Infra

Continue [here](https://www.notion.so/terraform): `week_1_basics_n_setup/1_terraform_gcp/terraform`

## Terraform Overview

[Video](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=2)

### Concepts

### Introduction

1. What is [Terraform](https://www.terraform.io/)?
    - open-source tool by [HashiCorp](https://www.hashicorp.com/), used for provisioning infrastructure resources
    - supports DevOps best practices for change management
    - Managing configuration files in source control to maintain an ideal provisioning state for testing and production environments
2. What is IaC?
    - Infrastructure-as-Code
    - build, change, and manage your infrastructure in a safe, consistent, and repeatable way by defining resource configurations that you can version, reuse, and share.
3. Some advantages
    - Infrastructure lifecycle management
    - Version control commits
    - Very useful for stack-based deployments, and with cloud providers such as AWS, GCP, Azure, K8S…
    - State-based approach to track resource changes throughout deployments

### Files

- `main.tf`
- `variables.tf`
- Optional: `resources.tf`, `output.tf`
- `.tfstate`

### Declarations

- `terraform`: configure basic Terraform settings to provision your infrastructure
    - `required_version`: minimum Terraform version to apply to your configuration
    - `backend`: stores Terraform's "state" snapshots, to map real-world resources to your configuration.
        - `local`: stores state file locally as `terraform.tfstate`
    - `required_providers`: specifies the providers required by the current module
- `provider`:
    - adds a set of resource types and/or data sources that Terraform can manage
    - The Terraform Registry is the main directory of publicly available providers from most major infrastructure platforms.
- `resource`
    - blocks to define components of your infrastructure
    - Project modules/resources: google_storage_bucket, google_bigquery_dataset, google_bigquery_table
- `variable` & `locals`
    - runtime arguments and constants

### Execution steps

1. `terraform init`:
    - Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control
2. `terraform plan`:
    - Matches/previews local changes against a remote state, and proposes an Execution Plan.
3. `terraform apply`:
    - Asks for approval to the proposed plan, and applies changes to cloud
4. `terraform destroy`
    - Removes your stack from the Cloud

### Terraform Workshop to create GCP Infra

Continue [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/terraform): `week_1_basics_n_setup/1_terraform_gcp/terraform`

### References

[https://learn.hashicorp.com/collections/terraform/gcp-get-started](https://learn.hashicorp.com/collections/terraform/gcp-get-started)

### Execution

```bash
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```

```bash
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

```bash
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```


# Setting up the Environment on Google Cloud (Cloud VM + SSH access)

- Generating SSH keys

[https://cloud.google.com/compute/docs/connect/create-ssh-keys](https://cloud.google.com/compute/docs/connect/create-ssh-keys)

`ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048`

- Creating a virtual machine on GCP
- Connecting to the VM with SSH

```bash
ssh -i ~/.ssh/key_name_public username@external_ip_adress
```

- Installing Anaconda

wget [https://www.anaconda.com/download](https://www.anaconda.com/download)

bash Anaconda….sh

- Installing Docker
- Creating SSH `config` file
- Accessing the remote machine with VS Code and SSH remote
- Installing docker-compose
- Installing pgcli
- Port-forwarding with VS code: connecting to pgAdmin and Jupyter from the local computer
- Installing Terraform
- Using `sftp` for putting the credentials to the remote machine
- Shutting down and removing the instance

Create a VM instance in Google Cloud.

Side Menu > Computer Engine > VM Instance. We need to generate an SSH key for the VM instance.

![Untitled](/images/Untitled.png)

You can google > create SSH keys for google cloud.

In the terminal write the following command -

```
cd ~/.ssh
ssh-keygen -t rsa -f ~/.ssh/gcp -C abd -b 2048
```

![Untitled](/images/Untitled%201.png)

Then provide a passphrase. 

This will create two keys -

- A private key (keep it yourself)
- A public key (.pub > you can share it)

![Untitled](/images/Untitled%202.png)

You will put the public key in the google cloud VM instance.

Go to the compute engine. Side menu > Metadata > SSH Keys > Add SSH Key > paste the Public SSH key you just created.

![Untitled](/images/Untitled%203.png)

After pasting in the pub ssh key, save and create the VM Instance.

Side menu > VM Instance > Create Instance.

Fiddle around with like computation power, set the distro to ubuntu, 30gb.

Remember you have 300 Dollars to spend in 3 months so create stuff based on that.

Copy the external IP address

![Untitled](/images/Untitled%204.png)

After copying the external IP ssh, run the command in the terminal - 

```
ssh -i ~/.ssh/gcp abd@external_ip_you_copied
```

If everything has gone by excellentlly, you can run the command - `htop` to see what is going on in your SSHed VM instance.

![Untitled](/images/Untitled%205.png)

You already have google cloud cli installed in it.

Now you can configure this machine -

**Installing Anaconda**

```
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh
```

Then install Anaconda.

Create a config file for SSH

```
Host de-zoomcamp
	Hostname 104.122.49.123
  User abd
  IdentityFile ~/.ssh/gcp
```

Then you can run `ssh de-zoomcamp`

With `ctrl + d` you can logout of the SSH terminal.

Again SSH into the VM instance. Do `sudo apt-get update` Install docker with `sudo apt-get install docker.io`

**Accessing the SSHed VM Instance with VSCode**

- Install the plugin **remote SSH**
- On the bottom left you have the green logo. Click it to “open in remote window”
- Select connect to host
- If you really hate yourself and using WSL then go to users:user and paste in your SSH files into a .ssh directory.
- then you can check the built in terminal if it working.

**Running Docker without Sudo**

[guides/docker-without-sudo.md at main · sindresorhus/guides (github.com)](https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md)

Follow the guide. Logout and login > close connection with ctrl d.

Then check with `docker run hello-world` > `docker run -it ubuntu bash`

**Install Docker Compose**

[https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64](https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64)

```
mkdir bin
cd bin
wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
ls
chmod -x docker-compose
ls
cd
vim .bashrc
```

Ls to check if `docker-compose` is installed. Then declare it as excutable with `chmod`. The second ls will show the docker-compose in green meaning that is now an executable. You can run `./docker-compose version` to make sure everything is running. To make it a path variable add this line at the end of **.bashrc** (`vim .bashrc`)-

```
export PATH="${HOME}/bin:${PATH}"
```

Then run `source .bashrc` to render the change. Then you can run `docker-compose` from anywhere.

**Installing PgCLI**

`conda install -c conda conda-forge pgcli`

`pip install -U mycli`

**Accessing SSH ports from Local machine**

Toggle terminal in your SSHed VS Code. Add the port 5432 -

![Untitled](/images/Untitled%206.png)

Now you can run the command through SSH through VSCode to port from your local host terminal -

![Untitled](/images/Untitled%207.png)

You can also access [localhost](http://localhost) 8080 of your SSHed device.

![Untitled](/images/Untitled%208.png)

Make sure you don’t have any docker containers running with `docker ps`

You can even forward jupyter notebooks! [Localhost](http://Localhost):8888

**Install Terraform**

Download the binary

[https://releases.hashicorp.com/terraform/1.1.4/terraform_1.1.4_linux_amd64.zip](https://releases.hashicorp.com/terraform/1.1.4/terraform_1.1.4_linux_amd64.zip)

```
cd bin
wget https://releases.hashicorp.com/terraform/1.1.4/terraform_1.1.4_linux_amd64.zip
sudo apt-get install unzip 
unzip terraform_1.1.4_linux_amd64.zip
ls
```

It should be green. And you can run `terraform` directly.

**Transferring files and JSON cred using sftp**

Find gcp cred json file

![Untitled](/images/Untitled%209.png)

I found mine in .config>gcloud>dtc-d13423.json

```
sftp de-zoomcamp
mkdir .gc
cd .gc
put dtc-d13423.json
ls
```

sftp is like ssh but for file transfer. `put` transfer the file you have locally to sshed machine.

Login to Google and Terraforming the infra

```
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/dtc-d13423.json
```

```
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

Then terraform time -

```
terraform init
terrform plan
terrform apply
```

But for that you need git clone the terraform repo and cd into it.

Important point in video about setting variables in terrafrom >> [https://youtu.be/ae-CV2KfoN0?t=2637](https://youtu.be/ae-CV2KfoN0?t=2637)

![Untitled](/images/Untitled%2010.png)

YOU NEED TO GIT CLONE THEN RUN TERRFORM.

**Closing the VM**

```
sudo shutdown now
```

Or take your pick here

![Untitled](/images/Untitled%2011.png)

To continue running it you need to start/resume it again.

But you will be given a new ip address. And you will need to reconfigure your ssh config. But your data will persist.


## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 
![Alt text](/images/image.png)

- `--delete`
- `--rc`
- `--rmc`
- `--rm` (**Answer**)


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0 (**Answer**)
- 1.0.0
- 23.0.1
- 58.1.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

```
SELECT count(date(lpep_dropoff_datetime)) as date
FROM public.green_taxi_trips
WHERE date(lpep_pickup_datetime ) = '2019-09-18'
```
![Alt text](image.png)

- 15767(**Answer**)
- 15612
- 15859
- 89009


## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

```
SELECT date(lpep_pickup_datetime) as date,
	SUM(trip_distance)
FROM public.green_taxi_trips
GROUP BY date
ORDER BY SUM(trip_distance) desc
```
![Alt text](image-1.png)

- 2019-09-18
- 2019-09-16
- 2019-09-26 (**Answer**)
- 2019-09-21


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

``` SELECT "Borough", SUM("total_amount")
FROM green_taxi_trips a
LEFT JOIN taxi_zone_lookup
ON a."PULocationID" = taxi_zone_lookup."LocationID"
WHERE date(lpep_pickup_datetime) = '2019-09-18'
GROUP BY taxi_zone_lookup."Borough"
ORDER BY SUM("total_amount") desc
```
![Alt text](image-2.png)

- "Brooklyn" "Manhattan" "Queens" (**Answer**)
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```
SELECT zpu."Zone" as "pickup_location",
	zdo."Zone" as "dropoff_location",
	tip_amount
FROM green_taxi_trips g,
	taxi_zone_lookup as zpu,
	taxi_zone_lookup as zdo
WHERE 
	g."PULocationID"=zpu."LocationID" AND
	g."DOLocationID"=zdo."LocationID" AND
	zpu."Zone"='Astoria'
ORDER BY tip_amount desc
LIMIT 100
```
![Alt text](image-4.png)

- Central Park
- Jamaica
- JFK Airport (**Answer**)
- Long Island City/Queens Plaza


## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

![Alt text](/images/image-1.png)

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET


