"""Container displaying stats for the columns of the selected DataFrame."""

import pathlib

import numpy as np
import pandas as pd
import streamlit as st

from explore.io import read_df
from explore.utils import build_and_display_column_stats


def columns_stats_container(file_path: pathlib.Path) -> None:
    st.write("---")
    st.header("Columns statistics")
    df = read_df(file_path)

    col1, col2 = st.columns([1, 1])

    with col1:
        df_numeric = df.select_dtypes(include=[np.number])
        st.write("### Numeric columns")
        build_and_display_column_stats(df_numeric)

    with col2:
        df_object = df.select_dtypes(include=[object])
        st.write("### Object columns")
        build_and_display_column_stats(df_object)
