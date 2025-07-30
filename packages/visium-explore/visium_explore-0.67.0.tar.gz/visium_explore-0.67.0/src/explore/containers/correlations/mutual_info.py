"""Compute mutual information between features and target variable."""

import pandas as pd
import streamlit as st
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

import explore.containers.correlations.constants as constants


@st.cache_data
def compute_mutual_info(df: pd.DataFrame, target_feature: str, discrete_feat: dict) -> pd.DataFrame:
    """Compute the mutual information and pairwise null ratio between each feature in the DataFrame and the target feature. Track the process evolution with a progress bar.

    Args:
        df (pd.DataFrame): The input DataFrame containing the features and the target feature.
        target_feature (str): The name of the target feature.
        discrete_feat (dict): A dictionary indicating whether each feature is discrete or continuous.

    Returns:
        pd.DataFrame: A DataFrame containing the pairwise null ratio and mutual information for each feature.

    """
    features = df.drop(columns=[target_feature])
    discrete_target = discrete_feat[target_feature]
    discrete_feat.pop(target_feature)

    results_df = pd.DataFrame(index=features.columns, columns=["Pairwise Null Ratio", "Mutual Information"])

    # Initialize the progress bar
    progress_text = "Computing Mutual Information. Operation in progress. Please wait."
    progress_bar = st.progress(0, text=progress_text)
    num_features = len(features.columns)

    for idx, col in enumerate(features.columns):
        temp_df = pd.concat(
            [features[col], df[target_feature]], axis=1
        )  # Create a temporary DataFrame with the current feature and the target feature
        results_df.loc[col, "Pairwise Null Ratio"] = compute_pairwise_null_ratio(temp_df)
        temp_df = temp_df.dropna()

        results_df.at[col, "Mutual Information"] = compute_mutual_info_for_feature(
            temp_df, col, target_feature, discrete_feat[col], discrete_target
        )
        # Update the progress bar
        progress_bar.progress(((idx + 1) / num_features), text=progress_text)

    # Emptry the progress bar
    progress_bar.progress(100)
    progress_bar.empty()

    return results_df


def encode_categorical_feature(feature: pd.DataFrame) -> pd.DataFrame:
    """Encode a categorical feature using pandas Categorical codes.

    Args:
        feature (pd.DataFrame): The categorical feature to be encoded.

    Returns:
        pd.DataFrame: The encoded feature as a pandas DataFrame.
    """
    return pd.Categorical(feature).codes


def compute_pairwise_null_ratio(df: pd.DataFrame) -> float:
    """Computes the ratio of rows in the given DataFrame that contain at least one null value.

    Args:
    - temp_df (pd.DataFrame): The DataFrame to compute the null ratio for.

    Returns:
    - float: The ratio of rows with null values, rounded to 4 decimal places.
    """
    return round(df.isnull().any(axis=1).mean(), 4)


def compute_mutual_info_for_feature(
    df: pd.DataFrame, feature: str, target_feature: str, discrete_feat: bool, discrete_target: bool
) -> float:
    """Compute the mutual information between a feature and a target feature in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        feature (str): The name of the feature for which to compute the mutual information.
        target_feature (str): The name of the target feature.
        discrete_feat (dict): A dictionary mapping feature names to boolean values indicating whether they are discrete or not.
        discrete_target (bool): A boolean value indicating whether the target feature is discrete or not.

    Returns:
        float: The computed mutual information between the feature and the target feature, rounded to 4 decimal places.
    """
    if (
        len(df) <= 3
    ):  # Ensure there is enough data to compute the numerical approximation using k-nearest neighbors with k = 3
        return None
    else:
        if discrete_feat:
            df.loc[:, feature] = encode_categorical_feature(df[feature])

        if discrete_target:
            if is_computable(df, target_feature):
                mi = mutual_info_classif(
                    df[[feature]],
                    df[target_feature],
                    discrete_features=discrete_feat,
                    random_state=constants.RANDOM_STATE,
                )[0]
                return round(mi, 4)
            else:
                return None
        else:
            if discrete_feat and not is_computable(df, feature):
                return None
            else:
                mi = mutual_info_regression(
                    df[[feature]],
                    df[target_feature],
                    discrete_features=discrete_feat,
                    random_state=constants.RANDOM_STATE,
                )[0]
                return round(mi, 4)


def is_computable(df: pd.DataFrame, col: str) -> bool:
    """Check if the column contains enough information to compute correlation coefficients. This includes having only null values or only unique values for categorical variables.

    Args:
    - df (pd.DataFrame): The DataFrame containing the column to check.
    - col (str): The name of the column to check.

    Returns:
    - bool: True if the target feature contains enough information, False otherwise.
    """
    if df[col].isnull().all() or all(df[col].value_counts() == 1):
        # st.warning("The target feature does not contain enough information, mutual information is not computable.")
        return False
    return True
