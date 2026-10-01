DROP DATABASE IF EXISTS de_review_etl;
CREATE DATABASE IF EXISTS de_review_etl;

\c de_review_etl;



CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    day INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT,
    day_of_week VARCHAR(20),
    is_weekend BOOLEAN
);

CREATE TABLE dim_store (
    store_id VARCHAR(10) PRIMARY KEY,
    store_name VARCHAR(50),
    region VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE dim_flavour (
    flavour_id INT PRIMARY KEY,
    flavour_name VARCHAR(50),
    contains_nuts BOOLEAN,
    cost_price_in_pence INT
);

CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_id INT NOT NULL,
    store_id VARCHAR(10) NOT NULL,
    flavour_id INT NOT NULL,
    price_in_pence INT NOT NULL,

    FOREIGN KEY (store_id) REFERENCES dim_store(store_id),
    FOREIGN KEY (flavour_id) REFERENCES dim_flavour(flavour_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);