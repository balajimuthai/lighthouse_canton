import requests
import json
import datetime
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2


payload = {}
headers = {
  'Authorization': 'Bearer f73e3b35-57b8-47b5-ad43-d1dc1c85ff97'
}
def rates():
  url = "http://api.coincap.io/v2/rates"
  response = requests.request("GET", url, headers=headers, data=payload)
  res = response.text
  dict1 = json.loads(res)['data']
  rate_df = pd.DataFrame(dict1)
  rate_df['timestamp'] = datetime.datetime.now()
  return rate_df
rate_df=rates()

rate_df1=rate_df
rate_df1['currency']=rate_df1['id'].str.split('-').str[-1]
rate_df1['name']=rate_df1['id'].apply(lambda x: "-".join(x.split('-')[:-1]))
rate_df1['rateUsd'] = rate_df1['rateUsd'].astype('double')
print(rate_df1.info())

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
