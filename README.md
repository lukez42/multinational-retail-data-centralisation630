# Multinational Retail Data Centralisation

---
[![python](https://img.shields.io/badge/python-3.10.15-blue?style=plastic&logo=python)](https://www.python.org/downloads/release/python-31015/)
## Table of Contents
- [Multinational Retail Data Centralisation](#multinational-retail-data-centralisation)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
    - [Objectives](#objectives)
  - [Installation](#installation)
  - [Usage](#usage)
  - [File Structure](#file-structure)
  - [License](#license)

---

## Description
This project is a data cleaning and extraction pipeline designed to process and clean data from multiple sources (e.g., CSV files, APIs, databases) and upload the cleaned data to a local PostgreSQL database. The aim of the project is to demonstrate proficiency in data cleaning, extraction, processing and database management using Python & various Python libraries and pgAdmin 4.

### Objectives
- How to extract data from various sources (CSV, API, database).
- Techniques for cleaning and transforming data using pandas.
- How to upload cleaned data to a PostgreSQL database.
- How to effectively query and analyze data using SQL.
- Best practices for version control and documentation using GitHub.

---

## Installation
To run this project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/luke-who/multinational-retail-data-centralisation630.git
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

   **The complete code is in `main.ipynb` run this file interactively in your IDE/Jupyter Notebook to produced cleaned and formatted data (preferred)**

2. **View Cleaned Data**:
   Connect to your PostgreSQL database and query the tables (e.g., dim_users, dim_products, dim_date_times, dim_store_details, dim_card_details, orders_table).

3. **Query Cleaned Data**:
   Run `sales_data_milstone3.sql` and `sales_data_milstone4.sql` to check SQL output for Mileestone 3 and 4.

Please note for some tasks in Milestone 3 and 4, the SQL queries are in `sales_data_milstone3.sql` and `sales_data_milstone4.sql` respectively. Please follow the instructions in `main.ipynb` to run code interactively in your IDE/Jupyter Notebook and switch to pgAdmin 4 to query the tables if necessary.

## File Structure
```
.
├── README.md                 # Project documentation
├── main.ipynb                # Main Jupyter notebook for analysis or exploration
├── main.py                   # Main script to run the pipeline (for testing)
├── aws_db_creds.yaml         # AWS RDS database credentials (.gitignore)
├── local_db_creds.yaml       # Local PostgreSQL database credentials (.gitignore)
├── data_cleaning.py          # Contains data cleaning methods
├── data_extraction.py        # Contains data extraction methods
├── database_utils.py         # Contains database connection and upload methods
├── debug_csv/                # Debugging CSV files
├── requirements.txt          # List of dependencies
├── sales_data_milstone3.sql  # SQL queries for Mileestone 3
└── sales_data_milstone4.sql  # SQL queries for Mileestone 4
```

## License
