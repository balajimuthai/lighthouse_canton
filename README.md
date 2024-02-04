# Data Flow: 
1. The data originates from **CoinCap** tool, providing real-time pricing and market activity for **cryptocurrencies stock data**.
2. **Python rest API** is used to fetch data from website using **token key**.
3. Data fetched in **JSON data type** and using Python json transformed into **pandas Dataframe**.
4. Data transformation is done in **Python** to make cleaner data.
5. Data further pushed into **RDS (Postgres - 16.1.1)** locally using **PGadmin**.
6. Postgres has powering **Tableau** for data and dashboard was created in **Tableau**.

# Data dict:
**Data model** has been designed based on stock data output.
Total 3 table are pushed into postgres post transformation.
**Table name**: stock_Assert(Contains information about top 100 stocks in market)
**column** - id,rank,symbol,name,supply,maxsupply,marketcapusd,volumeusd24hr,priceusd,changepercent24hr,vwap24hr,explorer,timestamp.

**Table name**: stock_Assert_history(Contains last one year stock history at average price in day level)
**column** - priceusd, usd_record_time, usd_record_Date, update_timestamp, id 

**Table name**: stock_rate(Contains live stock value)
**column** - id, symbol,currencysymbol, type, rateusd, stock_timestamp, currency, name

# Data Governance Policy:
postgres has been rescricted by specific **role and permission** with rescpect to end customer and authority.

# Data Transformation process:

1. Stock assets are fetched using **Python API**, running at **t-1 level** (batch processing) through a **Lambda function** to obtain daily updated new stocks as **JSON** output. The data is then transformed into a **Pandas DataFrame**. Further, data transformations, including adjustments to **data types and timestamp to datetime conversion**, are implemented to create a cleaner dataset. Custom columns are added, and the processed data is pushed into **Postgres using SQLAlchemy**. The table is updated only when new stocks are added to the stock_assets table. (**Refer** to - api_connector/stock_assets_data.py)

2. Stock assets history is retrieved by passing the **stock ID from the stock assets API** to obtain the entire history at the **YTD level**. This operation is scheduled in a Lambda function using **EventBridge at t-1 level** and is subsequently transformed into Postgres. (**Refer** to - api_connector/stock_asset_history.py)

3. Stock rate is fetched in **real-time** at any given interval **(e.g., 1 minute, 5 minutes)** using a **Lambda function with EventBridge**, or alternatively, **Kafka** can be utilized to stream **near real-time data**. The fetched data undergoes further transformations and is then pushed into **Postgres**.

# Tableau Dashboard:
  **Graph 1: Daily Stock Rate**
  The live stock rate will be refreshed and published in a **bar graph**. Filters such as **stock name, stock value, and stock rank** will be applied, and all filters are **interconnected across all graphs**.
  
**Graph 2: Monthly Performance Trend**

This line graph illustrates the **monthly trend**, showcasing how the stock performed on an average level. Connected filters ensure users can explore specific aspects related to **stock performance**.

**Graph 3: Quarterly Performance Trend**

Similar to Graph 2, this line graph depicts the **quarterly trend** of the stock's performance at a monthly average level. Filters are **interconnected**, providing a **comprehensive view of stock performance over time**.
