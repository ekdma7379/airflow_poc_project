from selenium import webdriver 
from pyvirtualdisplay import Display 

display = Display(visible=0, size=(1920, 1080)) 
display.start() 

path='/app/docker/images/news_scrap/scripts/chromedriver' # 구글 드라이버 설치 경로 지정
driver = webdriver.Chrome(path)

driver.get("https://www.naver.com") # naver 열기
print(driver.current_url) # 현재 url 출력