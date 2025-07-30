"""Streamlit container to study correlations between features."""

import pathlib

import pandas as pd
import streamlit as st

from explore.containers.correlations.corr_user_input import (
    user_input_corr_table,
    user_input_umap,
    user_inputs_corr_matrix,
)
from explore.containers.correlations.correlation_matrix import correlation_matrix_output_container
from explore.containers.correlations.correlation_table import compute_correlation_table_container
from explore.containers.correlations.st_explanations import st_correlation_matrix_phik_disclaimer
from explore.containers.correlations.umap import plot_umap
from explore.io import read_df


def correlation_container(file_path: pathlib.Path, dvc_step_key: str, schema_dict: dict[str, str]) -> None:
    """Display the correlation container.

    Args:
        file_path (pathlib.Path): The path to the file.
        dvc_step_key (str): The DVC step key.
        schema_dict (dict[str, str]): A dictionary containing the schema information.

    Returns:
        None
    """
    st.write("---")
    st.header("Correlation study")

    # Initialize session states for button clicks
    if "corr_matrix_button_clicked" not in st.session_state:
        st.session_state.corr_matrix_button_clicked = False

    if "ranked_corr_button_clicked" not in st.session_state:
        st.session_state.ranked_corr_button_clicked = False

    if "umap_button_clicked" not in st.session_state:
        st.session_state.umap_button_clicked = False

    selectable_columns = [col for col, _ in schema_dict.items()]
    # filtered_df = filter(file_path, selectable_columns)
    df = read_df(file_path)
    df = df.loc[:, selectable_columns]

    with st.container(border=True):
        submitted, feature = user_input_corr_table(dvc_step_key, columns=selectable_columns)

        if submitted:
            st.session_state.selected_feature = feature
            st.session_state.ranked_corr_button_clicked = True  # Set the state to True when the button is clicked

        # Only display the table if the button has been clicked
        if st.session_state.ranked_corr_button_clicked:
            compute_correlation_table_container(df, st.session_state.selected_feature)

    st.write("---")
    with st.container(border=True):
        submitted, corr_matrix_fields = user_inputs_corr_matrix(dvc_step_key, columns=selectable_columns)
        st_correlation_matrix_phik_disclaimer()

        if submitted:
            st.session_state.corr_matrix_fields = corr_matrix_fields
            st.session_state.corr_matrix_button_clicked = True  # Set the state to True when the button is clicked

        # Only display the matrix if the button has been clicked
        if st.session_state.corr_matrix_button_clicked:
            correlation_matrix_output_container(df, st.session_state.corr_matrix_fields)

    st.write("---")
    with st.container(border=True):
        submitted, feature_color, dimensions, e_vs_r = user_input_umap(dvc_step_key, columns=selectable_columns)

        if submitted:
            st.session_state.umap_button_clicked = True  # Set the state to True when the button is clicked

        # Only display the matrix if the button has been clicked
        if st.session_state.umap_button_clicked:
            plot_umap(df, feature_color, dimensions, e_vs_r)
