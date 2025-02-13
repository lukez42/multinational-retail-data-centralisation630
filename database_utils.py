import sqlalchemy
import yaml


class DatabaseConnector:
    """
    A utility class to connect to a database and upload data.
    """

    def __init__(self, creds_file="db_creds.yaml"):
        """
        Initializes the DatabaseConnector with credentials.

        Args:
            creds_file (str): Path to the YAML file containing database credentials.
        """
        self.creds = self.read_db_creds(creds_file)

    def read_db_creds(self, creds_file):
        """
        Reads the database credentials from a YAML file.

        Args:
            creds_file (str): Path to the YAML file.

        Returns:
            dict: Database credentials.
        """
        with open(creds_file, "r") as file:
            return yaml.safe_load(file)

    def init_db_engine(self):
        """
        Initializes and returns a SQLAlchemy database engine.

        Returns:
            sqlalchemy.engine.Engine: Database engine.
        """
        connection_string = (
            f"postgresql://{self.creds['RDS_USER']}:{self.creds['RDS_PASSWORD']}@"
            f"{self.creds['RDS_HOST']}:{self.creds['RDS_PORT']}/{self.creds['RDS_DATABASE']}"
        )
        return sqlalchemy.create_engine(connection_string)

    def list_db_tables(self):
        """
        Lists all tables in the database.

        Returns:
            list: List of table names.
        """
        engine = self.init_db_engine()
        with engine.connect() as connection:
            return sqlalchemy.inspect(engine).get_table_names()

    # database_utils.py (continued)
    def upload_to_db(self, df, table_name):
        """
        Uploads a DataFrame to a database table.

        Args:
            df (pd.DataFrame): DataFrame to upload.
            table_name (str): Name of the table.
        """
        engine = self.init_db_engine()
        df.to_sql(table_name, engine, if_exists="replace", index=False)
