from flask import Flask
import sqlite3, configparser

# import API handlers
from api import CostCalculator, UsageCalculator

# init app
app = Flask(__name__)
api_base = '/api/hw/v1'

# Get lineItem/UnblendedCost grouping by product/productname
@app.route(api_base+'/unblendedcost/<usageaccountid>', methods=['GET'])
def get_cost(usageaccountid):
    """
    rtype: flask.wrappers.Response
            200: required dictionary
            400: Invalid ID supplied. ID must be an integer and larger than 0
            404: The unblended cost of the specified ID was not found
    
    Output example of required dictionary
    {
      "AWS Premium Support": 0.0,
      "Amazon Elastic Compute Cloud": 0.0
    }
    """
    
    # query db and cacluate costs
    c = CostCalculator.CostCalculator()
    response = c.get_cost(usageaccountid)
    
    return response
    
# Get daily lineItem/UsageAmount grouping by product/productname
@app.route(api_base+'/usageamount/<usageaccountid>', methods=['GET'])
def get_usage_amount(usageaccountid):
    """
    rtype: flask.wrappers.Response
            200: required dictionary
            400: Invalid ID supplied. ID must be an integer and larger than 0
            404: The usage amount of the specified ID was not found
    
    Output example
    {
      "AWS Premium Support": {
        "YYYY/MM/01": "1.0",
        "YYYY/MM/02": "1.0"
      },
      "Amazon Elastic Compute Cloud": {
        "YYYY/MM/01": "1.0",
        "YYYY/MM/02": "0.0"
      }
    }
    """
    # query db and cacluate costs
    c = UsageCalculator.UsageCalculator()
    response = c.get_usage_amount(usageaccountid)    
    return response

# run server
if __name__ == "__main__":
    app.run(debug=True)