"""Functions for displaying the correlation matrix of the data."""

import pandas as pd
import plotly.express as px
import streamlit as st
from phik import phik_matrix

from explore.containers.correlations.st_explanations import st_correlation_matrix_explanation


@st.cache_data
def correlation_matrix_output_container(df: pd.DataFrame, corr_matrix_fields: list[str]) -> None:
    """Display the 𝜙k correlation matrix for the user-selected fields.

    Args:
        file_path (pathlib.Path): The path to the file containing the data.
        corr_matrix_fields (list[str]): The list of fields to include in the correlation matrix.

    Returns:
        None
    """
    temp_df = df[corr_matrix_fields]
    correlations = temp_df.phik_matrix(verbose=False, dropna=True)

    # Plotly heatmap of the correlations
    fig = px.imshow(correlations)
    fig.update_layout()
    st.write("Correlation matrix computed with the 𝜙k correlation coefficient.")
    st.plotly_chart(fig)
    st_correlation_matrix_explanation
