"""
This is a converter to load data from raw data file to web service database.

The jobs of the converter are:
    create database and data table
    insert data to database        
        load data from csv file
        select required columns of raw data
        insert data 

"""
import csv, sqlite3, configparser, os

def create_db():
    """
    rtype: bool
            True: db is ready
            False: db is not ready
    """
    # load config data for db
    cfg = configparser.ConfigParser()
    cfg.read('conf.cfg')
    
    # create data base
    print("\nCreating DB...")
    try:
        # create DB folder if it's not exists
        db_folder = cfg['DB']['FOLDER']
        if not os.path.exists( db_folder ):
            os.makedirs( db_folder )
        
        # connect to DB
        db_conn = sqlite3.connect( db_folder+cfg['DB']['NAME'] )
        c = db_conn.cursor()
        
        # create data table
        c.execute( cfg['CREATETABLE']['SQL'] )
        
        # create index
        c.execute( cfg['CREATEINDEX']['SQL'] )        
        
        db_conn.close()
        print("\nDB is ready.")
        return True
    except sqlite3.Error as error:
        print("\nError while creating DB:", error)
        return False
    
def populate_db():
    # load config data for rawdata
    cfg = configparser.ConfigParser()
    cfg.read('conf.cfg')
    
    # load data from csv file
    print("\Loading raw data...")
    with open(cfg['RAWDATA']['PATH'],'r') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter, first line as key
        # select required columns of raw data
        to_db = [(i[''], i['bill/PayerAccountId'], i['lineItem/UnblendedCost'], 
                    i['lineItem/UnblendedRate'], i['lineItem/UsageAccountId'], i['lineItem/UsageAmount'],
                    i['lineItem/UsageStartDate'], i['lineItem/UsageEndDate'], i['product/ProductName']) for i in dr]
    
    # populate database
    print("\nInserting data to DB...")
    try:
        # connect to DB
        db_conn = sqlite3.connect( cfg['DB']['FOLDER']+cfg['DB']['NAME'] )
        c = db_conn.cursor()
        
        # insert data to db
        c.executemany( cfg['INSERTTABLE']['SQL'], to_db)
        db_conn.commit()
        db_conn.close
        print("\nData is ready.")
    except sqlite3.Error as error:
        print("\nError while populating DB:", error)
    
if __name__ == "__main__":
    print("\nThe converter is working...")
    if create_db():
        populate_db()
    print("\nThe converter is finished.")