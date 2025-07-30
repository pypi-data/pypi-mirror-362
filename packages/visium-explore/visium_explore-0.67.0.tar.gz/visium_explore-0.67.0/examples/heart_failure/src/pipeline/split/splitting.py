"""Module for data splitting."""

from pathlib import Path

import pandas as pd
import typer
from sklearn.model_selection import train_test_split

# isort: off
from params import SplitParams

# isort: on
from src.pipeline.split.constants import SplitConstants
from src.pipeline.split.io import load_parquet_data, save_split_data


def split_data(dataset: pd.DataFrame, test_proportion: float, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataset into a train and test set using the given proportion and seed.

    Args:
        dataset (pd.DataFrame): The dataset to be split.
        test_proportion (float): The proportion of the dataset to be used for testing.
        seed (int): The random seed for reproducibility.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the train set and test set.
    """
    train_set, test_set = train_test_split(
        dataset, test_size=test_proportion, random_state=seed, stratify=dataset[SplitConstants.LABEL]
    )
    return train_set, test_set


def main(input_file_path: Path = typer.Option(...), output_folder: Path = typer.Option(...)) -> None:
    """Main function, load the dataset, split it into train and test, then save the splits to parquet files.

    Args:
        input_file_path (Path): The path to the input file.
        output_folder (Path): The path to the output folder.
    """
    output_folder.mkdir(exist_ok=True, parents=True)

    # Load the IRIS dataset
    df = load_parquet_data(input_file_path)

    # split the data into train and test splits
    train_set, test_set = split_data(df, SplitParams.TEST_PROPORTION, SplitParams.SEED)

    # save the data to csv files
    # pylint: disable=R0801
    save_split_data(
        train_set,
        test_set,
        SplitConstants.TRAIN_FILE_NAME,
        SplitConstants.TEST_FILE_NAME,
        output_folder,
    )
    # pylint: enable=R0801


if __name__ == "__main__":
    typer.run(main)
