from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    ########## Task 3 ############
    try:
        aws_connector = DatabaseConnector(creds_file="aws_db_creds.yaml")
        data_extractor = DataExtractor()
        data_cleaner = DataCleaning()
        local_connector = DatabaseConnector(creds_file="local_db_creds.yaml")

        # Step 1: Extract data from AWS RDS
        table_names_list = aws_connector.list_db_tables()
        logging.info(f"List of table names: {table_names_list}")
        user_table_name = table_names_list[2]
        user_df = data_extractor.read_rds_table(aws_connector, user_table_name)

        # Step 2: Clean data
        cleaned_user_df = data_cleaner.clean_user_data(user_df)

        # Step 3: Upload to local database
        local_connector.upload_to_db(cleaned_user_df, "dim_users")
        logging.info("Uploaded cleaned user data to the local sales_data database.")

    except Exception as e:
        logging.error(f"Error in Task 3: {e}")

    ########## Task 4 ############
    try:
        # Step 1: Retrieve card data from the PDF
        pdf_link = (
            "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        )
        card_df = data_extractor.retrieve_pdf_data(pdf_link)

        # Step 2: Clean card data
        cleaned_card_df = data_cleaner.clean_card_data(card_df)
        logging.info(f"Cleaned card data info:\n{cleaned_card_df.info()}")

        # Step 3: Upload to local database
        local_connector.upload_to_db(cleaned_card_df, "dim_card_details")
        logging.info("Uploaded cleaned card data to the local sales_data database.")

    except Exception as e:
        logging.error(f"Error in Task 4: {e}")

    ########## Task 5 ############
    try:
        # Initialize classes
        data_extractor = DataExtractor()
        data_cleaner = DataCleaning()
        local_connector = DatabaseConnector(creds_file="local_db_creds.yaml")

        # Step 1: Retrieve the number of stores
        number_of_stores_endpoint = (
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        )
        num_stores = data_extractor.list_number_of_stores(number_of_stores_endpoint)
        logging.info(f"Number of stores to retrieve: {num_stores}")

        # Step 2: Retrieve all stores data
        retrieve_store_endpoint = (
            "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details"
        )
        stores_df = data_extractor.retrieve_stores_data(
            retrieve_store_endpoint, num_stores
        )
        logging.info(f"Retrieved {len(stores_df)} stores from the API.")

        # Step 3: Clean the store data
        cleaned_stores_df = data_cleaner.clean_store_data(stores_df)
        logging.info(f"Cleaned store data has {len(cleaned_stores_df)} rows.")

        # Step 4: Upload the cleaned data to the database
        local_connector.upload_to_db(cleaned_stores_df, "dim_store_details")
        logging.info("Uploaded cleaned store data to the local sales_data database.")

    except Exception as e:
        logging.error(f"Error in main workflow: {e}")

    local_connector.shutdown_jvm()  # shut down the JVM when you are done with the extraction process.


if __name__ == "__main__":
    main()
