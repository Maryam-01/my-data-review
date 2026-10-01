
\c de_review_etl


\copy dim_date FROM 'star_schema/dim_date.csv' CSV HEADER;
\copy dim_store FROM 'star_schema/dim_store.csv' CSV HEADER;
\copy dim_flavour FROM 'star_schema/dim_flavour.csv' CSV HEADER;
\copy fact_sales FROM 'star_schema/fact_sales.csv' CSV HEADER;