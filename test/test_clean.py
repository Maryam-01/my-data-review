from clean import clean_flavours, clean_sales,clean_prices_in_sales, clean_stores_strip_store_name, clean_stores_strip_region
import pandas as pd
from reader import read_flavours, read_sales, read_stores






def  test_clean_flavours_converts_booleans():
    
    flavours = pd.DataFrame({
        "contains_nuts": [
            "Y", "YES", "TRUE", "1", 
            "N", "NO", "FALSE", "0"
        ]
    })

    result = clean_flavours(flavours)
    assert result["contains_nuts"].tolist() == [
        True, True, True, True, False, False, False, False
    ]


def test_converts_datetime_to_pd_format():
    sales = pd.DataFrame({
        "timestamp": [
            "06/01/2024 11:47:08"
        ]
    })

    result = clean_sales(sales)
    assert result["timestamp"].tolist() == [
       pd.Timestamp("2024-01-06 11:47:08")

    ]

def test_removes_invalid_datetime():
    sales = pd.DataFrame({
        "timestamp": [
            "na", "not a date"
        ]

    })

    result = clean_sales(sales)
    assert result.empty

def test_na_prices_dropped():
    sales = pd.DataFrame({"price_in_pence": [
                              100,
                              200,
                              "na"
                          ]
                          })
    result = clean_prices_in_sales(sales)
    assert result["price_in_pence"].tolist() == [
       100, 200
    ]

def test_na_prices_dropped():
    sales = pd.DataFrame({"price_in_pence": [
                              100,
                              200,
                              "na"
                          ]
                          })
    result = clean_prices_in_sales(sales)
    assert result["price_in_pence"].tolist() == [
       100, 200
    ]

def test_negative_prices_dropped():
    sales = pd.DataFrame({"price_in_pence": [
                              100,
                              200,
                              -1
                          ]
                          })
    result = clean_prices_in_sales(sales)
    assert result["price_in_pence"].tolist() == [
       100, 200
    ]

def test_store_name_white_space_stripped():
    stores = pd.DataFrame({"store_name": [
                              " McDonald's ",
                              "  Tesco   ",
                              "  Sainsbury's  "
                          ]
                          })
    result = clean_stores_strip_store_name(stores)
    assert result["store_name"].tolist() == [
       "mcdonald's", "tesco", "sainsbury's"
    ]

def test_region_white_space_stripped():
    stores = pd.DataFrame({"region":
        [
            " Oxford Street  ",
            " Leicester SQuare  ",
            " Picadilly Circus "
        ]
    })
    result = clean_stores_strip_region(stores)
    assert result["region"].tolist() == [
        "oxford street",
        "leicester square",
        "picadilly circus"
    ]

    

    
