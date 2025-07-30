"""Train the baseline, a Most Popular Items recommender."""

import pathlib
import pickle

import scipy
import typer

from src.models.baseline import MostPopularRecommender


def main(
    input_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Training the baseline model and storing it as a pickle file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    train_interactions = scipy.sparse.load_npz(input_dir / "train_interactions.npz")

    model = MostPopularRecommender()
    model.fit(interactions=train_interactions)

    # Store model as a pickle file
    with open(output_dir / "baseline_model.pkl", "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    typer.run(main)
