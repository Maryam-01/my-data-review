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

    