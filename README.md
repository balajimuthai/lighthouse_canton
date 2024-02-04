#Data Flow:
1. The data originates from **CoinCap** tool, providing real-time pricing and market activity for **cryptocurrencies stock data**.
2. **Python rest API** is used to fetch data from website using **token key**.
3. Data fetched in **JSON data type** and using Python json transformed into **pandas Dataframe**.
4. Data transformation is done in **Python** to make cleaner data.
5. Data further pushed into **RDS (Postgres - 16.1.1)** locally using **PGadmin**.
6. Postgres has powering **Tableau** for data and dashboard was created in **Tableau**.

**Data dict:**
**Data model** has been designed based on stock data output.
Total 3 table are pushed into postgres post transformation.
Table name: stock_Assert(Contains information about top 100 stocks in market)
column - id,rank,symbol,name,supply,maxsupply,marketcapusd,volumeusd24hr,priceusd,changepercent24hr,vwap24hr,explorer,timestamp.

Table name: stock_Assert_history(Contains last one year stock history at average price in day level)
column - priceusd, usd_record_time, usd_record_Date, update_timestamp, id 

Table name: stock_rate(Contains live stock value)
column - id, symbol,currencysymbol, type, rateusd, stock_timestamp, currency, name

Data Governance Policy:
postgres has been rescricted by specific role and permission with rescpect to end customer and authority.

Data Transformation process:
1. stock asserts are fetched using python API and this will run at t-1 level (batch processing) using lambda function to get daily updated new stocks as json output and
   futher it has been transformed into pandas dataframe and data transformation are done to make it more cleaner data(Data type, timestamp to datetime) and added custom
   column as well and data has been pushed into postgres using sqlalchemy and table will get updated only when new stock are
   added in stock_assets table.(refer - api_connector/stock_assets_data.py)
2. stock asserts history are fetched by passing stock id from stock asserts api to get all stock id history at ytd level(can be pulled at mtd,hourly,weekly as well) and this
   will be scheduled in lambda using eventbridge at t-1 level and transformed into postgres. (refer - api_connector/stock_asset_history.py)
3. stock rate will be fetched at real-time data at any time interval(1 min , 5mins) using lambda with eventbridge or we can use kafka to steam near real time data and futher
   transformation are done and pushed into postgres.

Tableau Dashboard:
  Graph 1. Stock daily rate - live stock rate will be refershed and publised in bar graph with filterss(stock_name, stock_value,stock_rank) and all filters are conneted
  across all graph
  Graph 2 . Month trend on how stock performed at month level average in line graph with connected filters.
  Graph 2 . Quaterly trend on how stock performed at month level average in line graph with connected filters.
