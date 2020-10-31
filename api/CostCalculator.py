import sqlite3, configparser
from flask import abort, jsonify

class CostCalculator():
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
        
    def get_cost(self, usageaccountid):
        """
        rtype: flask.wrappers.Response
                200: required dictionary
                400: Invalid ID supplied. ID must be an integer and larger than 0
                404: The unblended cost of the specified ID was not found
        
        Output example of required dictionary
        {
          "AWS Premium Support": "0.0",
          "Amazon Elastic Compute Cloud": "0.0"
        }
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
        query = cfg['API']['SQL_get_cost']
        t = (usageaccountid,) # python suggests to provide a tuple of values as the second argument to the cursor’s execute() method
        results = c.execute( query, t ).fetchall()
        
        # deal with null response
        if not results:
            abort(404, 'The unblended cost of the specified ID was not found')
        
        # parse to required dictionary
        response={}    
        for u in enumerate(results):
            product_name = u[1][0]
            cost = u[1][1]
            response[ product_name ] = cost
            
        db_conn.close()
        return jsonify(response)
        