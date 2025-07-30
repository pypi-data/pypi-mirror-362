import pandas as pd


def fill_missing_num_cols(df, strategy="mean"):
    for col in df.select_dtypes(include="number").columns:
        if strategy == "mean":
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == "median":
            df[col] = df[col].fillna(df[col].median())
        else:
            raise ValueError("Unsupported strategy")
    return df
