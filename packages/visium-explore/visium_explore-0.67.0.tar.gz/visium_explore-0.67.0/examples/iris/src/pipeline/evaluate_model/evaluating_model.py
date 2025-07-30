"""Evaluate the model using test data."""

import json
import pathlib

import pandas as pd
import sklearn.metrics
import typer

from src.pipeline.evaluate_model.io import read_model


def main(
    train_model_dir: pathlib.Path = typer.Option(...),
    split_dataset_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Evaluate the model using test data."""
    output_dir.mkdir(parents=True, exist_ok=True)
    # Read data from the split dataset step
    test_df = pd.read_parquet(split_dataset_dir / "test.parquet")

    # Read the model from the train model step
    model = read_model(train_model_dir)

    # Compute predictions
    test_df["preds"] = model.predict(test_df.drop("target", axis=1))

    # Evaluate the model

    metrics_model = evaluate_model(test_df["target"], test_df["preds"])

    test_df["majority_baseline"] = test_df["target"].value_counts().index[0]
    metrics_majority_baseline = evaluate_model(test_df["target"], test_df["majority_baseline"])

    metrics = {
        "model": metrics_model,
        "majority_baseline": metrics_majority_baseline,
    }

    # Save the accuracy as a json file
    with open(pathlib.Path("metrics/metrics.json"), "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    test_df.to_parquet(output_dir / "preds.parquet")


def evaluate_model(y_true: list[str], y_pred: list[str]) -> dict[str, float]:
    accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
    balanced_accuracy = sklearn.metrics.balanced_accuracy_score(y_true, y_pred)
    f1_score = sklearn.metrics.f1_score(y_true, y_pred, average="macro")
    return {"accuracy": accuracy, "balanced_accuracy": balanced_accuracy, "f1_score": f1_score}


if __name__ == "__main__":
    typer.run(main)
