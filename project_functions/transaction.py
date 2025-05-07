from project_functions.connect import Connect
from project_functions.query import Query
import pandas as pd
from calendar import monthrange

class Transaction():
    """
    Wrapper around Connect and Query classes to query against the transactions database
    and validate the query results.
    """
    def __init__(self, connection:Connect):
        """
        Take in the database connection and set an internal attribute to the connection.
        """
        self.connection = connection
        self.query = Query(connection)

        #Ensure the user has access to this table and data can be read from it.
        self._validate_transaction_connection()

    def retreive_transactions(self, month:str, year:str):
        """
        Take in a month and year value in MM and YYYY format, respectively, and return a dataframe of all transactions in that time frame.

        Invalid queries should return a one row dataframe with -1 for all values.
        """

        try:
            max_day = monthrange(int(year),int(month))[1]
            min_date = f'{year}-{month}-01 00:00:00'
            max_date = f'{year}-{month}-{max_day} 00:00:00'

            result = self.query.read_query(f"""
                                    SELECT * 
                                    FROM transaction
                                    WHERE txn_date BETWEEN %s AND %s
                                """, params=(min_date, max_date))  
            
            assert len(result) > 0
                
            return result
        
        except Exception as e:
            # return the invalid df
            return self.invalid_df

    def _validate_transaction_connection(self):
        """
        Validate the connection to the transaction table. 
        
        Also, construct the dataframe that will be returned if self.retreive_transactions encounters an
        invalid month and year.
        """
        try:
            result = self.query.read_query("""
                                    SELECT *
                                    FROM transaction
                                    LIMIT 1
                                """)  

            # Construct the invalid dataframe from the result
            self.invalid_df = {}
            
            for col in result.columns:
                self.invalid_df[col]=[-1]
        
            self.invalid_df = pd.DataFrame(self.invalid_df)

        except Exception as e:
            print(f'ERROR: {e}')