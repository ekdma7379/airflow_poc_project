import datetime as dt

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="01_docker",
    start_date=dt.datetime(2022,12,17),
    schedule="@daily",
    catchup=False,
) as dag:
    docker_fetch_ratings=DockerOperator(
        task_id="docker_fetch_ratings",
        image="ekdma7379/movielens-fetch",
        command=[
            "fetch-ratings",
            "--start_date",
            "{{ds}}",
            "--output_path",
            "/tmp/ratings/{{ds}}.json",
            "--host",
            "https://apis.data.go.kr/B551015/API28_1",
        ],
        mounts=["/tmp/airflow/data:/tmp",],
        network_mode="airflow",
    )
    
    docker_fetch_ratings
