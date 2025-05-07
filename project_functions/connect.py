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
            self.creds = {}
            with open(path) as f:
                for i, line in enumerate(f.readlines()):
                    if i==0:
                        self.creds["user"]=line.strip()
                    else:
                        self.creds["pass"]=line.strip()

            self._test_connection()

            return self.engine
        
        except Exception as e:
            print(f"Error: {e}")

    def _test_connection(self):
        self.engine=f'postgresql://{self.creds["user"]}:{self.creds["pass"]}@{self.host}:{self.port}/{self.db}'
        try:
            pd.read_sql_query("""
                              SELECT * 
                              FROM INFORMATION_SCHEMA.TABLES
                              """
                        ,self.engine)
            print(f"User: {self.creds["user"]} successfully connected to {self.db}!")
            
        except Exception as e:
            print(f"Error: {e}")