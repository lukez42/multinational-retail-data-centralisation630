import pandas as pd


class DataExtractor:
    """
    A utility class to extract data from various sources.
    """

    def __init__(self):
        pass

    def read_rds_table(self, db_connector, table_name):
        """
        Extracts data from an RDS database table.

        Args:
            db_connector (DatabaseConnector): Instance of DatabaseConnector.
            table_name (str): Name of the table to extract.

        Returns:
            pd.DataFrame: Data extracted from the table.
        """
        engine = db_connector.init_db_engine()
        return pd.read_sql_table(table_name, engine)
