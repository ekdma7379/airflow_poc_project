#!/usr/bin/env python
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup as bs
from pytz import timezone
import requests
import json
import logging
from pathlib import Path
from threading import Event
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from pymongo import MongoClient
from goose3 import Goose
from goose3.text import StopWordsKorean
import socket
import click
import time
import traceback

def scrap_news_content(  media : str = "조선일보"
                       , std_date : datetime = datetime.now()
                       , anchorlists : List = []) -> List:  
### virtual display
    display = Display(visible=0, size=(1920, 1080)) 
    display.start() 
    ### chrome driver
    path='/app/docker/images/news_scrap/scripts/chromedriver' # 구글 드라이버 설치 경로 지정
    driver = webdriver.Chrome(path)
    ### goose3
    g = Goose({'stopwords_class':StopWordsKorean})
    
    #output_path_contents = f"{output_path_anchors}/{media}_{std_date_nodash}_contents.txt"
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
    anchorlists = [[134,"https://n.news.naver.com/article/077/0005822143?sid=104"]
                  ,[135,"https://n.news.naver.com/article/001/0013677921?sid=106"]
                  ,[136,"https://n.news.naver.com/article/077/0005822149?sid=104"]]
    for idx, anchor in anchorlists:
        try:
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
        except Exception as e:
            with output_path.open("a") as file_:
                file_.write(f'ERROR|{idx}|{anchor}{traceback.format_exc()}\n')
            continue
    # goose3 close
    g.close()
    return contentlists
    
if __name__ == "__main__":
    # scrap_news_content()
    client = MongoClient('mongodb://root:1234@172.25.2.202:27017/')
    db = client["news_data"]
    # 뉴스 입력
    mngo_raw_news_press = db["raw_news_press"]
    mngo_raw_news_press.delete_many({"std_date":"2023-01-03", "media" : "연합뉴스"})