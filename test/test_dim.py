import pandas as pd
from main import generate_dim_date, generate_dim_flavour, generate_dim_store, generate_fact_sales


def test_generate_dim_date():
    sales = pd.DataFrame({
        "timestamp": [
            "2024-01-05 10:00:00",
            "2024-01-07 15:30:00"
        ]
    })

    result = generate_dim_date(sales)
    assert list(result.columns) == [
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


def test_generate_dim_flavour():
    flavours_cleaned = pd.DataFrame({
        "id": [1,2,3],
        "name": ["Pistachio", "Vanilla", "Chocolate"],
        "contains_nuts": [False, True, False],
        "cost_price_in_pence": [80, 120, 10],
        "extra_column": ["ignore", "ignore", "ignore"]
        
    })

    result = generate_dim_flavour(flavours_cleaned)
    expected = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Pistachio", "Vanilla", "Chocolate"],
        "contains_nuts": [False, True, False],
        "cost_price_in_pence": [80, 120, 10]
    })

    pd.testing.assert_frame_equal(result, expected)


def test_generate_fact_sales():
    sales_cleaned = pd.DataFrame({
        "id": [1, 2],
        "timestamp": pd.to_datetime([
            "2024-01-05 10:00:00",
            "2024-12-07 15:30:00"
        ]),
        "store_id": [10, 20],
        "flavour_id": [3, 4],
        "price_in_pence": [250, 300],
        "extra_column": ["ignore", "ignore"]
    })

    result = generate_fact_sales(sales_cleaned)
        
    expected = pd.DataFrame({
        "id": [1, 2],
        "date_id": [20240105, 20241207],
        "store_id": [10, 20],
        "flavour_id": [3, 4],
        "price_in_pence": [250, 300]
    })

    pd.testing.assert_frame_equal(result, expected)

def test_generate_dim_store():
    stores = pd.DataFrame({
        "store_id": [1,2,3],
        "store_name": ["Oxford Street", "Westfield", "Manchester City Centre"],
        "region": ["London", "Shepherd's Bush", "Manchester"],
        "latitude": [51.5159, 53.4808, 52.5094],
        "longitude": [-0.1431, -2.2426, -1.8933],
        "extra_column": ["blah", "blah", "blah"]

    })
    result = generate_dim_store(stores)
    expected = pd.DataFrame({
        "store_id": [1,2,3],
        "store_name": ["Oxford Street", "Westfield", "Manchester City Centre"],
        "region": ["London", "Shepherd's Bush", "Manchester"],
        "latitude": [51.5159, 53.4808, 52.5094],
        "longitude": [-0.1431, -2.2426, -1.8933]
    })

    pd.testing.assert_frame_equal(result, expected)
