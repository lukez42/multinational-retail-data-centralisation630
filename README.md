# Multinational Retail Data Centralisation

---
[![python](https://img.shields.io/badge/python-3.10.15-blue?style=plastic&logo=python)](https://www.python.org/downloads/release/python-31015/)
## Table of Contents
- [Multinational Retail Data Centralisation](#multinational-retail-data-centralisation)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
    - [Objectives](#objectives)
  - [Local Deployment](#local-deployment)
    - [Data Source Changes](#data-source-changes)
    - [Local Directory Structure](#local-directory-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [File Structure](#file-structure)
  - [License](#license)

---

## Description
This project is a data cleaning and extraction pipeline designed to process and clean data from multiple sources (e.g., CSV files, APIs, databases) and upload the cleaned data to a local PostgreSQL database. The aim of the project is to demonstrate proficiency in data cleaning, extraction, processing and database management using Python & various Python libraries and pgAdmin 4.

### Objectives
- How to extract data from various sources (RDS, PDF, API, CSV, JSON).
- Techniques for cleaning and transforming data using pandas.
- How to upload cleaned data to a PostgreSQL database.
- How to effectively query and analyse data using SQL.
- Best practices for version control and documentation using GitHub.

---

## Local Deployment

To reduce costs, this project has been migrated from cloud-based data sources to local storage. The following changes have been implemented:

### Data Source Changes

| Task | Original Source | New Local Source |
|------|----------------|-----------------|
| Task 3: Extract user data | AWS RDS Database | `Legacy_RDS/legacy_users.csv` and `Legacy_RDS/orders_table.csv` |
| Task 4: Extract card details | S3 PDF link | Local file: `card_details.pdf` |
| Task 5: Extract store details | API endpoints | Local file: `legacy_store_details.csv` |
| Task 6: Extract product details | S3 CSV link | Local file: `products.csv` |
| Task 7: Retrieve orders table | AWS RDS Database | `Legacy_RDS/orders_table.csv` |
| Task 8: Retrieve date events data | S3 JSON link | Local file: `date_details.json` |

### Local Directory Structure

```
Legacy_Data_Source/                # Local data source files
├── Legacy_RDS/                    # Tables from AWS RDS
│   ├── legacy_users.csv           # Task 3: User data table
│   └── orders_table.csv           # Task 7: Orders data table
├── card_details.pdf               # Task 4: Card details document
├── date_details.json              # Task 8: Date events data
├── legacy_store_details.csv       # Task 5: Store details data
└── products.csv                   # Task 6: Product details data

Data_Cleaning_Requirments/         # Data cleaning instructions
├── Task3_Legacy-Table-Cleaning-Requirements.md.txt
├── Task4_Card-Details-Cleaning-Requirement.md.txt
├── Task5_Store-Details-Cleaning-Requirements.md.txt
├── Task6_Product-Details-Cleaning-Requirements.md.txt
├── Task7_Order-Data-Cleaning-Requirements.md.txt
└── Task8_Date-Details-Cleaning-Requirements.md.txt
```

---

## Installation
To run this project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/lukez42/multinational-retail-data-centralisation630.git
   cd multinational-retail-data-centralisation630
   ```
2. **Set Up a Virtual Environment (conda)**:
3. **Install Dependencies**:
   See `requirements.txt` for a list of required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up PostgreSQL Database and Open Source graphical management tool for PostgreSQL(pgAdmin 4)**:

## Usage

1. **Run the Main Script:**
   <!-- ```
   python main.py
   ```
   or -->
   `main.py` is *for testing only*.

   **The complete code is in `main.ipynb`. Run this file interactively in your IDE/Jupyter Notebook to produce cleaned and formatted data (preferred)**

2. **View Cleaned Data**:
   Connect to your PostgreSQL database and query the tables (e.g., dim_users, dim_products, dim_date_times, dim_store_details, dim_card_details, orders_table).

3. **Query Cleaned Data**:
   Run `sales_data_milstone3.sql` and `sales_data_milstone4.sql` to check SQL output for Milestone 3 and 4.

Please note that for some tasks in Milestones 3 and 4, the SQL queries are in `sales_data_milstone3.sql` and `sales_data_milstone4.sql` respectively. Please follow the instructions in `main.ipynb` to run code interactively in your IDE/Jupyter Notebook and switch to pgAdmin 4 to query the tables if necessary.

## File Structure
```
.
├── README.md                          # Project documentation
├── main.ipynb                         # Main Jupyter notebook for analysis or exploration
├── main.py                            # Main script to run the pipeline (for testing)
├── local_db_creds.yaml                # Local PostgreSQL database credentials (.gitignore)
├── data_cleaning.py                   # Contains data cleaning methods
├── data_extraction.py                 # Contains data extraction methods
├── database_utils.py                  # Contains database connection and upload methods
├── Legacy_Data_Source/                # Local data source files
├── Data_Cleaning_Requirments/         # Data cleaning instructions
├── debug_csv/                         # Debugging CSV files
├── requirements.txt                   # List of dependencies
├── sales_data_milstone3.sql           # SQL queries for Milestone 3
└── sales_data_milstone4.sql           # SQL queries for Milestone 4
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
