import requests
import json
import datetime
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np


payload = {}
headers = {
  'Authorization': 'Bearer f73e3b35-57b8-47b5-ad43-d1dc1c85ff97'
}
def assets():
  url = "http://api.coincap.io/v2/assets"
  response = requests.request("GET", url, headers=headers, data=payload)
  res1 = response.text
  dict2 = json.loads(res1)['data']
  assets_df = pd.DataFrame(dict2)
  assets_df['timestamp'] = datetime.datetime.now()
  return assets_df
assets_df=assets()

def assets_his(id):
  url = f"http://api.coincap.io/v2/assets/{id}/history?interval=d1"
  response = requests.request("GET", url, headers=headers, data=payload)
  res1 = response.text
  dict2 = json.loads(res1)['data']
  assets_his = pd.DataFrame(dict2)
  assets_his['timestamp'] = datetime.datetime.now()
  assets_his['id']=id
  return assets_his

uniq_id=assets_df[['id']].drop_duplicates()
uniq_asset=[]
for i in uniq_id.itertuples():
  uniq_asset.append(i[1])
df=pd.DataFrame()
for i in uniq_asset:
  assets_his_df=assets_his(i)
  df=pd.concat([assets_his_df,df])


stock_assert_history=df
stock_assert_history['priceusd'] = stock_assert_history['priceUsd'].astype('double')
# stock_assert_history['date'] = stock_assert_history['date'].astype('datetime')
stock_assert_history['time'] = pd.to_datetime(stock_assert_history['time'],unit='ms')
stock_assert_history.replace(to_replace=[None], value=np.nan, inplace=True)
stock_assert_history = stock_assert_history.fillna(value=np.nan)
print(stock_assert_history.info())

db = create_engine("postgresql://postgres:%s@localhost:5432/postgres"%quote_plus("April123"))

conn=db.connect()
stock_assert_history.to_sql('data',con=conn,if_exists='replace',index=False)
conn.autocommit=True
sql=text('''
insert into stock_assert_history
select 
priceusd,
         cast(time as date),
         cast(date as date),
         cast(timestamp as timestamp),
         id
from data 
''')
conn.execute(sql)
conn.commit()
conn.close()
