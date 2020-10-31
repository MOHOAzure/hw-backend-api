import sqlite3, configparser
from flask import abort

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
        rtype: list of tuple
        
        Output : example
        [
            (0, ('AWS Data Transfer', 0.0)),
            (1, ('Amazon DynamoDB', 1.7450000000000003e-07)),
            (2, ('Amazon Elastic Compute Cloud', 25.358105829299983)),
            (3, ('Amazon Simple Storage Service', 0.000405)),
            (4, ('AmazonCloudWatch', 0.0022699999999999994))
        ]
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
            abort(404, 'The cost with the specified ID was not found')
        
        db_conn.close()
        return results
        