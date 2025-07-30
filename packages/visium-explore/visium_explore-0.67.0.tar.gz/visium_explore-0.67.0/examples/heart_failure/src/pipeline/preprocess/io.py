"""Module for input/output for preprocessing."""

import pickle
from pathlib import Path
from typing import Any

import pandas as pd


def load_splits(train_file_name: str, test_file_name: str, input_folder: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load splitted datasets from input folder.

    Args:
        train_file_name (str): The name of the train file.
        test_file_name (str): The name of the test file.
        input_folder (Path): The path to the input folder.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the train set and test set as pandas DataFrames.
    """
    train_set = pd.read_parquet(input_folder / f"{train_file_name}.parquet")
    test_set = pd.read_parquet(input_folder / f"{test_file_name}.parquet")
    return train_set, test_set


def save_pickle(obj: Any, file_path: Path) -> None:
    """Save an object to a pickle file.

    Args:
        obj (Any): The object to be saved.
        file_path (Path): The path to the pickle file.
    """
    with open(file_path, "wb") as file:
        pickle.dump(obj, file)


def load_pickle(file_path: str) -> Any:
    """Load data from a pickle file.

    Args:
        file_path (str): The path to the pickle file.

    Returns:
        Any: The loaded data from the pickle file.
    """
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data
