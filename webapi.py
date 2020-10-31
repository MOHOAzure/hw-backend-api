from flask import Flask, request, jsonify
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
            404: The cost with the specified ID was not found
    
    Output example of required dictionary
    {
      "AWS Premium Support": "0.0",
      "Amazon Elastic Compute Cloud": "0.0"
    }
    """
    print(api_base+'/unblendedcost/'+usageaccountid)
    
    
    # query db and cacluate costs
    c = CostCalculator.CostCalculator()
    usage_cost = c.get_cost(usageaccountid)
    
    # parse to required dictionary
    response={}    
    for u in enumerate(usage_cost):
        product_name = u[1][0]
        cost = u[1][1]
        response[ product_name ] = cost

    # 
    response = jsonify(response)
    response.status_code = 200
    print(type(response))
    return response
    
# Get daily lineItem/UsageAmount grouping by product/productname
@app.route(api_base+'/usageamount/<usageaccountid>', methods=['GET'])
def get_usage_amount(usageaccountid):
    """
    rtype: dictionary
    
    Output example
    {
      "AWS Premium Support": {
        "YYYY/MM/01": "1.0,",
        "YYYY/MM/02": "1.0,"
      },
      "Amazon Elastic Compute Cloud": {
        "YYYY/MM/01": "1.0,",
        "YYYY/MM/02": "0.0,"
      }
    }
    """
    c = UsageCalculator.UsageCalculator()
    return c.get_usage_amount(usageaccountid)

# run server
if __name__ == "__main__":
    app.run(debug=True)