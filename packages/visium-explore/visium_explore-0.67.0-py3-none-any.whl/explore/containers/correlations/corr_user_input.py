"""User input forms for the correlation analysis."""

import streamlit as st

from explore.containers.correlations.st_explanations import st_UMAP_disclaimer


def user_inputs_corr_matrix(dvc_step_key: str, columns: list[str]) -> tuple[bool, list[str]]:
    """Display the user inputs form and return the submitted values for correlation matrix.

    Args:
        dvc_step_key (str): The key for the DVC step.
        columns (list[str]): The list of column names.

    Returns:
        tuple[bool, list[str]]: A tuple containing a boolean value indicating whether the form was submitted
        and a list of selected features for the correlation matrix.
    """
    st.subheader("Correlation matrix (𝜙k  coefficient).")
    form = st.form(key=f"corr_matrix_form_{dvc_step_key}", border=False)
    with form:
        options = sorted(columns)
        corr_matrix_fields = st.multiselect(
            "Select the features of interest:",
            options=options,
            default=[],
            key=f"y_corr_cols_{dvc_step_key}",
        )

    # submit the form
    submitted = form.form_submit_button(label="Execute")

    return submitted, corr_matrix_fields


def user_input_corr_table(dvc_step_key: str, columns: list[str]) -> tuple[bool, str]:
    """Display the user inputs form and return the submitted values for correlation table.

    Args:
    - dvc_step_key (str): The key for the DVC step.
    - columns (list[str]): The list of column names.

    Returns:
    - tuple[bool, str]: A tuple containing a boolean value indicating whether the form was submitted and the user-selected feature for the correlation table.
    """
    st.subheader("Ranked correlation table for input feature (Pearson  coefficient and Mutual Information).")
    form = st.form(key=f"corr_table_form_{dvc_step_key}", border=False)
    with form:
        options = sorted(columns)
        selected_feature = st.selectbox(
            "Select a feature to explore its correlation coefficients with all other variables.",
            options=options,
            index=0,
            key=f"y_corr_col_{dvc_step_key}",
        )

    # submit the form
    submitted = form.form_submit_button(label="Execute")

    return submitted, selected_feature


def user_input_umap(dvc_step_key: str, columns: list[str]) -> tuple[bool, str, int]:
    """Display the user inputs form for UMAP visualization.

    Args:
    - dvc_step_key (str): The key for the DVC step.
    - columns (list[str]): The list of column names.

    Returns:
    - tuple[bool, str, int]: A tuple containing a boolean value indicating whether the form was submitted and the user-selected feature to color
    the data points on the plot and an int indicating the number of dimensions to reduce the dataset to.
    """
    st.subheader("UMAP visualization")
    st_UMAP_disclaimer()
    form = st.form(key=f"umap_form_{dvc_step_key}", border=False)
    with form:
        options = [None] + sorted(columns)
        selected_feature = st.selectbox(
            "Optional: Select a feature to color the data points in the low-dimensional space.",
            options=options,
            index=None,
            key=f"umap_form_{dvc_step_key}",
        )
    with form:
        n_dim = option = st.radio("Choose a number of dimensions:", ("2D", "3D"))
        if n_dim == "2D":
            n_components = 2
        else:
            n_components = 3

    with form:
        efficiency_vs_reproducibility = option = st.radio(
            "Reproducibility of results and Parallelization of process for better efficiency (computation using all available cores) are mutually exclusive. Choose your preference:",
            ("Reproducibility of results", "Parallelization of process"),
        )
    submitted = form.form_submit_button(label="Execute")

    return submitted, selected_feature, n_components, efficiency_vs_reproducibility
