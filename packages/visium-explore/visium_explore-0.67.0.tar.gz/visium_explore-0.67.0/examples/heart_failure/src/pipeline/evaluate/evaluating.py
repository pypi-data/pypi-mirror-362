"""Module for evaluating the models."""

from pathlib import Path

import pandas as pd
import typer
from sklearn.base import BaseEstimator
from sklearn.metrics import balanced_accuracy_score, classification_report

# isort: off
from params import TrainEvalParams

# isort: on
from src.pipeline.evaluate.io import load_model_pickle, save_metrics
from src.pipeline.preprocess.io import load_splits
from src.pipeline.split.constants import SplitConstants


def compute_metrics(model: BaseEstimator, data_set: pd.DataFrame, label: str) -> dict:
    """Compute evaluation metrics for a model on a given dataset.

    Args:
        model (BaseEstimator): The trained model to evaluate.
        data_set (pd.DataFrame): The dataset to evaluate the model on.
        label (str): The name of the target variable in the dataset.

    Returns:
        dict: A dictionary containing the evaluation metrics.
    """
    y_pred = model.predict(data_set.drop([label], axis=1, inplace=False))
    y_true = data_set[label]

    evaluation_metrics = classification_report(y_true, y_pred, output_dict=True)
    evaluation_metrics["balanced_accuracy_score"] = balanced_accuracy_score(y_true, y_pred)
    return evaluation_metrics


def evaluate_model(
    model: BaseEstimator,
    train_set: pd.DataFrame,
    test_set: pd.DataFrame,
    label: str,
) -> dict:
    """Evaluate the model on the training and test set.

    Args:
        model (BaseEstimator): The machine learning model to evaluate.
        train_set (pd.DataFrame): The training dataset.
        test_set (pd.DataFrame): The test dataset.
        label (str): The label column name.

    Returns:
        dict: A dictionary containing the evaluation metrics for the model on the training and test set.
    """
    # Retrieve the model's class name
    model_name = model.__class__.__name__

    evaluation_metrics = {}
    evaluation_metrics["train"] = compute_metrics(model, train_set, label)
    evaluation_metrics["test"] = compute_metrics(model, test_set, label)
    print(f"{model_name}:\n {evaluation_metrics} \n")
    return evaluation_metrics


def main(
    model_folder: Path = typer.Option(...),
    preprocessed_folder: Path = typer.Option(...),
    output_folder: Path = typer.Option(...),
) -> None:
    """Load the models, evaluate the models, then save the evaluation metrics.

    Args:
        model_folder (Path): The folder path where the models are stored.
        preprocessed_folder (Path): The folder path where the preprocessed data is stored.
        output_folder (Path): The folder path where the evaluation metrics will be saved.
    """
    output_folder.mkdir(exist_ok=True, parents=True)

    # Load the preprocessed train and test splits
    train_set, test_set = load_splits(
        SplitConstants.TRAIN_FILE_NAME, SplitConstants.TEST_FILE_NAME, preprocessed_folder
    )

    # Initialize, train and save all models
    for _, model_param in TrainEvalParams.model_config.items():
        model = load_model_pickle(model_folder, model_param["model_file"])
        eval_metrics = evaluate_model(
            model,
            train_set,
            test_set,
            SplitConstants.LABEL,
        )
        save_metrics(eval_metrics, output_folder, model_param["metrics_file"])


if __name__ == "__main__":
    typer.run(main)
