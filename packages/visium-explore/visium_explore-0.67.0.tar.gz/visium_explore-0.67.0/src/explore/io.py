"""General Input/Output utilities for the explore module."""

import pathlib

import pandas as pd
import pyarrow
import streamlit as st
from pyarrow.parquet import ParquetFile


def read_df_top_rows(file_path: pathlib.Path, nrows: int) -> pd.DataFrame:
    """Read top nrows rows of a DataFrame in a memory efficient manner, using pyarrow."""
    pf = ParquetFile(file_path)
    first_rows = next(pf.iter_batches(batch_size=nrows))
    df = pyarrow.Table.from_batches([first_rows]).to_pandas()

    return df


@st.cache_data
def read_df(file_path: pathlib.Path) -> pd.DataFrame:
    """Read a DataFrame from a parquet file and cache the result if run in Streamlit."""
    return pd.read_parquet(file_path)
