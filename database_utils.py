import sqlalchemy
import yaml

class DatabaseConnector:
    """
    A utility class to connect to different databases (AWS RDS or local).
    """

    def __init__(self, creds_file):
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

    def init_db_engine(self, source="aws"):
        """Initializes and returns a SQLAlchemy database engine."""
        try:
            if source == "aws":
                connection_string = (
                    f"postgresql://{self.creds['RDS_USER']}:{self.creds['RDS_PASSWORD']}@"
                    f"{self.creds['RDS_HOST']}:{self.creds['RDS_PORT']}/{self.creds['RDS_DATABASE']}"
                )
            elif source == "local":
                connection_string = (
                    f"postgresql://{self.creds['RDS_USER']}:{self.creds['RDS_PASSWORD']}@"
                    f"{self.creds['RDS_HOST']}:{self.creds['RDS_PORT']}/{self.creds['RDS_DATABASE']}"
                )
            return sqlalchemy.create_engine(connection_string)
        except Exception as e:
            print(f"Error initializing database engine: {e}")
            return None

    def list_db_tables(self):
        """
        Lists all tables in the AWS RDS database.
        """
        engine = self.init_db_engine(source="aws")
        with engine.connect() as connection:
            return sqlalchemy.inspect(engine).get_table_names()

    def upload_to_db(self, df, table_name, dtype=None):
        """
        Uploads a DataFrame to the local PostgreSQL database.
        """
        engine = self.init_db_engine(source="local")
        df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=dtype)
        print(f"Uploaded {len(df)} rows to {table_name}.")
