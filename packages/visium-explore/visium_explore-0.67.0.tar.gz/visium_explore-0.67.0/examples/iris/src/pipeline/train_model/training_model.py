"""Train a model using sklearn."""

import pathlib
import pickle

import mlflow.sklearn  # type: ignore
import pandas as pd
import sklearn.dummy  # type: ignore
import sklearn.neural_network  # type: ignore
import typer
from mlflow.models import infer_signature
from params import TrainModelParams


def main(split_dataset_dir: pathlib.Path = typer.Option(...), output_dir: pathlib.Path = typer.Option(...)) -> None:
    """Read data from the split dataset step and then train a model."""
    output_dir.mkdir(parents=True, exist_ok=True)
    # Read data from the split dataset step
    train_df = pd.read_parquet(split_dataset_dir / "train.parquet")

    # train model
    hidden_layer_sizes = [TrainModelParams.HIDDEN_LAYER_SIZE] * TrainModelParams.N_HIDDEN_LAYERS
    model = sklearn.neural_network.MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=500)

    X_train = train_df.drop("target", axis=1)
    model.fit(X_train, train_df["target"])

    mlflow.sklearn.save_model(
        model, output_dir / "mlflow_model", signature=infer_signature(X_train, model.predict(X_train))
    )

    # Save the model as a pickle file
    with open(output_dir / "model.pkl", "wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    typer.run(main)
