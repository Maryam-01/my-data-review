import pandas as pd
import os

def read_flavours():
    try:
        flavours = pd.read_csv("raw_data/flavours.csv")
        if flavours.empty:
            print("file is empty")
        else:
            return flavours
    except FileNotFoundError:
        print('CSV file not found')


print(read_flavours())




def read_sales():
    try:
        sales = pd.read_csv("raw_data/sales.csv")
        if sales.empty:
            print('file is empty')
        else:

            return sales
    except FileNotFoundError:
        print("csv is not found")
print(read_sales())

def read_stores():
    try:

        stores = pd.read_csv("raw_data/stores.csv")
        if stores.empty:
            print("file is empty")
        else:
            return stores
    except FileNotFoundError:
        print("csv is not found")
print(read_stores())

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
        errors="coerce",
        dayfirst=True
    )
    invalid_timestamps = sales_cleaned["timestamp"].isna().sum()

    sales_cleaned["price_in_pence"] = pd.to_numeric(
        sales_cleaned["price_in_pence"],
        errors="coerce"
    )
    invalid_prices = sales_cleaned["price_in_pence"].isna().sum()

    negative_prices = (sales_cleaned["price_in_pence"] < 0).sum()

    sales_cleaned = sales_cleaned[
        sales_cleaned["price_in_pence"] >= 0
    ]

    final_row_count = len(sales_cleaned)

    # ---- Report ----
    print("SALES CLEANING SUMMARY")
    print("----------------")
    print(f"Original rows: {original_row_count}")
    print(f"Invalid timestamps coerced to NaT: {invalid_timestamps}")
    print(f"Invalid prices coerced to NaN: {invalid_prices}")
    print(f"Negative prices removed: {negative_prices}")
    print(f"Final rows: {final_row_count}")

    return sales_cleaned


sales = read_sales()
sales_cleaned = clean_sales(sales)
print(sales_cleaned.head())

def clean_stores(stores):
    cleaned_stores = stores.copy()
    original_number_of_rows = len(cleaned_stores)
    cleaned_stores["store_name"] = (cleaned_stores["store_name"]
    .str.strip()
    .str.lower()
    )

    cleaned_stores["region"] = (cleaned_stores["region"]
    .str.strip()
    .str.lower()
    )

    cleaned_stores["store_name"] = (cleaned_stores["store_name"]
                                    .str.replace("Center", "Centre", regex = False)
    )
    rows_after_cleaning = len(cleaned_stores)
    print("STORES CLEANING SUMMARY")
    print("------------------------")
    print(f"Original rows: {original_number_of_rows}")
    print(f"rows_after_cleaning: {rows_after_cleaning}")

    return cleaned_stores
stores = read_stores()
cleaned_stores = clean_stores(stores)


def save_cleaned_flavours(cleaned_flavours):
    os.makedirs("cleaned_data", exist_ok = True)
    cleaned_flavours.to_csv("cleaned_data/cleaned_flavours.csv", index = False)
    print("cleaned flavours saved successfully")
cleaned_flavours = clean_flavours(flavours)
save_cleaned_flavours(cleaned_flavours)

def save_cleaned_sales(cleaned_sales):
    os.makedirs("cleaned_data", exist_ok = True)
    cleaned_sales.to_csv("cleaned_data/cleaned_sales.csv", index = False)
    print("cleaned sales saved successfully")
cleaned_sales = clean_sales(sales)
save_cleaned_sales(cleaned_sales)

def save_cleaned_stores(cleaned_stores):
    cleaned_stores.to_csv("cleaned_data/cleaned_stores.csv", index = False)
    print("cleaned stores saved successfully")
cleaned_stores = clean_stores(stores)
save_cleaned_stores(cleaned_stores)





sales = pd.read_csv("cleaned_data/cleaned_sales.csv")
stores = pd.read_csv("cleaned_data/cleaned_stores.csv")
flavours = pd.read_csv("cleaned_data/cleaned_flavours.csv")

def generate_dim_date(sales):

    sales["timestamp"] = pd.to_datetime(sales["timestamp"])

    start_date = sales["timestamp"].min().date()
    end_date = sales["timestamp"].max().date()

    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    dim_date = pd.DataFrame({
        "full_date": date_range
    })

    dim_date["date_id"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.month_name()
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["day_of_week"] = dim_date["full_date"].dt.day_name()
    dim_date["is_weekend"] = dim_date["full_date"].dt.weekday >= 5

    # Reorder columns
    dim_date = dim_date[
        [
            "date_id",
            "full_date",
            "day",
            "month",
            "month_name",
            "quarter",
            "year",
            "day_of_week",
            "is_weekend"
        ]
    ]

    return dim_date

dim_date = generate_dim_date(sales)
dim_date.to_csv("cleaned_data/dim_date.csv", index=False)
