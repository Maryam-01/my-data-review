import pandas as pd
import os
import requests

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
    sales_cleaned = sales_cleaned.dropna(subset=["timestamp"])

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




def save_cleaned_flavours(cleaned_flavours, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_flavours.csv")
    cleaned_flavours.to_csv(output_path, index=False)
    print("cleaned flavours saved successfully")


def save_cleaned_sales(cleaned_sales, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_sales.csv")
    cleaned_sales.to_csv(output_path, index=False)
    print("cleaned sales saved successfully")


def save_cleaned_stores(cleaned_stores, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cleaned_stores.csv")
    cleaned_stores.to_csv(output_path, index=False)
    print("cleaned stores saved successfully")
# save_cleaned_stores(cleaned_stores)





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

dim_date = generate_dim_date(sales_cleaned)
dim_date.to_csv("star_schema/dim_date.csv", index=False)



def generate_fact_sales(sales_cleaned):
    # create date_id in sales
    sales_cleaned["date_id"] = sales_cleaned["timestamp"].dt.strftime("%Y%m%d").astype(int)

    fact_sales = sales_cleaned[[
        "id",
        "date_id",
        "store_id",
        "flavour_id",
        "price_in_pence"
    ]]
    return fact_sales
fact_sales = generate_fact_sales(sales_cleaned)
os.makedirs("star_schema", exist_ok = True)
fact_sales.to_csv("star_schema/fact_sales.csv", index= False)


def generate_dim_store(cleaned_stores):
    dim_store = cleaned_stores[[
        "store_id",
        "store_name",
        "region",
        "latitude",
        "longitude"
    ]]
    return dim_store

dim_store = generate_dim_store(cleaned_stores)
dim_store.to_csv("star_schema/dim_store.csv", index = False)



def generate_dim_flavour(flavours_cleaned):
    dim_flavour = flavours_cleaned[[
        "id",
        "name",
        "contains_nuts",
        "cost_price_in_pence"
    ]]
    return dim_flavour


flavours = read_flavours()
flavours_cleaned = clean_flavours(flavours)

dim_flavour = generate_dim_flavour(flavours_cleaned)

os.makedirs("star_schema", exist_ok=True)
dim_flavour.to_csv("star_schema/dim_flavour.csv", index=False)


years = sorted(dim_date["year"].unique())
bank_holiday_dates = set() # creates an empty python set, a set is like a list, it only stores unique values
#### Enriching with bank holidays
for year in years:
    url = f"http://18.170.47.199:8000/uk/bank-holidays/{year}"
    response = requests.get(url)
    response.raise_for_status()
    holidays = response.json() # holidays = [
#     {"date": "2024-01-01", "name": "New Year's Day"},
#     {"date": "2024-03-29", "name": "Good Friday"},
#     {"date": "2024-04-01", "name": "Easter Monday"}
# ]
    for holiday in holidays: # loops around the list of holiday dictionaries one by one
        bank_holiday_dates.add(pd.to_datetime(holiday["date"]).date()) # this gets the date from each holiday and adds it to the set, italso converts the it to pandas datetime and .date() converts it to plain date

dim_date_path = "star_schema/dim_date.csv"
dim_date["is_bank_holiday"] = dim_date["full_date"].dt.date.isin(bank_holiday_dates) # checks every date in full_date column and checks if its in bank_holiday_dates


dim_date.to_csv(dim_date_path, index=False)


def read_weather():


    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        "?latitude=52.52"
        "&longitude=13.41"
        "&start_date=2026-09-20"
        "&end_date=2026-10-04"
        "&hourly=temperature_2m,precipitation,weather_code"
        "&timezone=Europe/Berlin"
    )
    response = requests.get(url)
    response.raise_for_status()
    weather = response.json() # converts the response into a python dictionary
    weathers = pd.DataFrame({"datetime": weather["hourly"]["time"],
                            "temperature_c": weather["hourly"]["temperature_2m"],
                             "precipitation_mm": weather["hourly"]["precipitation"], 
                            "weather_code": weather["hourly"]["weather_code"] 
                            })
    
    return weathers

df = read_weather()
print(df)

weather_code_map = {
	0: "Clear sky",
	1: "Mainly clear",
	2: "Partly cloudy",
	3: "Overcast",
	45: "Fog",
	48: "Depositing rime fog",
	51: "Light drizzle",
	53: "Moderate drizzle",
	55: "Dense drizzle",
	56: "Light freezing drizzle",
	57: "Dense freezing drizzle",
	61: "Slight rain",
	63: "Moderate rain",
	65: "Heavy rain",
	66: "Light freezing rain",
	67: "Heavy freezing rain",
	71: "Slight snowfall",
	73: "Moderate snowfall",
	75: "Heavy snowfall",
	77: "Snow grains",
	80: "Slight rain showers",
	81: "Moderate rain showers",
	82: "Violent rain showers",
	85: "Slight snow showers",
	86: "Heavy snow showers",
	95: "Thunderstorm",
	96: "Thunderstorm with slight hail",
	97: "Heavy thunderstorm",
	99: "Thunderstorm with heavy hail"
}

df["weather_code"] = df["weather_code"].map(weather_code_map)
print(df)

df = df.copy()
df["date_id"] = (
    pd.to_datetime(df["datetime"])
    .dt.strftime("%Y%m%d")
    .astype(int)
)

sales_keys = fact_sales[["date_id", "store_id"]].drop_duplicates()

df = df.rename(columns={
    "temperature_c": "temp_celsius",
    "precipitation_mm": "rainfall_mm",
    "weather_code": "weather_condition"
})
                        
df = df.merge(
    sales_keys, 
    on="date_id",
    how="inner"
)
                        



def generate_fact_weather(df):
    fact_weather = df[[
        "date_id",
        "store_id",
        "temp_celsius",
        "rainfall_mm",
        "weather_condition"
    ]]
    return fact_weather

fact_weather = generate_fact_weather(df)
fact_weather.to_csv("star_schema/fact_weather.csv", index = False)