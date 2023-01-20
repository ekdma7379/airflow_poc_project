import json
import logging
import requests
import airflow
from airflow import DAG
import os
import pandas as pd
import datetime as dt

from airflow.operators.python import PythonOperator


# url = 'http://apis.data.go.kr/6430000/phyStngTstScrService/getPhyStngTstScr'
# params ={'serviceKey' : 'cHmskJkcmjxQ0gkHaF9rzvRvi8Cytvk7vN7px5yJ0V3aO9PlKylpr9hZ0tj/gs2CeiVx0SmfGhPtjM+AnU7v6g==',
#          'currentPage' : '1', 
#          'perPage' : '10' }

# response = requests.get(url, params=params)
# print(response.content)

ODDS_HOST = os.environ.get("ODDS_HOST","apis.data.go.kr/B551015/API28_1")
ODDS_SCHEMA = os.environ.get("ODDS_HOST","https")

dag=DAG(
    dag_id="01_python",
    description="Fetches ratings from the Movielens API using the Python Operator.",
    start_date=dt.datetime(2022, 12, 17),
    end_date=dt.datetime(2022, 12, 17),
    schedule_interval="@daily",
)
    
def _get_session():
    session = requests.Session()
    schema = ODDS_SCHEMA
    host = ODDS_HOST
    
    base_url = f"{schema}://{host}"
    
    return session, base_url

def _get_with_pagination(session : requests.Session, url, params, batch_size=100):
    """_summary_

    Args:
        session (_type_): _description_
        url (_type_): _description_
        params (_type_): _description_
        batch_size (int, optional): _description_. Defaults to 100.
    """
    pageNo = 0
    offset = 0
    total = None
    while total is None or offset < total:
        pageNo += 1
        response = session.get(
            url,
            params ={**params,
                     **{"pageNo":pageNo, "numOfRows":batch_size},
                     },
            verify=False,
        )
        response.raise_for_status()
        response_json = response.json()
        
        yield from response_json["response"]["body"]
        
        offset += response_json["response"]["body"]["numOfRows"]
        total = response_json["response"]["body"]["totalCount"]
        
def _get_ratings(start_date, batch_size=100):
    session, base_url = _get_session()
    
    yield from _get_with_pagination(
        session=session,
        url=base_url + "/singlePredictionRateInfo_1",
        params={
                'ServiceKey' : 'cHmskJkcmjxQ0gkHaF9rzvRvi8Cytvk7vN7px5yJ0V3aO9PlKylpr9hZ0tj/gs2CeiVx0SmfGhPtjM+AnU7v6g==', 
                'pool' : 'WIN',
                'numOfRows' : batch_size, 
                'rc_date' : start_date,
                '_type' : 'json',
        },
        batch_size=batch_size
    )

def _fetch_ratings(templates_dict : dict, batch_size=1000, **_):
    logger = logging.getLogger(__name__)
    
    start_date = templates_dict["start_date"]
    output_path = templates_dict["output_path"]
    
    logger.info(f"Fetching ratings date : {start_date}")
    ratings = list(
        _get_ratings(
            start_date=start_date,
            batch_size=batch_size,
        )
    )
    
    logger.info(f"Fetched {len(ratings)} ratings")
    
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir,exist_ok=True)
    
    with open(output_path, "w") as file_:
        json.dump(ratings,fp=file_)

fetch_ratings = PythonOperator(
    task_id="fetch_ratings",
    python_callable=_fetch_ratings,
    templates_dict={
        "start_date":"{{ds_nodash}}",
        "output_path":"/tmp/airflow_example/ratings/{{ds_nodash}}.json",
    },
    dag=dag
)

def _rank_odds(templates_dict : dict, **_):
    from custom.ranking import rank_odds_by_rating 
    
    input_path = templates_dict["input_path"]
    output_path = templates_dict["output_path"]
    
    ratings = pd.read_json(input_path)
    ranking = rank_odds_by_rating(ratings=ratings)
    
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    ranking.to_csv(output_path, index=True)
    
rank_odds = PythonOperator(
    task_id="rank_odds",
    python_callable=_rank_odds,
    templates_dict={
        "input_path":"/tmp/airflow_example/ratings/{{ds_nodash}}.json",
        "output_path":"/tmp/airflow_example/ratings/{{ds_nodash}}.csv",
    },
    dag=dag,
)    

fetch_ratings >> rank_odds

if __name__ == "__main__":
    # from airflow.utils.state import State
    # KST = dt.timezone(dt.timedelta(hours=9))
    # start_date=dt.datetime(year=2022, month=12, day=17, hour=21, minute=0, second=0, tzinfo=KST)
    # end_date=dt.datetime(year=2022, month=12, day=17, hour=0, minute=0, second=0, tzinfo=KST)
    dag.test()