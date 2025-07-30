"""Streamlit component to display a sample of a dataframe and its schema."""

import pandas as pd
import streamlit as st


def display_sample_df_container(sample_df: pd.DataFrame) -> pd.DataFrame:
    """Display a sample of the selected dataframe."""
    sample_df = sample_df.copy()
    st.write("---")
    st.header("Sample data")
    col1, col2 = st.columns(spec=[4, 1])
    st.info(f":information_source: Sample DataFrame - {len(sample_df)} rows")
    # Streamlit does not support displaying timedelta types at the moment.
    if (sample_df.dtypes == "timedelta64[ns]").any():
        td_cols = sample_df.dtypes.index[sample_df.dtypes == "timedelta64[ns]"]
        for col in td_cols:
            sample_df[col] = sample_df[col].dt.total_seconds()
    columns_with_types = [f"{col} [{str(sample_df[col].dtype)}]" for col in sample_df.columns]

    sample_df.columns = columns_with_types
    st.write(sample_df)
