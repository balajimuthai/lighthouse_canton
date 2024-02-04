import json
import lambda_stock_asset_rate
def lambda_handler(event,context):
  return lambda_stock_asset_rate.main()
