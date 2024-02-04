import json
import stock_asset_rate
def lambda_handler(event,context):
  return stock_asset_rate.main()
