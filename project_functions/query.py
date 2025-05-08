from project_functions.connect import Connect
import pandas as pd

class Query():
    """
    Wrapper around the connection class to handle SQL queries to the database connection.
    """
    def __init__(self, connection:Connect):
        """
        Take in the database connection engine and set it as an attribute.
        """
        self.engine = connection.engine

    def read_query(self, query:str, params=()):
        """
        Take in a SQL query as a parameter and return the response from the database.

        This utilizes the engine from Connect, which allows for the query class to be invariant 
        to changes in the connection parameters.
        """
        try:
            return pd.read_sql_query(f"{query}",self.engine, params=params)
        except Exception as e:
            print(f"Error: {e}")


