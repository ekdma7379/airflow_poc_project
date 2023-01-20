import airflow
import datetime as dt
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag=DAG(
    dag_id="extract_gz",
    start_date=dt.datetime(2022,12,21),
    schedule_interval=None,
)

extract_gz=BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /tmp/wikipageviews.gz",
    dag=dag,
)

def _fetch_pageviews(pagenames):
    result=dict.fromkeys(pagenames,0)
    with open(f"/tmp/wikipageviews","r") as f:
        for line in f:
            domain_code, page_title, view_counts, _=line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title]=view_counts
    
    print(result)

fetch_pageviews=PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={
        "pagenames":{
            "Google",
            "Amazon",
            "Apple",
            "Microsoft",
            "Meta",
        }
    },
    dag=dag,
)

extract_gz >> fetch_pageviews