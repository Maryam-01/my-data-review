from clean import clean_flavours, clean_sales,clean_stores
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
