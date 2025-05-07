import pandas as pd
import os

class Connect():
    """
    Wrapper for pandas SQL engine and query management.

    Additional functionality has been added for credential ingestion from a text file.
    """
    def __init__(self, host:str = 'localhost', port:str = '5432', db:str = 'bank'):
        self.host = host
        self.port = port
        self.db = db
        self.engine=f'postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASS')}@{self.host}:{self.port}/{self.db}'

    def connect(self, path:str):
        """
        Read in the credentials from 'path' and test the DB connection.
        """
        try:
            creds = {}
            with open(path) as f:
                for i, line in enumerate(f.readlines()):
                    if i==0:
                        creds["user"]=line.strip()
                    else:
                        creds["pass"]=line.strip()

            self.engine = self._test_connection(user=creds["user"], password=creds["pass"])
        
        except Exception as e:
            print(f"Error: {e}")

    def _test_connection(self, user, password):
        try:
            engine = f'postgresql://{user}:{password}@{self.host}:{self.port}/{self.db}'

            pd.read_sql_query("""
                              SELECT * 
                              FROM INFORMATION_SCHEMA.TABLES
                              """
                        ,engine)
            
            print(f"User: {user} successfully connected to {self.db}!")
            return engine
            
        except Exception as e:
            print(f"Error: {e}")