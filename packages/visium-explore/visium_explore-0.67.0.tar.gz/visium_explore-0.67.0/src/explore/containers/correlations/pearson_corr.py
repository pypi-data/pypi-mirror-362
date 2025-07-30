"""Compute the Pearson correlation coefficient."""

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def compute_pearson_corr(df: pd.DataFrame, target_feature: str, discrete_feat: dict) -> pd.DataFrame:
    """Compute the Pearson correlation coefficient between all features and the target variable. Track the process evolution with a progress bar.

    Args:
        df (pd.DataFrame): The input DataFrame containing the features and target variable.
        target_feature (str): The name of the target variable.
        discrete_feat (dict): A dictionary indicating whether each feature is discrete or not (key:string, value:bool).

    Returns:
        pd.DataFrame: A DataFrame containing the Pearson correlation coefficients between each features and the target variable.
    """
    features = df.drop(columns=[target_feature])
    discrete_target = discrete_feat[target_feature]
    discrete_feat.pop(target_feature)

    results_df = pd.DataFrame(index=features.columns, columns=["Pearson Correlation"])

    if not discrete_target:
        corr_pearson = df.corr(method="pearson", numeric_only=True)
        # Initialize the progress bar
        progress_text = "Computing Pearson Correlation. Operation in progress. Please wait."
        progress_bar = st.progress(0, text=progress_text)
        num_features = len(features.columns)

        for idx, col in enumerate(features.columns):
            if not discrete_feat[col] and col in corr_pearson.columns:
                results_df.at[col, "Pearson Correlation"] = round(corr_pearson[target_feature][col], 4)
            else:
                results_df.at[col, "Pearson Correlation"] = np.nan

            # Update the progress bar
            progress_bar.progress(((idx + 1) / num_features), text=progress_text)

        progress_bar.empty()
    else:
        results_df["Pearson Correlation"] = np.nan
        st.warning("The target feature is discrete. Pearson correlation is not applicable.")

    return results_df
