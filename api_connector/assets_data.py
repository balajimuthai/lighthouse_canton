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

assets_df['supply'] = assets_df['supply'].astype('double')
assets_df['maxsupply'] = assets_df['maxSupply'].astype('double')
assets_df['marketcapusd'] = assets_df['marketCapUsd'].astype('double')
assets_df['volumeusd24hr'] = assets_df['volumeUsd24Hr'].astype('double')
assets_df['priceusd'] = assets_df['priceUsd'].astype('double')
assets_df['changepercent24hr'] = assets_df['changePercent24Hr'].astype('double')
assets_df['vwap24hr'] = assets_df['vwap24Hr'].astype('double')
assets_df.replace(to_replace=[None], value=np.nan, inplace=True)
assets_df = assets_df.fillna(value=np.nan)


db = create_engine("postgresql://postgres:%s@localhost:5432/postgres"%quote_plus("April123"))

conn=db.connect()
assets_df.to_sql('data',con=conn,if_exists='replace',index=False)
conn.autocommit=True
sql=text('''
truncate table stock_assets
''')
conn.execute(sql)
conn.commit()
sql=text('''
insert into stock_assets
select 
id, cast(rank as int) as rank, symbol, name, supply,
maxsupply, marketcapusd,
volumeusd24hr,
priceusd, changepercent24hr, vwap24hr, explorer, timestamp
from data 
''')
conn.execute(sql)
conn.commit()
conn.close()
