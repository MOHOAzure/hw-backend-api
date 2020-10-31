import sqlite3, configparser
from flask import jsonify, abort

class UsageCalculator():
    def check_id_illegal(self, id):
        """
        type: str
        rtype: bool
                True: str is not like int
                False: str is like int
        """
        try: 
            id = int(id)
            if id>0:
                return False
            return True
        except ValueError:
            return True
        
    def get_usage_amount(self, usageaccountid):
        """
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
        
        Assumption:
            If usage is less than one day, then it is counted as one day.
            
        Purpose of SQL:
            Given usage account Id, find out the usage amount of a product in a period of days

        Field returned by SQL:
            product/ProductName
            UsageAmount of a period
            date(startdate)
            days: the number of days between "lineItem/UsageStartDate" and "lineItem/UsageEndDate" (exclusive)
            
        Left for python program:        
            Date structure:
                a "reponse" dict for API reponse
                    a "product usage" dict for daily usage statistic of a product
                        a "daily usage" dict for usage amount per day
            
            Logic:
                If the period of days>1, then 
                    avg_amount = average (usage amount / days)
                    for each day in the period            
                        if that date exists in dict, then add this usage amount to that date
                        otherwise, create a key in dict named after the date, and then assign the usage amount 
                If the period of days=1, then 
                    if that date exists in dict, then add this usage amount to that date
                    otherwise, create a key in dict named after the date, and then assign the usage amount
        """
        # check usageaccountid is legal
        if self.check_id_illegal(usageaccountid):
            abort(400, 'Invalid ID supplied. ID must be an integer and larger than 0')
        
        # load database config
        cfg = configparser.ConfigParser()
        cfg.read('conf.cfg')
        db_path = cfg['DB']['FOLDER'] + cfg['DB']['NAME']
        
        # connect to DB
        db_conn = sqlite3.connect( cfg['DB']['FOLDER']+cfg['DB']['NAME'] )
        c = db_conn.cursor()
        
        # query DB
        query = cfg['API']['SQL_get_amount']
        t = (usageaccountid,) # python suggests to provide a tuple of values as the second argument to the cursor’s execute() method
        results = c.execute( query, t ).fetchall()
        
        # deal with null response
        if not results:
            abort(404, 'The usage amount with the specified ID was not found')
            
        db_conn.close()
        return jsonify(results)
    