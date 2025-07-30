"""Download dataset and save it as parquet file."""

import pathlib
import pickle

import numpy as np
import scipy
import typer
from params import EPOCHS, LEARNING_RATE, LOSS, NO_COMPONENTS, RANDOM_STATE, WITH_ITEM_FEATURES, WITH_USER_FEATURES

from src.models.hybrid_recommender import HybridRecommender


def main(
    input_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Download datasets and save them as parquet file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    train_interactions = scipy.sparse.load_npz(input_dir / "train_interactions.npz")

    train_user_features = scipy.sparse.load_npz(input_dir / "user_features.npz") if WITH_USER_FEATURES else None
    train_item_features = scipy.sparse.load_npz(input_dir / "item_features.npz") if WITH_ITEM_FEATURES else None

    model = HybridRecommender(
        no_components=NO_COMPONENTS, learning_rate=LEARNING_RATE, loss=LOSS, random_state=RANDOM_STATE
    )
    model.fit(train_interactions, user_features=train_user_features, item_features=train_item_features, epochs=EPOCHS)

    _, user_embeddings = model.get_user_representations(train_user_features)
    _, item_embeddings = model.get_item_representations(train_item_features)

    # Store embeddings
    np.save(output_dir / "user_embeddings.npy", user_embeddings)
    np.save(output_dir / "item_embeddings.npy", item_embeddings)

    # Store model as a pickle file
    with open(output_dir / "hybrid_model.pkl", "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    typer.run(main)
