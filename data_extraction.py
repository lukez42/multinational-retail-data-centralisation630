import tabula
import pandas as pd
import jpype
import requests
import logging
import boto3
from io import StringIO

class DataExtractor:
    """
    A utility class to extract data from various sources.
    """

    def __init__(self):
        # Start the JVM with the correct path
        if not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath())

        # Initialize the headers for API requests
        self.headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}

    def read_rds_table(self, db_connector, table_name):
        """
        Extracts data from an RDS database table.

        Args:
            db_connector (DatabaseConnector): Instance of DatabaseConnector.#-
            table_name (str): Name of the table to extract.#-
            db_connector (DatabaseConnector): An instance of DatabaseConnector, which provides a connection to the RDS database.#+
            table_name (str): The name of the table from which to extract data.#+

        Returns:
            pd.DataFrame: Data extracted from the table.#-
            pd.DataFrame: A pandas DataFrame containing the extracted data from the specified RDS database table.#+
        """
        engine = db_connector.init_db_engine()
        return pd.read_sql_table(table_name, engine)

    def retrieve_pdf_data(self, link):
        """Extracts data from a PDF document stored in an S3 bucket."""
        try:
            # Use tabula to extract all pages from the PDF
            dfs = tabula.read_pdf(link, pages="all", multiple_tables=True)
            # Combine all pages into a single DataFrame
            return pd.concat(dfs, ignore_index=True)
        except Exception as e:
            print(f"Error extracting data from PDF: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def list_number_of_stores(self, number_of_stores_endpoint):
        """
        Retrieves the number of stores from the API.

        Args:
            number_of_stores_endpoint (str): The API endpoint to retrieve the number of stores.

        Returns:
            int: The number of stores.
        """
        try:
            response = requests.get(number_of_stores_endpoint, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json().get("number_stores")
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving number of stores: {e}")
            return 0

    def retrieve_stores_data(self, retrieve_store_endpoint, num_stores):
        """
        Retrieves data for all stores from the API.

        Args:
            retrieve_store_endpoint (str): The API endpoint to retrieve store details.
            num_stores (int): The number of stores to retrieve.

        Returns:
            pd.DataFrame: A DataFrame containing all store details.
        """
        stores_data = []
        for store_number in range(0, num_stores):  # Start from 0 to include all stores
            try:
                response = requests.get(
                    f"{retrieve_store_endpoint}/{store_number}", headers=self.headers
                )
                response.raise_for_status()  # Raise an exception for HTTP errors
                store_details = response.json()
                stores_data.append(store_details)
            except requests.exceptions.HTTPError as e:
                if response.status_code == 500:
                    logging.warning(
                        f"Skipping store {store_number} due to server error: {e}"
                    )
                else:
                    logging.error(f"Error retrieving store {store_number}: {e}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error retrieving store {store_number}: {e}")

        return pd.DataFrame(stores_data)

    def extract_from_s3(self, s3_address):
        """
        Extracts data from an S3 bucket and returns it as a pandas DataFrame.

        Args:
            s3_address (str): The S3 address of the file (e.g., "s3://bucket-name/file.csv").

        Returns:
            pd.DataFrame: The extracted data.
        """
        try:
            # Parse the S3 address
            bucket_name = s3_address.split("/")[2]
            file_key = "/".join(s3_address.split("/")[3:])

            # Initialize S3 client
            s3_client = boto3.client("s3")

            # Download the file
            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = response["Body"].read().decode("utf-8")

            # Load the CSV content into a DataFrame
            df = pd.read_csv(StringIO(file_content))
            return df
        except Exception as e:
            print(f"Error extracting data from S3: {e}")
            return pd.DataFrame()


    def extract_json_from_s3(self, s3_url):
        """
        Extracts JSON data from a publicly accessible S3 URL and returns it as a pandas DataFrame.

        Args:
            s3_url (str): The S3 URL of the JSON file.

        Returns:
            pd.DataFrame: The extracted data.
        """
        try:
            # Directly load the JSON file from the URL
            df = pd.read_json(s3_url)
            print("Date times data extracted successfully.")
            return df
        except Exception as e:
            print(f"Error extracting JSON data from S3: {e}")
            return pd.DataFrame()

    def shutdown_jvm(self):
        if jpype.isJVMStarted():
            jpype.shutdownJVM()
