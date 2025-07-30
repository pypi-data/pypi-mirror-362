import pandas as pd
from dsutilbox.preprocessing import fill_missing_num_cols


def test_fill_missing_num_cols():
    df = pd.DataFrame({'a': [1, None, 3]})
    filled = fill_missing_num_cols(df)
    assert not filled.isnull().any().any()
