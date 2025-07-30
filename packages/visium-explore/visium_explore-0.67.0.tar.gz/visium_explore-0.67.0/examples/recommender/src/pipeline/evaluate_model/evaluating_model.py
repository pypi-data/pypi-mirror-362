"""Evaluating model."""

import json
import pathlib
import pickle

import scipy
import typer
from params import K

from src.pipeline.evaluate_model.utils import evaluate_model


def main(
    train_baseline_model_dir: pathlib.Path = typer.Option(...),
    train_hybrid_model_dir: pathlib.Path = typer.Option(...),
    create_lightfm_dataset_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Evaluating Model."""
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline_model = load_pickle_file(train_baseline_model_dir / "baseline_model.pkl")
    hybrid_model = load_pickle_file(train_hybrid_model_dir / "hybrid_model.pkl")

    train_interactions = scipy.sparse.load_npz(create_lightfm_dataset_dir / "train_interactions.npz")
    test_interactions = scipy.sparse.load_npz(create_lightfm_dataset_dir / "test_interactions.npz")

    hybrid_model_metrics = evaluate_model(hybrid_model, test_interactions, train_interactions, K)
    baseline_model_metrics = evaluate_model(baseline_model, test_interactions, train_interactions, K)

    metrics = {"baseline_model": baseline_model_metrics.__dict__, "hybrid_model": hybrid_model_metrics.__dict__}

    with open("metrics/metrics.json", "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)


def load_pickle_file(file_path: pathlib.Path):
    """Load pickle file."""
    with open(file_path, "rb") as file:
        return pickle.load(file)


if __name__ == "__main__":
    typer.run(main)
