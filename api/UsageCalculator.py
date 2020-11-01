import sqlite3, configparser, datetime
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
        rtype: flask.wrappers.Response
                200: required dictionary
                400: Invalid ID supplied. ID must be an integer and larger than 0
                404: The usage amount of the specified ID was not found
        
        Output example of required dictionary
        {
          "AWS Premium Support": {
            "YYYY/MM/01": 1.0,
            "YYYY/MM/02": 1.0
          },
          "Amazon Elastic Compute Cloud": {
            "YYYY/MM/01": 1.0,
            "YYYY/MM/02": 0.0
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
            # init "product usage" dict if there is a product but dict has no corresponding product key
            # average the usage amount in the period (days) to each date
            # for each day
            # # init "daily usage" dict if there is a usage of that date but dict has no corresponding date key
            # # add average usage amount to this date
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
        
        db_conn.close()
        
        # deal with null response
        if not results:
            abort(404, 'The usage amount of the specified ID was not found')
            
        # parse to required dictionary
        response={}    
        for entity in enumerate(results):
            product_name = entity[1][0]
            usage_amount = entity[1][1]
            start_date = entity[1][2]
            days = entity[1][3]
            
            # init "product usage" dict for daily usage statistic of a product
            if product_name not in response:
                response[product_name]={}
            
            # average the usage amount in the period (days) to each date
            avg_amount = usage_amount/days
            
            day_offset=0 # day offset to be added to the date
            # add average usage amount to every day in the period
            for _ in range(days):
                date = (datetime.datetime.strptime(start_date, "%Y-%m-%d")+datetime.timedelta(days=day_offset)).strftime('%Y-%m-%d')
                # init "daily usage" dict for usage amount per day
                if date not in response[product_name]:
                    response[product_name][date]=0
                response[product_name][date] += avg_amount
                day_offset += 1
                
        # add 200 OK
        response = jsonify(response)
        response.status_code = 200
        
        return response
    