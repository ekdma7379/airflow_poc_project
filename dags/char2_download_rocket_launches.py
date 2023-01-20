import json
import pathlib

import airflow
import requests
import requests.exceptions as requests_exceptions

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
# from airflow.utils.dates import days_ago

# dag 인스턴스 생싱
dag=DAG(
    # Airflow webUI에 표시되는 Dag 이름
    dag_id = "download_rocket_launches",
    # workflow가 처음 실행되는 날짜/시간
    start_date=airflow.utils.dates.days_ago(14),
    # 반복설정 -> 추후 Dag 관련 옵션을 더 살펴볼 예정
    schedule_interval=None,
)

# 발사되는 로켓 리스트 API를 통해 Image URL list를 조회를 위한 BashOperator
download_launches = BashOperator(
    # task ID
    task_id="download_launches",
    # API 호출 명령어
    bash_command='curl -o /tmp/launches.json -L "https://ll.thespacedevs.com/2.0.0/launch/upcoming"',
    # 이건 뭔지 아직 모르겠다.
    dag=dag,
)

def _get_pictures():
    # 경로가 존재하는지 확인
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    #launches.json 파일 열기
    with open("/tmp/launches.json") as f:
        # 다운로드 받은 Json 읽기
        launches=json.load(f)
        # Json 구조의 image url 찾기
        image_urls=[launch["image"] for launch in launches["results"]]
        # URL 이미지를 하나씩 작업
        for image_url in image_urls:
            try:
                # url 다운로드
                response=requests.get(image_url)
                # 경로의 마지막 단어를 통해 file name 추출
                image_filename = image_url.split("/")[-1]
                # 이미지 다운로드할 경로 설정
                target_file=f"/tmp/images/{image_filename}"
                # 해당 경로에 사진 생성
                with open(target_file, "wb") as f:
                    f.write(response.content)
                # 파일 다운로드 되었는지 출력
                print(f"Download {image_url} to {target_file}")
            # Json에 해당 키값이 없을때 
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            # 해당 API가 response가 없을때
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")

# python 실행 Operater 구현
get_pictures=PythonOperator(
    task_id="get_pictures",
    python_callable=_get_pictures,
    dag=dag,
)

# 이미지 개수 출력 BashOperator
notify=BashOperator(
    task_id="notify",
    bash_command='echo "there are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag,
)

# task 실행 순서 정의
download_launches >> get_pictures >> notify