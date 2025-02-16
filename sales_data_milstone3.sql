-- Use this part of the code to verify column_name, data_type after each task
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'orders_table'; -- Change this as necessary

SELECT COUNT(card_number)
FROM dim_card_details;
SELECT COUNT(card_number)
FROM orders_table;

-- Commented ones are not tested, non commented ones works
----------------
-- Milestone 3--
----------------

------ Task 3 ------
-- Merge Latitude Columns
-- UPDATE dim_store_details 
-- SET latitude = COALESCE(latitude, lat);
-- -- Drop the Redundant Column
-- ALTER TABLE dim_store_details
-- DROP COLUMN lat;
-- -- Update location Column
-- UPDATE dim_store_details
-- SET locality = NULL
-- WHERE locality = 'N/A';

-- -- Check the updated table columns & type
-- SELECT *
-- FROM dim_store_details;

------ Task 4 (Executed in SQL instead of .ipynb)------
-- Query to Remove £
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');
-- Add the weight_class Column
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(14);

UPDATE dim_products
SET weight_class = CASE
    WHEN weight::NUMERIC < 2 THEN 'Light'
    WHEN weight::NUMERIC >= 2 AND weight::NUMERIC < 40 THEN 'Mid_Sized'
    WHEN weight::NUMERIC >= 40 AND weight::NUMERIC < 140 THEN 'Heavy'
    WHEN weight::NUMERIC >= 140 THEN 'Truck_Required'
END;
-- -- Check the updated table columns & type
SELECT *
FROM dim_products;


------ Task 5 ------
-- Rename the 'removed' column to 'still_available'
-- ALTER TABLE dim_products
-- RENAME COLUMN removed TO still_available;

-- -- Update 'still_available' values
-- UPDATE dim_products
-- SET still_available = CASE
--     WHEN still_available = 'Still_avaliable' THEN TRUE
--     WHEN still_available = 'Removed' THEN FALSE
-- END;

-- -- Cast 'product_price' to NUMERIC
-- ALTER TABLE dim_products
-- ALTER COLUMN product_price TYPE NUMERIC
-- USING product_price::NUMERIC;

-- -- Cast 'weight' to NUMERIC
-- ALTER TABLE dim_products
-- ALTER COLUMN weight TYPE NUMERIC
-- USING weight::NUMERIC;

-- -- Cast 'EAN' to VARCHAR with appropriate length
-- ALTER TABLE dim_products
-- ALTER COLUMN EAN TYPE VARCHAR(17);  -- Replace 17 with the actual max length

-- -- Cast 'product_code' to VARCHAR with appropriate length
-- ALTER TABLE dim_products
-- ALTER COLUMN product_code TYPE VARCHAR(11);  -- Replace 11 with the actual max length

-- -- Cast 'date_added' to DATE
-- ALTER TABLE dim_products
-- ALTER COLUMN date_added TYPE DATE
-- USING date_added::DATE;

-- -- Cast 'uuid' to UUID
-- ALTER TABLE dim_products
-- ALTER COLUMN uuid TYPE UUID
-- USING uuid::UUID;

-- -- Cast 'still_available' to BOOLEAN
-- ALTER TABLE dim_products
-- ALTER COLUMN still_available TYPE BOOLEAN
-- USING still_available::BOOLEAN;

-- -- Cast 'weight_class' to VARCHAR with appropriate length
-- ALTER TABLE dim_products
-- ALTER COLUMN weight_class TYPE VARCHAR(14);  -- Replace 14 with the actual max length

------ Task 6 ------
-- Step 1: Calculate maximum lengths for VARCHAR columns
-- DO $$
-- DECLARE
--     max_month_length INT;
--     max_year_length INT;
--     max_day_length INT;
--     max_time_period_length INT;
-- BEGIN
--     -- Calculate maximum lengths
--     SELECT MAX(LENGTH(month::TEXT)) INTO max_month_length FROM dim_date_times;
--     SELECT MAX(LENGTH(year::TEXT)) INTO max_year_length FROM dim_date_times;
--     SELECT MAX(LENGTH(day::TEXT)) INTO max_day_length FROM dim_date_times;
--     SELECT MAX(LENGTH(time_period::TEXT)) INTO max_time_period_length FROM dim_date_times;

