import pytest, requests, json

api_base = 'http://127.0.0.1:5000/api/hw/v1' # The root url of the web api

def test_unblended_cost_with_legal_id():
    usageaccountid = "147878817734"
    r = requests.get(api_base+'/unblendedcost/'+usageaccountid)
    data = r.json()
    assert r.status_code == 200
    assert len(data) == 5 # there should be five kinds products
    
def test_unblended_cost_with_illegal_id():
    usageaccountid = "-1"
    r = requests.get(api_base+'/unblendedcost/'+usageaccountid)
    assert r.status_code == 400
    
def test_unblended_cost_with_non_existing_legal_id():
    usageaccountid = "1"
    r = requests.get(api_base+'/unblendedcost/'+usageaccountid)
    assert r.status_code == 404
    
    
def test_usage_amount_with_legal_id():
    usageaccountid = "147878817734"
    r = requests.get(api_base+'/usageamount/'+usageaccountid)
    data = r.json()
    assert r.status_code == 200
    assert len(data) == 5 # there should be five kinds products
    
def test_usage_amount_with_illegal_id():
    usageaccountid = "-1"
    r = requests.get(api_base+'/usageamount/'+usageaccountid)
    assert r.status_code == 400
    
def test_usage_amount_with_non_existing_legal_id():
    usageaccountid = "1"
    r = requests.get(api_base+'/usageamount/'+usageaccountid)
    assert r.status_code == 404
    
    