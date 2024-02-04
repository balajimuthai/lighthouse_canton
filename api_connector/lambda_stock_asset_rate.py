import requests
import json
import datetime
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2


def rates(token):
  payload = {}
  headers = {
  'Authorization': f'Bearer {token}'
  }
  url = "http://api.coincap.io/v2/rates"
  response = requests.request("GET", url, headers=headers, data=payload)
  res = response.text
  dict1 = json.loads(res)['data']
  rate_df = pd.DataFrame(dict1)
  rate_df['timestamp'] = datetime.datetime.now()
  return rate_df

def rate_transform(rate_df):
  rate_df1=rate_df
  rate_df1['currency']=rate_df1['id'].str.split('-').str[-1]
  rate_df1['name']=rate_df1['id'].apply(lambda x: "-".join(x.split('-')[:-1]))
  rate_df1['rateUsd'] = rate_df1['rateUsd'].astype('double')
  return rate_df1

def postgres_conn(rate_df1):
  db = create_engine("postgresql://postgres:%s@localhost:5432/postgres"%quote_plus("April123"))
  
  conn=db.connect()
  rate_df1.to_sql('data',con=conn,if_exists='replace',index=False)
  conn.autocommit=True
  sql=text('''
  truncate table stock_rate
  ''')
  conn.execute(sql)
  sql=text('''
  insert into stock_rate
  select * from data 
  ''')
  conn.execute(sql)
  conn.close()
def main():
  config=get_secret('secret_name')
  token=config['token_key']
  rate_df=rates(token)
  print('stock_rate generated')
  rate_df1=rate_transform(rate_df)
  print('stock data transformed')
  postgres_conn(rate_df1)
  print('data pushed into postgres db')
