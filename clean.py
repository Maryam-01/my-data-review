import pandas as pd
from reader import read_flavours, read_sales, read_stores

def clean_flavours(flavours):
    flavours_cleaned = flavours.copy()
    original_row_count = len(flavours_cleaned)

    boolean_map = {
        "Y": True,
        "YES": True,
        "TRUE": True,
        "1": True,
        "N": False,
        "NO": False,
        "FALSE": False,
        "0": False
    }
    invalid_boolean_values = (flavours_cleaned["contains_nuts"].isna().sum())
    final_row_count = len(flavours_cleaned)
    flavours_cleaned["contains_nuts"] = (
        flavours_cleaned["contains_nuts"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map(boolean_map)
        .astype("boolean")
    )

    print("FLAVOURS CLEANING SUMMARY")
    print("-------------------------")
    print(f"Original rows: {original_row_count}")
    print(f"Invalid contains_nuts values: {invalid_boolean_values}")
    print(f"Final rows: {final_row_count}")

    return flavours_cleaned

    
flavours = read_flavours()
flavours_cleaned = clean_flavours(flavours)

print(flavours.head())           # original unchanged
print(flavours_cleaned.head())   # cleaned version

print(flavours_cleaned.dtypes)

def clean_sales(sales):
    sales_cleaned = sales.copy()
    original_row_count = len(sales_cleaned)

    sales_cleaned["timestamp"] = pd.to_datetime(
        sales_cleaned["timestamp"],
        errors="coerce", # turns invalid or unparsable dates into NaT rather than raising an error
        dayfirst=True # day/month/year format
    )
    invalid_timestamps = sales_cleaned["timestamp"].isna().sum()
    sales_cleaned = sales_cleaned.dropna(subset=["timestamp"])
    print(f"Original rows: {original_row_count}")

    print(f"Invalid timestamps coerced to NaT: {invalid_timestamps}")
    return sales_cleaned

def clean_prices_in_sales(sales_cleaned):

    sales_cleaned["price_in_pence"] = pd.to_numeric(
        sales_cleaned["price_in_pence"],
        errors="coerce"
    )
    invalid_prices = sales_cleaned["price_in_pence"].isna().sum()
    sales_cleaned = sales_cleaned.dropna(subset=["price_in_pence"])
    negative_prices = (sales_cleaned["price_in_pence"] < 0).sum()

    sales_cleaned = sales_cleaned[
        sales_cleaned["price_in_pence"] >= 0
    ]

    final_row_count = len(sales_cleaned)

    # ---- Report ----
    print("SALES CLEANING SUMMARY")
    print("----------------")
    print(f"Invalid prices coerced to NaN: {invalid_prices}")
    print(f"Negative prices removed: {negative_prices}")
    print(f"Final rows: {final_row_count}")

    return sales_cleaned


sales = read_sales()
sales_cleaned = clean_sales(sales)
print(sales_cleaned.head())

def clean_stores_strip_store_name(stores):
    cleaned_stores = stores.copy()
    original_number_of_rows = len(cleaned_stores)
    cleaned_stores["store_name"] = (cleaned_stores["store_name"]
    .str.strip()
    .str.lower()
    )
    cleaned_stores["store_name"] = (cleaned_stores["store_name"]
                                    .str.replace("Center", "Centre", regex = False)
    )
    print(f"Original rows: {original_number_of_rows}")
    return cleaned_stores

def clean_stores_strip_region(cleaned_stores):

    cleaned_stores["region"] = (cleaned_stores["region"]
    .str.strip()
    .str.lower()
    )


    rows_after_cleaning = len(cleaned_stores)
    print("STORES CLEANING SUMMARY")
    print("------------------------")
    
    print(f"rows_after_cleaning: {rows_after_cleaning}")

    return cleaned_stores

stores = read_stores()
# cleaned_stores = clean_stores(stores)