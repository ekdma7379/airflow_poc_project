#!/usr/bin/env python

import datetime
import json
import logging
import os
from pathlib import Path
import requests
import click

logging.basicConfig(level=logging.INFO)

@click.command()
@click.option(
    "--start_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.datetime(year=2022,month=12,day=17),
    required=True,
    help="Start date for ratings.",
)
@click.option(
    "--output_path",
    type=click.Path(dir_okay=False),
    default="/tmp/ratings/2022-12-17.json",
    required=True,
    help="Output file path.",
)
@click.option(
    "--host", type=str, default="https://apis.data.go.kr/B551015/API28_1", help="마장동 말 투자배율 API URL."
)
@click.option(
    "--batch_size", type=int, default=100, help="Batch size for retrieving records."
)
def main(start_date, output_path,host, batch_size):
    session = requests.Session()
    
    logging.info("Fetching ratings from %s (start_date : %s)", host,start_date.strftime("%Y-%m-%d"))
    
    ratings = list(
        _get_ratings(
            session=session,
            host=host,
            start_date=start_date,
            batch_size=batch_size,
        )
    )
    
    logging.info("Retrieved %d ratings!", len(ratings))
    output_path = Path(output_path)
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("writing to %s", output_path)
    with output_path.open("w") as file_:
        json.dump(ratings, file_)
    

def _get_ratings(session, host, start_date, batch_size=100):
    
    yield from _get_with_pagination(
        session=session,
        url= host + "/singlePredictionRateInfo_1",
        params={
                'ServiceKey' : 'cHmskJkcmjxQ0gkHaF9rzvRvi8Cytvk7vN7px5yJ0V3aO9PlKylpr9hZ0tj/gs2CeiVx0SmfGhPtjM+AnU7v6g==', 
                'pool' : 'WIN',
                'numOfRows' : batch_size, 
                'rc_date' : start_date.strftime("%Y%m%d"),
                '_type' : 'json',
        },
        batch_size=batch_size
    )

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
        logging.info("url : %s",url)
        response = session.get(
            url,
            params ={**params,
                     **{"pageNo":pageNo, "numOfRows":batch_size},
                     },
            verify=False,
        )
        response.raise_for_status()
        response_json = response.json()
        
        yield from response_json["response"]["body"]["items"]["item"]
        
        offset += response_json["response"]["body"]["numOfRows"]
        total = response_json["response"]["body"]["totalCount"]
        
if __name__ == "__main__":
    main()