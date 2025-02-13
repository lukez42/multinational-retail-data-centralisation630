# main.py
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Step 1: Initialize classes
db_connector = DatabaseConnector()
data_extractor = DataExtractor()
data_cleaner = DataCleaning()

# Step 2: List tables and extract user data
tables = db_connector.list_db_tables()
print("Tables in the database:", tables)

user_table_name = "legacy_users"  # Replace with the actual table name
user_df = data_extractor.read_rds_table(db_connector, user_table_name)

# Step 3: Clean user data
cleaned_user_df = data_cleaner.clean_user_data(user_df)

# Step 4: Upload cleaned data to the database
db_connector.upload_to_db(cleaned_user_df, "dim_users")

# Verify the number of rows
print("Number of rows after cleaning:", len(cleaned_user_df))
