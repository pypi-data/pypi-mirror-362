"""Analyse the principal component of the user and item embeddings."""

import pathlib

import numpy as np
import pandas as pd
import typer
from sklearn.decomposition import PCA


def main(
    preprocess_dataset_dir: pathlib.Path = typer.Option(...),
    train_hybrid_model_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Download datasets and save them as parquet file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    user_features = pd.read_parquet(preprocess_dataset_dir / "user_features.parquet")
    item_features = pd.read_parquet(preprocess_dataset_dir / "item_features.parquet")

    user_embeddings_hybrid = load_embeddings_as_dataframe(train_hybrid_model_dir, "user_embeddings.npy")
    item_embeddings_hybrid = load_embeddings_as_dataframe(train_hybrid_model_dir, "item_embeddings.npy")

    pc_user_embeddings_hybrid = get_principal_components(user_embeddings_hybrid)
    pc_item_embeddings_hybrid = get_principal_components(item_embeddings_hybrid)

    save_user_embeddings_with_features_as_parquet(
        pc_user_embeddings_hybrid, user_features, output_dir, "pc_user_embeddings_hybrid.parquet"
    )
    save_item_embeddings_with_features_as_parquet(
        pc_item_embeddings_hybrid, item_features, output_dir, "pc_item_embeddings_hybrid.parquet"
    )


def load_embeddings_as_dataframe(input_dir, filename):
    """Load embeddings as dataframe."""
    embeddings = np.load(input_dir / filename)
    df_embeddings = pd.DataFrame(embeddings)
    return df_embeddings


def save_user_embeddings_with_features_as_parquet(df_embeddings, df_user_features, output_dir, filename):
    """Save user embeddings with merged user features as parquet."""
    df_embeddings_with_features = df_embeddings.merge(df_user_features, left_index=True, right_index=True)
    df_embeddings_with_features.to_parquet(output_dir / filename)


def save_item_embeddings_with_features_as_parquet(df_embeddings, df_item_features, output_dir, filename):
    """Save item embeddings with merged item features as parquet."""
    df_embeddings_with_features = df_embeddings.merge(df_item_features, left_index=True, right_index=True)
    df_embeddings_with_features.to_parquet(output_dir / filename)


def get_principal_components(df_embeddings):
    """Get first 2 principal components."""
    pca = PCA(n_components=2)
    pca.fit(df_embeddings)
    principal_components = pd.DataFrame(pca.transform(df_embeddings))
    principal_components.columns = ["PC1", "PC2"]
    return principal_components


if __name__ == "__main__":
    typer.run(main)
