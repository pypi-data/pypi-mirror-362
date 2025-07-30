import pandas as pd
from dsutilbox.preprocessing import fill_missing


def test_fill_missing():
    df = pd.DataFrame({'a': [1, None, 3]})
    filled = fill_missing(df)
    assert not filled.isnull().any().any()
