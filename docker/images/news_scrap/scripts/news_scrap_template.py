#!/usr/bin/env python
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup as bs
from pytz import timezone
import requests
import logging
from pathlib import Path
from threading import Event
from selenium import webdriver 
from pyvirtualdisplay import Display
from pymongo import MongoClient
from goose3 import Goose
from goose3.text import StopWordsKorean
import socket
import click
import traceback
import os



def scrap_news_anchorlist(media
                        , std_date : datetime 
                        , start_idx : int
                        , isdebug : int = 0
                        , output_path : str = "/app/downloads/news"):
    ### INPUT PARAMETER
    # media = "전자신문"
    # std_date = datetime(2023,1,2)
    ### INPUT END
    
    session = requests.Session()
    page = 0
    idx = start_idx
    std_date_nodash = std_date.strftime("%Y%m%d")
    std_date_pot = std_date.strftime("%Y.%m.%d")
    output_path = f"{output_path}/{media}_{std_date_nodash}_anchors.txt"
    
    if isdebug:
        ### OUTPUT PATH
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        ### OUPUT INIT
        with output_path.open("w") as file_:
            file_.write('')
        ### OUTPUT INIT END    
    
    anchorlists : List[str] = []
    
    while True:
        base_url = f"https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query={media}&sort=2&photo=0&field=0&pd=3&ds={std_date_pot}&de={std_date_pot}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from{std_date_nodash}to{std_date_nodash}&is_sug_officeid=1&start={idx}"
        response = session.get(
            base_url,
            verify=False,
        )
        response.raise_for_status()
        soup = bs(response.text, "lxml")
        items = soup.select("a.news_tit")
        if len(items) == 0:
            break
        else:
            for item in items:
                idx += 1
                anchorlists.append([idx,item["href"]])
                if isdebug:
                    with output_path.open("a") as file_:
                        file_.write(f'{idx}|{item["href"]}\n',)
                    
        logging.info("%d article is writing"% idx)
        # 1초 기다림
        Event().wait(1)

    # print("total article = %d"%idx)
    
    return idx, anchorlists

def scrap_news_content(  media : str
                       , std_date : datetime
                       , anchorlists : List
                       , isdebug : int = 0) -> List:
    ### virtual display
    display = Display(visible=0, size=(1920, 1080)) 
    display.start() 
    ### chrome driver
    # path='/app/docker/images/news_scrap/scripts/chromedriver' # 구글 드라이버 설치 경로 지정
    #driver = webdriver.Chrome(path)
    chrome_options = webdriver.ChromeOptions()

    # linux 환경에서 필요한 option
    chrome_options.add_argument(("lang=ko_KR"))
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=chrome_options)
    ### goose3
    g = Goose({'stopwords_class':StopWordsKorean})
    
    #output_path_contents = f"{output_path_anchors}/{media}_{std_date_nodash}_contents.txt"
    if isdebug:
        ### test
        std_date_nodash = std_date.strftime("%Y%m%d")
        output_path = f"/app/downloads/news/{media}_{std_date_nodash}_complete.txt"
        output_path = Path(output_path)
        with output_path.open("w") as file_:
            file_.write('')
        ### test end
    
    contentlists = []
    ins_id = socket.gethostname()
    ins_ip = socket.gethostbyname(ins_id)
    ins_dtm = datetime.now(timezone('Asia/Seoul'))
    std_date_ds = std_date.strftime("%Y-%m-%d")
    for idx, anchor in anchorlists:
        try:
            if isdebug:
                with output_path.open("a") as file_:
                    file_.write(f'{idx}|{anchor}\n',)
            driver.get(anchor)
            driver.implicitly_wait(time_to_wait=1000)
            soup = bs(driver.page_source, "lxml")
            title = soup.select_one("h2#title_area span").text

            if soup.find('a',{"class":"media_end_head_origin_link"}):
                content_url = soup.select_one("a.media_end_head_origin_link")["href"]
            else:
                content_url = None
            naver_url = anchor
            content_clean = g.extract(raw_html = driver.page_source)
            content = soup.select_one("div._article_content").text
            data = {
              "std_date" : std_date_ds,
              "idx" : idx,
              "media":media,
              "title": title,
              "title_clean": content_clean.title,
              "content_url": content_url,
              "naver_url": naver_url,
              "content": content,
              "content_clean":content_clean.cleaned_text,
              # "clear": False,
              "ins_id": ins_id,
              "ins_ip": ins_ip,
              "ins_dtm": ins_dtm,
              "upd_dtm": ins_dtm,
            }

            contentlists.append(data)
            # print(anchor)
        except Exception as e:
            if isdebug:
                # TODO : aws S3 로 로깅하도록 변경해야 한다.
                with output_path.open("a") as file_:
                    file_.write(f'ERROR|{idx}|{anchor}{traceback.format_exc()}\n')
            continue
    # drivers close
    g.close()
    driver.quit()
    display.stop()
    return contentlists

def scrap_news_insertcontent(  media : str
                             , std_date : datetime
                             , contentlists : List):
    client = MongoClient(mongoURL)
    db = client["news_data"]
    # 뉴스 입력
    mngo_raw_news_press = db["raw_news_press"]
    mngo_raw_news_press.delete_many({"std_date":std_date.strftime("%Y-%m-%d"), "media" : media})
    mngo_raw_news_press.insert_many(contentlists)

def scrap_news_insertidx(  media : str
                             , std_date : datetime
                             , end_idx : int):
    client = MongoClient(mongoURL)
    db = client["news_data"]
    # 뉴스 index  입력
    mngo_raw_news_press = db["raw_news_press_idx"]
    mngo_raw_news_press.insert_one({
        "std_date":std_date.strftime("%Y-%m-%d"),
        "media" : media,
        "end_idx" : end_idx,
        "ins_dtm": datetime.now(timezone('Asia/Seoul')),
    })    

def scrap_news_selectidx( media : str
                        , std_date : datetime):
    client = MongoClient(mongoURL)
    db = client["news_data"]
    # 뉴스 index  입력
    mngo_raw_news_press = db["raw_news_press_idx"]
    fixed_idx = mngo_raw_news_press.find_one({
        "std_date":std_date.strftime("%Y-%m-%d"),
        "media" : media,
    }, sort=[('ins_dtm', -1)])
    
    return 0 if fixed_idx == None else int(fixed_idx["end_idx"])

@click.command()
@click.option(
    "--media",
    type= click.STRING,
    default="서울경제",
    required=True,
    help="조회 언론사 ex) 조선일보, 연합뉴스 한국경제 서울경제 등등",
)
@click.option(
    "--std_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.now,
    required=True,
    help="Start date for ratings.",
)
@click.option(
    "--start_idx",
    type=click.INT,
    default=0,
    help="Start date for ratings.",
)
@click.option(
    "--isdebug",
    type=click.INT,
    default=0,
    help="Start date for ratings.",
)
def main( media
        , std_date
        , start_idx
        , isdebug):
    ## start_idx가 양수이면 입력된 start_idx로,
    if start_idx > 0:
        fixed_idx = start_idx
    ### 아니면 DB에서 그전에 작업된 idx로 작업 시작
    else:
        fixed_idx = scrap_news_selectidx(media = media, std_date = std_date)
    end_idx, anchorlists = scrap_news_anchorlist(media = media, std_date = std_date,start_idx = fixed_idx, isdebug = isdebug)
    contentlists = scrap_news_content(media, std_date = std_date, anchorlists=anchorlists, isdebug = isdebug)
    scrap_news_insertcontent(media, std_date = std_date,contentlists=contentlists)
    scrap_news_insertidx(media, std_date = std_date, end_idx=end_idx)
if __name__ == "__main__":
    main()
    