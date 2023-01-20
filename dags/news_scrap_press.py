import datetime as dt

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="news_scrap_3h",
    start_date=dt.datetime(2023,1,4),
    schedule="5 */3 * * *",
    catchup=False,
) as dag:
    # tasks = {}
    # medias = ["서울경제","한국경제","조선일보","연합뉴스"]
    # for media in medias:
    #     docker_fetch_ratings=DockerOperator(
    #         # task_id=f"news_scrap_3h_{media}",
    #         task_id=f"news_scrap_3h_00",
    #         image="ekdma7379/news_scrapper:0.0.1",
    #         command=[
    #             "news_scrap_template",
    #             "--std_date",
    #             "{{ds}}",
    #             # "--media",
    #             # media,
    #         ],
    #         mounts=["/tmp/airflow/data:/tmp",],
    #         network_mode="airflow",
    #     )
    #     tasks[media] = docker_fetch_ratings
    # tasks["서울경제"] >> tasks["한국경제"] >> tasks["조선일보"] >> tasks["연합뉴스"] 
    
    docker_fetch_ratings=DockerOperator(
            task_id=f"news_scrap_3h_00",
            image="ekdma7379/news_scrapper:0.0.1",
            command=[
                "news_scrap_template",
                "--std_date",
                "{{ds}}",
                # "--media",
                # media,
            ],
            api_version='auto',
            auto_remove=True,
            docker_url="unix://var/run/docker.sock",
            network_mode="bridge",
        )
    docker_fetch_ratings
