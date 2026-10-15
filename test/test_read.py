import pandas as pd
from reader import read_flavours, read_sales, read_stores

def test_read_flavours():
    result = read_flavours()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty