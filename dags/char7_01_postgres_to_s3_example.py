# import airflow
# from airflow import DAG
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.providers.amazon.aws.hooks.s3 import S3Hook

# def execute(self, context):
#     postgres_hook = PostgresHook()
    
#     #curl --include --request GET 'http://apis.data.go.kr/6430000/phyStngTstScrService/getPhyStngTstScr?serviceKey=cHmskJkcmjxQ0gkHaF9rzvRvi8Cytvk7vN7px5yJ0V3aO9PlKylpr9hZ0tj%2Fgs2CeiVx0SmfGhPtjM%2BAnU7v6g%3D%3D&currentPage=1&perPage=10'


import requests

url = 'http://apis.data.go.kr/6430000/phyStngTstScrService/getPhyStngTstScr'
params ={'serviceKey' : 'cHmskJkcmjxQ0gkHaF9rzvRvi8Cytvk7vN7px5yJ0V3aO9PlKylpr9hZ0tj/gs2CeiVx0SmfGhPtjM+AnU7v6g==',
         'currentPage' : '1', 
         'perPage' : '10' }

response = requests.get(url, params=params)
print(response.content)
