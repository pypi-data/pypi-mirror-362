"""Module for input/output for splitting."""

from pathlib import Path

import pandas as pd


def load_parquet_data(input_file_path: Path) -> pd.DataFrame:
    """Load data from a Parquet file.

    Args:
        input_file_path (Path): The path to the input Parquet file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    data = pd.read_parquet(input_file_path)
    return data


def save_split_data(
    train_set: pd.DataFrame,
    test_set: pd.DataFrame,
    train_file_name: str,
    test_file_name: str,
    output_folder: Path,
) -> None:
    """Save the train and test splits to parquet files.

    Args:
        train_set (pd.DataFrame): The training dataset.
        test_set (pd.DataFrame): The testing dataset.
        train_file_name (str): The name of the train file.
        test_file_name (str): The name of the test file.
        output_folder (Path): The output folder where the files will be saved.
    """
    # Save as Parquet
    train_set.to_parquet(output_folder / f"{train_file_name}.parquet", index=False)
    test_set.to_parquet(output_folder / f"{test_file_name}.parquet", index=False)
