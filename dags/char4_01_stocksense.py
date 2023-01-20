from urllib import request
import datetime as dt

import airflow 
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

# stocksense : 사람들이 많이 찾은 기업이 관심이 많아 주가가 오를것이라고 예상함
dag=DAG(
    dag_id="stocksense",
    # 하루 전 기준으로 실행
    start_date=airflow.utils.dates.days_ago(1) ,
    # 한시간마다 한번씩 실행
    schedule_interval="@daily",
    # postgresql 쿼리가 존재하는 위치 참조
    template_searchpath="/tmp",
)

# 위키피디아 pageview 다운로드
# 파일명의 규칙을 input parameter로 받고 있다.
def _get_data(year, month, day, hour, output_path, **_):
    url=(
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/"
        f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    print(url)
    request.urlretrieve(url,output_path)

# _get_data 함수 호출하는 PythonOperator
# data_interval_start 와 같은 Jinja Templating을 참고해야 한다.
# Jinja Templating doc url : https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
get_data=PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        # data_interval_start : pendulum.DateTime type의 실행 기준일자 범위 중 제일 빠른 일자
        # 해당 내용은 블로그에서 다루겠음
        "year":"{{data_interval_start.year}}",
        "month":"{{data_interval_start.month}}",
        "day":"{{data_interval_start.day}}",
        "hour":"{{data_interval_start.hour}}",
        "output_path":"/tmp/wikipageviews.gz",
    },
    dag=dag,
)

# 압축파일 압축해제하는 BashOperator
extract_gz=BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /tmp/wikipageviews.gz",
    dag=dag,
)


def _fetch_pageviews(pagenames,data_interval_start, **_):
    result=dict.fromkeys(pagenames,0)
    # wikipageviews 파일 열기
    with open(f"/tmp/wikipageviews","r") as f:
        # 한 라인라인마다 " "으로 나눠준 후 영어권 도메인 조회 결과를 결과 dictionary에 저장
        for line in f:
            domain_code, page_title, view_counts, _=line.split(" ")
            if domain_code == "en" and page_title in pagenames:
                result[page_title]=view_counts
    # 쿼리를 파일에 작성 - 원자성 떄문
    with open("/tmp/postgres_query.sql","w") as f:
        for pagename, pageviewcount in result.items():
            f.write(
                "INSERT INTO pageview_counts VALUES("
                f"'{pagename}','{pageviewcount}','{data_interval_start}'"
                ");\n"
            )
    # 쿼리 잘 작성되었는지 로그에서 확인
    with open("/tmp/postgres_query.sql","r") as f:
        for line in f:
            print(line)

# 구글,아마존 등 목적 회사를 parameter로 넘겨서 실행시키는 PythonOperator
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

# 작성된 쿼리를 실행시킴
write_to_postgres=PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="my_postgres",
    sql="postgres_query.sql",
    dag=dag,
)

get_data >> extract_gz >> fetch_pageviews >> write_to_postgres