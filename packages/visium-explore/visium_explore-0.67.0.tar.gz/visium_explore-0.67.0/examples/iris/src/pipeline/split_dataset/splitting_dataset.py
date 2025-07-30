"""Splitting dataset module."""

import pathlib

import pandas as pd
import typer
from params import SEED, TEST_RATIO
from sklearn.model_selection import train_test_split  # type: ignore


def main(
    download_dataset_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Split dataset into train and test."""
    output_dir.mkdir(parents=True, exist_ok=True)
    iris_df = pd.read_parquet(download_dataset_dir / "iris.parquet")

    # Split data with sklearn
    train_df, test_df = train_test_split(iris_df, test_size=TEST_RATIO, random_state=SEED)

    train_df.to_parquet(output_dir / "train.parquet")
    test_df.to_parquet(output_dir / "test.parquet")


if __name__ == "__main__":
    typer.run(main)
