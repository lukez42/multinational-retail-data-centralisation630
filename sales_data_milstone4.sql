-- Use the following code block to print all table names and their corresponding column names
SELECT 
    table_name, 
    column_name 
FROM 
    information_schema.columns 
WHERE 
    table_schema = 'public'  -- Change 'public' if your tables are in a different schema
ORDER BY 
    table_name, 
    ordinal_position;
-----------------
-- Milestone 4 --
-----------------
-- Task 1: How many stores does the business have and in which countries? --
SELECT 
	DISTINCT(country_code), COUNT(country_code) as total_no_stores
FROM 
	dim_store_details
GROUP BY
	country_code
ORDER BY
	total_no_stores DESC
-- Task 2: Which locations currently have the most stores? --
SELECT 
	DISTINCT(locality), COUNT(locality) as total_no_stores
FROM 
	dim_store_details
GROUP BY
	locality
ORDER BY
	total_no_stores DESC
-- Task 3: Which months produced the largest amount of sales? --
SELECT 
    dt.month,
    SUM(ot.product_quantity * dp.product_price) AS total_sales
FROM 
    orders_table ot
JOIN 
    dim_date_times dt ON ot.date_uuid = dt.date_uuid
JOIN 
    dim_products dp ON ot.product_code = dp.product_code
GROUP BY 
    dt.month
ORDER BY 
    total_sales DESC
LIMIT 6;

-- Task 4: How many sales are coming from online? The company is looking to increase its online sales. --
SELECT 
    CASE 
        WHEN store_code LIKE 'WEB%' THEN 'Web' 
        ELSE 'Offline' 
    END AS location,
    COUNT(*) AS numbers_of_sales,
    SUM(product_quantity) AS product_quantity_count
FROM 
    orders_table
GROUP BY 
    location
ORDER BY 
    location DESC;
-- Task 5: What percentage of sales come through each type of store? --
WITH sales_data AS (
    SELECT 
        ss.store_type,
        ot.product_quantity * dp.product_price AS revenue
    FROM 
        orders_table ot
    JOIN 
        dim_store_details ss ON ot.store_code = ss.store_code
    JOIN 
        dim_products dp ON ot.product_code = dp.product_code
),
aggregated_data AS (
    SELECT 
        store_type,
        SUM(revenue) AS total_sales,
        COUNT(*) AS sales_count
    FROM 
        sales_data
    GROUP BY 
        store_type
),
total_sales_summary AS (
    SELECT 
        SUM(total_sales) AS overall_total_sales,
        SUM(sales_count) AS overall_sales_count
    FROM 
        aggregated_data
)
SELECT 
    ad.store_type,
    ROUND(ad.total_sales, 2) AS total_sales,
    ROUND((ad.sales_count::NUMERIC / ts.overall_sales_count) * 100, 2) AS "sales_made(%)"
FROM 
    aggregated_data ad,
    total_sales_summary ts
ORDER BY 
    ad.total_sales DESC;
--TO CHECK Task 6: Which month in each year produced the highest cost of sales? --
WITH monthly_sales AS (
    SELECT 
        dt.year,
        dt.month,
        SUM(ot.product_quantity * dp.product_price) AS total_sales
    FROM 
        orders_table ot
    JOIN 
        dim_date_times dt ON ot.date_uuid = dt.date_uuid
    JOIN 
        dim_products dp ON ot.product_code = dp.product_code
    GROUP BY 
        dt.year, dt.month
),
ranked_sales AS (
    SELECT 
        year,
        month,
        total_sales,
        RANK() OVER (PARTITION BY year ORDER BY total_sales DESC) AS rank_within_year
    FROM 
        monthly_sales
)
SELECT 
    total_sales,
    year,
    month
FROM 
    ranked_sales
WHERE 
    rank_within_year = 1
ORDER BY 
    total_sales DESC
LIMIT 10;

-- Task 7: What is our staff headcount? --
SELECT 
    SUM(staff_numbers) AS total_staff_numbers,
    country_code
FROM 
    dim_store_details
GROUP BY 
    country_code
ORDER BY 
    total_staff_numbers DESC;

-- Task 8: Which German store type is selling the most? --
SELECT 
    SUM(ot.product_quantity * dp.product_price) AS total_sales,
    ss.store_type,
    ss.country_code
FROM 
    orders_table ot
JOIN 
    dim_store_details ss ON ot.store_code = ss.store_code
JOIN 
    dim_products dp ON ot.product_code = dp.product_code
WHERE 
    ss.country_code = 'DE'
GROUP BY 
    ss.store_type, ss.country_code
ORDER BY 
    total_sales DESC;
-- Task 9: How quickly is the company making sales? --
WITH full_timestamps AS (
    SELECT 
        dt.year,
        TO_TIMESTAMP(
            dt.year || '-' || dt.month || '-' || dt.day || ' ' || dt.timestamp,
            'YYYY-MM-DD HH24:MI:SS'
        ) AS sale_timestamp,
        LEAD(
            TO_TIMESTAMP(
                dt.year || '-' || dt.month || '-' || dt.day || ' ' || dt.timestamp,
                'YYYY-MM-DD HH24:MI:SS'
            )
        ) OVER (PARTITION BY dt.year ORDER BY TO_TIMESTAMP(dt.year || '-' || dt.month || '-' || dt.day || ' ' || dt.timestamp, 'YYYY-MM-DD HH24:MI:SS')) AS next_timestamp
    FROM 
        dim_date_times dt
),
time_differences AS (
    SELECT 
        year,
        EXTRACT(EPOCH FROM (next_timestamp - sale_timestamp)) AS time_diff_seconds
    FROM 
        full_timestamps
    WHERE 
        next_timestamp IS NOT NULL
),
average_time_per_year AS (
    SELECT 
        year,
        AVG(time_diff_seconds) AS avg_time_diff_seconds
    FROM 
        time_differences
    GROUP BY 
        year
)
SELECT 
    year,
    CONCAT(
        '"hours": ', FLOOR(avg_time_diff_seconds / 3600), ', ',
        '"minutes": ', FLOOR((avg_time_diff_seconds % 3600) / 60), ', ',
        '"seconds": ', FLOOR(avg_time_diff_seconds % 60), ', ',
        '"milliseconds": ', ROUND((avg_time_diff_seconds - FLOOR(avg_time_diff_seconds)) * 1000)
    ) AS actual_time_taken
FROM 
    average_time_per_year
ORDER BY 
    avg_time_diff_seconds DESC; -- Sort by average time difference in descending order