"""Download iris dataset and save it as parquet file."""

import pathlib

import typer
from sklearn.datasets import load_breast_cancer  # type: ignore
from sklearn.datasets import load_iris  # type: ignore


def main(output_dir: pathlib.Path = typer.Option(...)) -> None:
    """Download iris dataset and save it as parquet file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    # iris_df = load_breast_cancer(as_frame=True).frame  # pylint: disable=no-member
    iris_df = load_iris(as_frame=True).frame  # pylint: disable=no-member
    iris_df["target"] = iris_df["target"].map({0: "setosa", 1: "versicolor", 2: "virginica"})

    iris_df.to_parquet(output_dir / "iris.parquet")


if __name__ == "__main__":
    typer.run(main)
