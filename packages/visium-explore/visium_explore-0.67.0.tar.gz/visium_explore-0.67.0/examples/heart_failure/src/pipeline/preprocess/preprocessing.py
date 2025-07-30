"""Module for preprocessing."""

from pathlib import Path

import numpy as np
import pandas as pd
import typer
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler

from src.pipeline.preprocess.constants import PreprocessConstants
from src.pipeline.preprocess.io import load_pickle, load_splits, save_pickle
from src.pipeline.split.constants import SplitConstants
from src.pipeline.split.io import load_parquet_data, save_split_data


def train_and_save_scaler(train_set: pd.DataFrame, numerical_features: list, scaler_path: Path) -> StandardScaler:
    """Train the scaler using the provided training set and numerical features, and save it.

    Args:
        train_set (pd.DataFrame): The training set used to train the scaler.
        numerical_features (list): A list of numerical features used for scaling.
        scaler_path (Path): The path where the scaler will be saved.

    Returns:
        StandardScaler: The trained scaler object.
    """
    scaler = StandardScaler()
    scaler.fit(train_set[numerical_features])
    save_pickle(scaler, scaler_path)
    return scaler


def compute_and_save_gaussian(df: pd.DataFrame, columns: list[str], output_folder: Path) -> None:
    """Compute and save all the normal distributions of a list of columns to a file.

    Args:
        df (pd.DataFrame): The input data.
        columns (list[str]): The list of columns in the input dataframe to compute the distributions for.
        output_folder (Path): The output folder to save the distribution file.
    """
    distribution_data = {"mean": [], "std": []}

    for col in columns:
        df[col] = df[col].replace(0, np.nan)
        distribution_data["mean"].append(df[col].mean())
        distribution_data["std"].append(df[col].std())

    distribution_df = pd.DataFrame(distribution_data, index=columns)
    distribution_df.to_parquet(output_folder)


def gaussian_imputation_for_zeros(df: pd.DataFrame, distribution_path: Path) -> pd.DataFrame:
    """Impute non-realistic values using a pretrained gaussian distribution.

    Args:
        df (pd.DataFrame): The input DataFrame containing non-realistic values to be imputed.
        distribution_path (Path): The path to the file containing the gaussian distribution data.

    Returns:
        pd.DataFrame: The DataFrame with missing values imputed using the gaussian distribution.
    """
    distribution = load_parquet_data(distribution_path)
    for feat in distribution.index.to_list():
        df[feat] = df[feat].replace(0, np.nan)
        num_missing = df[feat].isnull().sum()
        imputed_values = norm(loc=distribution.loc[feat, "mean"], scale=distribution.loc[feat, "std"]).rvs(
            size=num_missing
        )
        df.loc[df[feat].isnull(), feat] = imputed_values
    return df


def preprocess_data(
    data: pd.DataFrame,
    numerical_features: list,
    features_to_encode: list,
    scaler_path: Path,
    distribution_path: Path,
) -> pd.DataFrame:
    """Preprocess the data.

    Impute the non realistic values of the numerical features from the feature's distribution.
    Apply the trained scaler to the numerical data.
    One-hot encode the categorical features.

    Args:
        data (pd.DataFrame): The input data set.
        numerical_features (list): A list of numerical feature names.
        features_to_encode (list): A list of categorical feature names to encode.
        scaler_path (Path): The path to the trained scaler.
        distribution_path (Path): The path to the distribution data.

    Returns:
        pd.DataFrame: The preprocessed data set with scaled numerical features and encoded categorical features.
    """
    data = gaussian_imputation_for_zeros(data, distribution_path)
    scaler = load_pickle(scaler_path)
    data[numerical_features] = scaler.transform(data[numerical_features])
    data_encoded = pd.get_dummies(data, columns=features_to_encode, drop_first=True) * 1
    return data_encoded


def main(input_folder: Path = typer.Option(...), output_folder: Path = typer.Option(...)) -> None:
    """Main function for preprocessing stage.

    Preprocesses the data by loading the train and test splits.
    Train and save the scaler.
    Compute and save the Gaussian features distributions.
    Preprocessing the train and test splits.
    Save the preprocessed data (to parquet and CSV files).

    Args:
        input_folder (Path): The path to the input folder containing the train and test data.
        output_folder (Path): The path to the output folder where the preprocessed data will be saved.
    """
    output_folder.mkdir(exist_ok=True, parents=True)

    # Load the train and test splits
    train_set, test_set = load_splits(SplitConstants.TRAIN_FILE_NAME, SplitConstants.TEST_FILE_NAME, input_folder)

    numerical_features = PreprocessConstants.NUMERICAL_FEATURES
    features_to_encode = PreprocessConstants.FEATURES_TO_ENCODE

    # Train and save the scaler
    train_and_save_scaler(train_set, numerical_features, output_folder / PreprocessConstants.SCALER)
    compute_and_save_gaussian(
        train_set, PreprocessConstants.FEATURES_TO_IMPUTE, output_folder / PreprocessConstants.FEATURE_DISTRIBUTIONS
    )

    # preprocess the train and test splits
    train_set_st = preprocess_data(
        train_set,
        numerical_features,
        features_to_encode,
        output_folder / PreprocessConstants.SCALER,
        output_folder / PreprocessConstants.FEATURE_DISTRIBUTIONS,
    )
    test_set_st = preprocess_data(
        test_set,
        numerical_features,
        features_to_encode,
        output_folder / PreprocessConstants.SCALER,
        output_folder / PreprocessConstants.FEATURE_DISTRIBUTIONS,
    )

    # save the preprocessed data to csv files
    save_split_data(
        train_set_st,
        test_set_st,
        SplitConstants.TRAIN_FILE_NAME,
        SplitConstants.TEST_FILE_NAME,
        output_folder,
    )


if __name__ == "__main__":
    typer.run(main)
