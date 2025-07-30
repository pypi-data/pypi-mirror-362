"""Preprocess datasets and save them as parquet file."""

import pathlib

import pandas as pd
import typer

from src.pipeline.preprocess_dataset.features import ItemFeatures, UserFeatures


def main(
    input_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Preprocess datasets and save them as parquet file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    df_users = pd.read_parquet(input_dir / "df_users.parquet")
    df_movies = pd.read_parquet(input_dir / "df_movies.parquet")
    data_tr = pd.read_parquet(input_dir / "data_tr.parquet")
    data_te = pd.read_parquet(input_dir / "data_te.parquet")

    # Implicit scenario, we do not care about ratings
    train_interactions = data_tr[["user_id", "item_id"]]
    test_interactions = data_te[["user_id", "item_id"]]

    # Only keep items that are in the training set
    test_interactions = test_interactions[test_interactions["item_id"].isin(train_interactions["item_id"])]

    user_features = UserFeatures().features
    item_features = ItemFeatures().features

    user_features = df_users[["user_id"] + user_features]
    item_features = df_movies[["movie_id"] + item_features]

    # We can only make predictions on users and items that are in the training set
    user_features = user_features[user_features["user_id"].isin(train_interactions["user_id"])]
    item_features = item_features[item_features["movie_id"].isin(train_interactions["item_id"])]

    user_features.to_parquet(output_dir / "user_features.parquet")
    item_features.to_parquet(output_dir / "item_features.parquet")

    train_interactions.to_parquet(output_dir / "train_interactions.parquet")
    test_interactions.to_parquet(output_dir / "test_interactions.parquet")


if __name__ == "__main__":
    typer.run(main)
