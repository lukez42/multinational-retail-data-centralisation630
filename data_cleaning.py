import pandas as pd


class DataCleaning:
    """
    A utility class to clean data from various sources.
    """

    def __init__(self):
        pass

    def clean_user_data(self, df):
        """
        Cleans user data.

        Args:
            df (pd.DataFrame): DataFrame containing user data.

        Returns:
            pd.DataFrame: Cleaned user data.
        """
        # Drop rows with NULL values
        df = df.dropna()

        # Convert date columns to datetime
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
        df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")

        # Drop rows with invalid dates
        df = df.dropna(subset=["date_of_birth", "join_date"])

        # Remove duplicates
        df = df.drop_duplicates()

        # Clean phone numbers (example)
        df["phone_number"] = df["phone_number"].str.replace(r"[^0-9]", "", regex=True)

        return df
