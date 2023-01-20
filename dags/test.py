import os
import requests

ODDS_HOST = os.environ.get("ODDS_HOST","apis.data.go.kr/B551015/API28_1")
ODDS_SCHEMA = os.environ.get("ODDS_HOST","https")
    
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
        
        # yield from response_json["response"]["body"]
        
        offset += response_json["response"]["body"]["numOfRows"]
        total = response_json["response"]["body"]["totalCount"]
        
def _get_ratings(start_date, batch_size=100):
    session, base_url = _get_session()
    
    _get_with_pagination(
        session=session,
        url=base_url + "/singlePredictionRateInfo_1",
        params={
                'ServiceKey' : 'cHmskJkcmjxQ0gkHaF9rzvRvi8Cytvk7vN7px5yJ0V3aO9PlKylpr9hZ0tj/gs2CeiVx0SmfGhPtjM+AnU7v6g==', 
                'pool' : 'WIN',
                'numOfRows' : batch_size, 
                'rc_date' : start_date,
                '_type' : 'json',
        },
        batch_size=batch_size,
    )

if __name__ == '__main__':
    _get_ratings(start_date="20221217")
    print("hello")