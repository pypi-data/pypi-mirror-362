"""Download dataset and save it as parquet file."""

import pathlib
import pickle

import numpy as np
import pandas as pd
import scipy as sp
import typer
from lightfm.data import Dataset

from src.pipeline.create_lightfm_dataset.io import save_sparse_matrix_as_parquet


def main(
    input_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Create LightFM dataset."""
    output_dir.mkdir(parents=True, exist_ok=True)
    train_interactions = pd.read_parquet(input_dir / "train_interactions.parquet")
    test_interactions = pd.read_parquet(input_dir / "test_interactions.parquet")
    df_user_features = pd.read_parquet(input_dir / "user_features.parquet")
    df_item_features = pd.read_parquet(input_dir / "item_features.parquet")

    train_users = train_interactions["user_id"].unique()
    train_items = train_interactions["item_id"].unique()

    # To use the fit method of LightFM's Dataset class, we need to generate all possible values of the features
    # e.g. for Gender, we need to provide 'M' and 'F' as possible values.

    # Be careful: If your possible values are NOT distinct between user/item features,
    # then some further processing is required.
    # e.g. if you have binned the 'age' and 'watchtime' into 'low' and 'high' categories,
    # then one option to distinguish between the values is appending a colon:
    # e.g. 'age:low', 'age:high', 'watchime:low', 'watchtime:high'

    # TODO: This difference to get access to the item_features and the user_features is not good
    # and is still dependent on structure of raw data
    all_possible_item_features = df_item_features.columns[1:].tolist()
    all_possible_user_features = df_user_features.stack().unique().tolist()

    dataset = Dataset(user_identity_features=True, item_identity_features=True)
    dataset.fit(
        users=train_users,
        items=train_items,
        user_features=all_possible_user_features,
        item_features=all_possible_item_features,
    )

    train_interactions, _ = dataset.build_interactions(
        zip(train_interactions["user_id"], train_interactions["item_id"])
    )
    test_interactions, _ = dataset.build_interactions(zip(test_interactions["user_id"], test_interactions["item_id"]))

    user_features = dataset.build_user_features(extract_user_features(df_user_features))
    sp.sparse.save_npz(output_dir / "user_features.npz", user_features)
    save_sparse_matrix_as_parquet(user_features, output_dir, "df_user_features.parquet")

    item_features = dataset.build_item_features(extract_item_features(df_item_features))
    sp.sparse.save_npz(output_dir / "item_features.npz", item_features)
    save_sparse_matrix_as_parquet(item_features, output_dir, "df_item_features.parquet")

    sp.sparse.save_npz(output_dir / "train_interactions.npz", train_interactions)
    sp.sparse.save_npz(output_dir / "test_interactions.npz", test_interactions)

    save_sparse_matrix_as_parquet(train_interactions, output_dir, "df_train_interactions.parquet")
    save_sparse_matrix_as_parquet(test_interactions, output_dir, "df_test_interactions.parquet")

    dataset_mapping = dataset.mapping()
    # Store mapping as a pickle file
    with open(output_dir / "dataset_mapping.pkl", "wb") as f:
        pickle.dump(dataset_mapping, f)


def non_zero_columns(row):
    """Return non zero columns."""
    return row.index[np.flatnonzero(row)].values.tolist()


def extract_item_features(item_features):
    """Extract item features."""
    return zip(item_features["movie_id"], item_features[item_features.columns[1:]].apply(non_zero_columns, axis=1))


def extract_user_features(user_features):
    """Extract user features."""
    return zip(user_features["user_id"], user_features[user_features.columns[1:]].values.tolist())


if __name__ == "__main__":
    typer.run(main)
