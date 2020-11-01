# hw-backend-api

## Framework and dependency
As specified in Pipfile
- python 3
- flask
- pytest
- request

## Quick Start
```
1. Place a raw data file, output.csv, in a folder named 'rawdata'

2. Excute converter
    python converter.py

3. Run web service
    python webapi.py
```

## API Spec and URL
- API 1
   - Desciption: Get lineItem/UnblendedCost grouping by product/productname
   - URL:  http://localhost:5000/api/hw/v1/unblendedcost/{usageaccountid}
   - Parameter (path): usageaccountid
   - Response
      | HTTP Code | Data Type | Content |
      | --------- | --------- | ------- |
      | 200 | object | {<br>"{product/productname_A}":"sum(lineitem/unblendedcost)",<br>"{product/productname_B}": "sum(lineitem/unblendedcost)",  <br> ...<br>} |
      | 400 | string | Invalid ID supplied. ID must be an integer and larger than 0 |
      | 404 | string | The unblended cost of the specified ID was not found |
      
- API 2
   - Desciption: Get daily lineItem/UsageAmount grouping by product/productname
   - URL:  http://localhost:5000/api/hw/v1/usageamount/{usageaccountid}
   - Parameter (path): usageaccountid
   - Response
      | HTTP Code | Data Type | Content |
      | --------- | --------- | ------- |
      | 200 | object | {<br>"{product/productname_A}": {<br>"YYYY/MM/01": "sum(lineItem/UsageAmount)",<br>"YYYY/MM/02": "sum(lineItem/UsageAmount)",<br>...<br>},<br>"{product/productname_B}": {<br>"YYYY/MM/01": "sum(lineItem/UsageAmount)",<br>"YYYY/MM/02": "sum(lineItem/UsageAmount)",<br>...<br>},<br>}|
      | 400 | string | Invalid ID supplied. ID must be an integer and larger than 0 |
      | 404 | string | The usage amount of the specified ID was not found |
    
- The swagger version of API spec is presented in [API issue](https://github.com/MOHOAzure/hw-backend-api/issues/3)

# DB design and schema
- Local SQLite
- Schema
    - PK stands for primary key
    
    | Column | Data Type |
    | -- | -- |
    | PK | INTEGER |
    | bill/PayerAccountId | INTEGER |
    | lineItem/UnblendedCost | REAL  |
    | lineItem/UnblendedRate | REAL  |
    | lineItem/UsageAccountId | INTEGER |
    | lineItem/UsageAmount | REAL  |
    | lineItem/UsageStartDate | TEXT  |
    | lineItem/UsageEndDate | TEXT |
    | product/ProductName | TEXT |
    
- `lineItem/UsageAccountId` is assigned as index since it will always be queried by two APIs.
- Details of DB design is presented in [DB design issue](https://github.com/MOHOAzure/hw-backend-api/issues/4)

## Architecture and component design
![](https://github.com/MOHOAzure/hw-backend-api/blob/master/demo-pic/architecture-and-components.png)
- The design is presented in [this issue](https://github.com/MOHOAzure/hw-backend-api/issues/8)

## API demo
![](https://github.com/MOHOAzure/hw-backend-api/blob/master/demo-pic/API-demo.PNG)

## Performance
- the response time of each API is about 30-70 ms, and most of the time is spent on DB query
- methods to reduce the response time and improve performance
   - assign the `lineItem/UsageAccountId` as DB index as two APIs use it to query
   - query DB only one time in an API