--     -- Step 2: Cast columns to correct data types
--     EXECUTE 'ALTER TABLE dim_date_times
--              ALTER COLUMN month TYPE VARCHAR(' || max_month_length || '),
--              ALTER COLUMN year TYPE VARCHAR(' || max_year_length || '),
--              ALTER COLUMN day TYPE VARCHAR(' || max_day_length || '),
--              ALTER COLUMN time_period TYPE VARCHAR(' || max_time_period_length || '),
--              ALTER COLUMN date_uuid TYPE UUID;';
-- END $$;

------ Task 7 ------
-- Step 1: Calculate maximum lengths for VARCHAR columns
-- DO $$
-- DECLARE
--     max_card_number_length INT;
--     max_expiry_date_length INT;
-- BEGIN
--     -- Calculate maximum lengths
--     SELECT MAX(LENGTH(card_number::TEXT)) INTO max_card_number_length FROM dim_card_details;
--     SELECT MAX(LENGTH(expiry_date::TEXT)) INTO max_expiry_date_length FROM dim_card_details;

--     -- Step 2: Cast columns to correct data types
--     EXECUTE 'ALTER TABLE dim_card_details
--              ALTER COLUMN card_number TYPE VARCHAR(' || max_card_number_length || '),
--              ALTER COLUMN expiry_date TYPE VARCHAR(' || max_expiry_date_length || '),
--              ALTER COLUMN date_payment_confirmed TYPE DATE;';
-- END $$;

------ Task 8 (Executed in SQL instead of .ipynb) ------
-- Step 1: Add primary key to dim_users
ALTER TABLE dim_users
ADD PRIMARY KEY (user_uuid);

-- Step 2: Add primary key to dim_store_details
ALTER TABLE dim_store_details
ADD PRIMARY KEY (store_code);

-- Step 3: Add primary key to dim_products
ALTER TABLE dim_products
ADD PRIMARY KEY (product_code);

-- Step 4: Add primary key to dim_date_times
ALTER TABLE dim_date_times
ADD PRIMARY KEY (date_uuid);

-- Step 5: Add primary key to dim_card_details
ALTER TABLE dim_card_details
ADD PRIMARY KEY (card_number);

-- Check primary keys in dim_users
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dim_users' AND column_name = 'user_uuid';

-- Check primary keys in dim_store_details
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dim_store_details' AND column_name = 'store_code';

-- Check primary keys in dim_products
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dim_products' AND column_name = 'product_code';

-- Check primary keys in dim_date_times
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dim_date_times' AND column_name = 'date_uuid';

-- Check primary keys in dim_card_details
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'dim_card_details' AND column_name = 'card_number';

------ Task 9 (Executed in SQL instead of .ipynb) ------
-- Step 1: Add foreign key to dim_users
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users (user_uuid);

-- Step 2: Add foreign key to dim_store_details
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_store_code
FOREIGN KEY (store_code)
REFERENCES dim_store_details (store_code);

-- Step 3: Add foreign key to dim_products
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_product_code
FOREIGN KEY (product_code)
REFERENCES dim_products (product_code);

-- Step 4: Add foreign key to dim_date_times
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_date_uuid
FOREIGN KEY (date_uuid)
REFERENCES dim_date_times (date_uuid);

-- Step 5: Add foreign key to dim_card_details
ALTER TABLE orders_table
ADD CONSTRAINT fk_orders_card_number
FOREIGN KEY (card_number)
REFERENCES dim_card_details (card_number);

-- Check foreign keys in orders_table
SELECT conname AS constraint_name,
       conrelid::regclass AS table_name,
       a.attname AS column_name,
       confrelid::regclass AS referenced_table,
       af.attname AS referenced_column
FROM pg_constraint
JOIN pg_attribute a ON a.attnum = ANY (conkey) AND a.attrelid = conrelid
JOIN pg_attribute af ON af.attnum = ANY (confkey) AND af.attrelid = confrelid
WHERE conrelid = 'orders_table'::regclass;

