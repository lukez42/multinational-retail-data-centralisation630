import pandas as pd
import os

class DataCleaning:
    """
    A utility class to clean data from various sources.
    """
    def __init__(self):
        self.df = None
        self.csv_file_path = "debug_csv" # Define the path to the CSV file

    def clean_user_data(self, df):
        """
        Cleans user data based on the specified requirements.

        Args:
            df (pd.DataFrame): DataFrame containing user data.

        Returns:
            pd.DataFrame: Cleaned user data.
        """
        # Step 1: Replace "NULL" strings and empty strings with pd.NA
        print(f"Initial number of rows: {len(df)}")
        df.replace(["NULL", ""], pd.NA, inplace=True)
        print(f"Rows after replacing 'NULL' strings: {len(df)}")

        # Step 2: Remove NULL values
        df.dropna(inplace=True)
        print(f"Rows after dropping NULLs: {len(df)}")

        # Step 3: Convert "join_date" with flexible parsing
        df["join_date"] = pd.to_datetime(
            df["join_date"],
            format="mixed",  # Handles multiple date formats
            dayfirst=True,  # Prioritize day-month-year format
            errors="coerce",
        )
        print(f"Rows after converting 'join_date': {len(df)}")

        # Step 4: Drop rows with invalid dates
        df = df.dropna(subset=["join_date"])
        print(f"Final rows after date cleaning in user data: {len(df)}")

        return df

    def clean_card_data(self, df):
        """
        Cleans card data based on the specified requirements.
        Args:
            df (pd.DataFrame): DataFrame containing card data.
        Returns:
            pd.DataFrame: Cleaned card data with 'date_payment_confirmed' as datetime.
        """
        # Create the directory if it doesn't exist
        task_dir = os.path.join(self.csv_file_path, "task_4")
        os.makedirs(task_dir, exist_ok=True)  # Ensure the directory exists

        # Step 1: Replace "NULL" strings with pd.NA
        print(f"Initial number of rows: {len(df)}")
        df = df.replace("NULL", pd.NA)  # Use explicit assignment to avoid views
        null_replaced_file_path = os.path.join(task_dir, "null_replaced_rows.csv")
        df.to_csv(null_replaced_file_path, index=False)  # Export replaced NULL rows
        print(f"Rows after replacing 'NULL' strings: {len(df)}")

        # Step 2: Remove NULL values
        removed_nulls = df[df.isna().any(axis=1)]  # Rows with any NULL values
        removed_nulls_file_path = os.path.join(task_dir, "removed_nulls.csv")
        removed_nulls.to_csv(
            removed_nulls_file_path, index=False
        )  # Export rows with NULLs removed
        df = df.dropna()  # Use explicit assignment to avoid views
        print(f"Rows after dropping NULLs: {len(df)}")

        # Step 3: Remove duplicates
        removed_duplicates = df[
            df.duplicated(subset=["card_number"], keep="first")
        ]  # Duplicate rows
        removed_duplicates_file_path = os.path.join(task_dir, "removed_duplicates.csv")
        removed_duplicates.to_csv(
            removed_duplicates_file_path, index=False
        )  # Export duplicate rows
        df = df.drop_duplicates(
            subset=["card_number"]
        )  # Use explicit assignment to avoid views
        print(f"Rows after removing duplicates: {len(df)}")

        # Step 4: Clean non-numeric card numbers (retain only digits)
        def clean_card_number(card_num):
            # Remove all non-numeric characters
            return "".join(filter(str.isdigit, str(card_num)))

        # Apply the cleaning function to the 'card_number' column
        original_card_numbers = df[
            "card_number"
        ].copy()  # Save original card numbers for comparison
        df["card_number"] = df["card_number"].apply(clean_card_number)

        # Identify rows where card numbers were changed
        modified_rows = df[original_card_numbers != df["card_number"]]
        modified_rows_file_path = os.path.join(task_dir, "modified_card_numbers.csv")
        modified_rows.to_csv(
            modified_rows_file_path, index=False
        )  # Export modified rows to CSV
        print(f"Rows with modified card numbers exported to {modified_rows_file_path}")

        # Step 5: Remove rows with empty card numbers (if any)
        df = df[df["card_number"].str.len() > 0]
        print(f"Rows after cleaning card numbers: {len(df)}")

        # Step 6: Convert 'date_payment_confirmed' to datetime
        df["date_payment_confirmed"] = pd.to_datetime(
            df["date_payment_confirmed"], format="mixed", dayfirst=True, errors="coerce"
        )
        df.dropna(
            subset=["date_payment_confirmed"], inplace=True
        )  # Drop rows with invalid dates
        print(f"Final rows after date cleaning: {len(df)}")

        return df

    def clean_store_data(self, df):
        """
        Cleans the store data while retaining Store 0 and logging removed rows for debugging.
        """
        # Create the directory if it doesn't exist
        task_dir = os.path.join(self.csv_file_path, "task_5")
        os.makedirs(task_dir, exist_ok=True)  # Ensure the directory exists
        print(f"Initial rows: {len(df)}")

        # Step 1: Replace both "NULL" AND "N/A" with pd.NA
        df.replace(["NULL", "N/A", "None", "nan"], pd.NA, inplace=True)
        print(f"Rows after replacing invalid strings with pd.NA: {len(df)}")

        # Step 2: Handle Store 0 separately
        store_0 = df[df["index"] == 0].copy()  # Extract Store 0
        df = df[
            df["index"] != 0
        ].copy()  # Exclude Store 0 from the main DataFrame (explicit copy)

        # Step 3: Remove NULL values (excluding Store 0)
        cols_to_check = ["address", "longitude", "latitude", "locality", "country_code"]
        removed_nulls = df[
            df[cols_to_check].isna().any(axis=1)
        ].copy()  # Rows with NULLs in key columns
        df.dropna(subset=cols_to_check, inplace=True)
        removed_nulls.to_csv(os.path.join(task_dir, "removed_nulls.csv"), index=False)
        print(f"Rows after dropping NULLs: {len(df)}")

        # Step 4: Clean staff_numbers (more robust)
        df.loc[:, "staff_numbers"] = (
            df["staff_numbers"]
            .astype(str)
            .str.replace(r"[^0-9]", "", regex=True)  # Remove all non-numeric characters
            .replace("", pd.NA)  # Treat empty strings as NULL
        )
        removed_staff_numbers = df[
            df["staff_numbers"].isna()
        ].copy()  # Rows with invalid staff_numbers
        df.dropna(subset=["staff_numbers"], inplace=True)
        removed_staff_numbers.to_csv(
            os.path.join(task_dir, "removed_staff_numbers.csv"), index=False
        )
        print(f"Rows after staff number cleanup: {len(df)}")

        # Step 5: Validate opening_date
        df.loc[:, "opening_date"] = pd.to_datetime(
            df["opening_date"], format="mixed", dayfirst=True, errors="coerce"
        )
        removed_dates = df[df["opening_date"].isna()].copy()  # Rows with invalid dates
        df.dropna(subset=["opening_date"], inplace=True)
        removed_dates.to_csv(os.path.join(task_dir, "removed_dates.csv"), index=False)
        print(
            f"Rows after converting opening_date column into a datetime data type: {len(df)}"
        )

        # Step 6: Reintegrate Store 0 (if valid)
        if not store_0.empty:
            # Clean Store 0's staff_numbers and opening_date
            store_0.loc[:, "staff_numbers"] = (
                store_0["staff_numbers"]
                .astype(str)
                .str.replace(r"[^0-9]", "", regex=True)
                .replace("", pd.NA)
            )
            store_0.loc[:, "opening_date"] = pd.to_datetime(
                store_0["opening_date"], format="mixed", dayfirst=True, errors="coerce"
            )
            # Only reintegrate if staff_numbers and opening_date are valid
            if (
                not store_0["staff_numbers"].isna().any()
                and not store_0["opening_date"].isna().any()
            ):
                df = pd.concat([df, store_0], ignore_index=True)
                print("Store 0 reintegrated after cleaning.")
            else:
                print("Store 0 could not be reintegrated due to invalid data.")

        print(f"Final rows after date validation: {len(df)}")
        return df

    def convert_product_weights(self, df):
        """
        Converts the weight column to a decimal value representing the weight in kg.

        Args:
            df (pd.DataFrame): The DataFrame containing the products data.

        Returns:
            pd.DataFrame: The DataFrame with the cleaned weight column.
        """
        task_dir = os.path.join(self.csv_file_path, "task_6")
        os.makedirs(task_dir, exist_ok=True)  # Ensure the directory exists

        df.to_csv(os.path.join(task_dir, "original.csv"), index=False)

        def convert_weight(weight):
            try:
                # Handle weights like "12 x 100g"
                if "x" in weight:
                    quantity, unit_weight = weight.split("x")
                    quantity = float(quantity.strip())
                    unit_weight = unit_weight.strip()
                    weight = f"{quantity * float(unit_weight[:-1])}{unit_weight[-1]}"

                # Extract numeric value and unit
                if "kg" in weight:
                    return float(weight.replace("kg", "").strip())
                elif "g" in weight:
                    return float(weight.replace("g", "").strip()) / 1000
                elif "ml" in weight:
                    return float(weight.replace("ml", "").strip()) / 1000  # 1:1 ml to g
                elif "oz" in weight:
                    return float(weight.replace("oz", "").strip()) * 0.0283495
                else:
                    return pd.NA
            except:
                return pd.NA

        df["weight"] = df["weight"].apply(convert_weight)
        return df

    def clean_products_data(self, df):
        """
        Cleans the products DataFrame and logs removed rows for debugging.

        Args:
            df (pd.DataFrame): The DataFrame containing the products data.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        # Create the directory if it doesn't exist
        task_dir = os.path.join(self.csv_file_path, "task_6")
        os.makedirs(task_dir, exist_ok=True)  # Ensure the directory exists

        print(f"Initial rows: {len(df)}")

        # Step 1: Replace "NULL" strings with pd.NA
        df.replace(["NULL", "N/A", "None", "nan"], pd.NA, inplace=True)
        print(f"Rows after replacing invalid strings: {len(df)}")

        # Step 2: Handle row with index=1779 (set weight to 0 if NULL)
        if 1779 in df.index and pd.isna(df.loc[1779, "weight"]):
            df.loc[1779, "weight"] = 0  # Directly set weight to 0 if it's NULL
            print(f"Row 1779: Set weight to 0 (previously NULL) as all the other values are valid.")

        # Step 3: Remove NULL values (excluding row 1779)
        removed_nulls = df[
            df.isna().any(axis=1) & (df.index != 1779)
        ]  # Exclude row 1779
        df.dropna(inplace=True)
        removed_nulls.to_csv(os.path.join(task_dir, "removed_nulls.csv"), index=False)
        print(f"Rows after dropping NULLs: {len(df)}")

        # Step 4: Clean the 'weight' column (already handled in convert_product_weights)
        print(f"Rows after converting weights to kg: {len(df)}")

        print(f"Final rows after cleaning: {len(df)}")
        return df

    def clean_orders_data(self, df):
        """
        Cleans the orders DataFrame by removing unwanted columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the orders data.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        # Step 1: Remove unwanted columns
        columns_to_remove = ["first_name", "last_name", "1"]
        df = df.drop(
            columns=columns_to_remove, errors="ignore"
        )  # Ignore if columns don't exist

        # Step 2: Log the number of rows after cleaning
        print(f"Rows after cleaning: {len(df)}")

        return df

    def clean_date_times_data(self, df):
        """
        Cleans the date times DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the date times data.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        # Step 1: Replace "NULL" strings with pd.NA
        df.replace(["NULL", "N/A", "None", "nan"], pd.NA, inplace=True)

        # Step 2: Remove NULL values
        df.dropna(inplace=True)

        # Step 3: Convert "day", "month", and "year" columns to numeric
        for col in ["day", "month", "year"]:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )  # Convert to numeric, invalid parsing -> NaN

        # Step 4: Remove rows with invalid numeric values
        df.dropna(subset=["day", "month", "year"], inplace=True)

        # Step 5: Convert "day" and "month" columns to int dtype
        df["day"] = df["day"].astype(int)
        df["month"] = df["month"].astype(int)
        df["year"] = df["year"].astype(int)

        # Step 6: Log the number of rows after cleaning
        print(f"Rows after cleaning: {len(df)}")

        return df
