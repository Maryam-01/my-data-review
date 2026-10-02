
from main import read_flavours, read_sales, read_stores, clean_flavours, clean_sales, clean_stores, save_cleaned_flavours, save_cleaned_sales, save_cleaned_stores, generate_dim_store, generate_dim_flavour, generate_dim_date, generate_fact_sales, dim_date, dim_date_path, dim_flavour, dim_store
from pathlib import Path
import os

def run_etl_pipeline(output_dir):
    try:

        output_dir = Path(output_dir)

        cleaned_dir = output_dir / "cleaned"
        star_schema_dir = output_dir / "star_schema"

        cleaned_dir.mkdir(parents=True, exist_ok=True)
        star_schema_dir.mkdir(parents=True, exist_ok=True)

        flavours = read_flavours()
        sales = read_sales()
        stores = read_stores()


        cleaned_flavours = clean_flavours(flavours)
        cleaned_sales= clean_sales(sales)
        cleaned_stores = clean_stores(stores)

        

        output_dir = "cleaned_data"

        save_cleaned_flavours(cleaned_flavours, output_dir)
        save_cleaned_sales(cleaned_sales, output_dir)
        save_cleaned_stores(cleaned_stores, output_dir)


        dim_date = generate_dim_date(cleaned_sales)
        fact_sales = generate_fact_sales(cleaned_sales)
        dim_store = generate_dim_store(cleaned_stores)
        dim_flavour = generate_dim_flavour(cleaned_flavours)



        dim_date.to_csv(star_schema_dir / "dim_date.csv", index=False)
        fact_sales.to_csv(star_schema_dir / "fact_sales.csv", index=False)
        dim_store.to_csv(star_schema_dir / "dim_store.csv", index=False)
        dim_flavour.to_csv(star_schema_dir / "dim_flavour.csv", index=False)

    except Exception as e:
        print(f"error occurred:{e}")
        raise










        