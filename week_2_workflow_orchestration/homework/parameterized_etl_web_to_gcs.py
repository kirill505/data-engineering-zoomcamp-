from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas Dataframe"""

    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@flow()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write Dataframe out locally as parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@flow()
def write_gsc(path: Path) -> None:
    """Upload local parquet file to GSC"""
    gsc_block = GcsBucket.load("de-zoomcamp-gsc")
    gsc_block.upload_from_path(
        from_path = f"{path}",
        to_path = path
    )
    return


@task()
def write_bq(df: pd.DataFrame, color: str) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("de-zoomcamp-gcp-cred")


    df.to_gbq(
        destination_table=f"dezoomcamp.{color}_tripdata",
        project_id="dtc-de-406412",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize= 500_000,
        if_exists="append"
    )

@flow()
def etl_web_to_gsc(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)

    write_bq(df_clean, color)

    write_gsc(path)
    

@flow()
def etl_parent_flow(
    months: list[int] = [1, 2], year: int = 2019, color: str = "yellow"
):

    for month in months:
        etl_web_to_gsc(year, month, color)


if __name__ == '__main__':
    color = "yellow"
    months = [4]
    year = 2019
    etl_parent_flow(months, year, color)
