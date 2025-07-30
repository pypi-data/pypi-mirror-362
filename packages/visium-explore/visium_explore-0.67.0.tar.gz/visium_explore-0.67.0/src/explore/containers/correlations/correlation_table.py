"""Functions for displaying the correlation table of the data."""

import copy

import numpy as np
import pandas as pd
import streamlit as st

from explore.containers.correlations.mutual_info import compute_mutual_info
from explore.containers.correlations.pearson_corr import compute_pearson_corr
from explore.containers.correlations.st_explanations import st_correlation_table_explanation
from explore.utils import build_and_display_column_stats


def compute_correlation_table_container(df: pd.DataFrame, target_feature: str) -> None:
    """Compute the correlation table for the selected feature.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        target_feature (str): The name of the target feature.

    Returns:
        None
    """
    discrete_feat = {col: not np.issubdtype(dtype, np.number) for col, dtype in df.dtypes.items()}
    feat_types = df.dtypes.to_frame(name="Feature Type")
    feat_types = feat_types.drop(index=target_feature)

    st.write("Target feature statistics:")
    target_stat(df[target_feature])

    # Mutual Info and Pearson Corr
    mutual_info = compute_mutual_info(df, target_feature, copy.deepcopy(discrete_feat))
    pearson_corr = compute_pearson_corr(df, target_feature, copy.deepcopy(discrete_feat))

    results_df = pd.concat([feat_types, mutual_info, pearson_corr], axis=1).sort_values(
        by="Mutual Information", ascending=False
    )

    # Display the results
    st.write("---")
    st.write("Correlation table of each feature with the selected target (ranked by descending Mutual Information):")
    st.data_editor(
        results_df,
        column_config={
            "Pairwise Null Ratio": st.column_config.ProgressColumn(
                min_value=0,
                max_value=1,
            )
        },
    )
    st_correlation_table_explanation()


def target_stat(df_target: pd.DataFrame) -> None:
    """Calculate and display statistics for a target feature.

    Args:
    df_target (pd.DataFrame): The target feature as a DataFrame.

    Returns:
    None
    """
    build_and_display_column_stats(df_target.to_frame())
