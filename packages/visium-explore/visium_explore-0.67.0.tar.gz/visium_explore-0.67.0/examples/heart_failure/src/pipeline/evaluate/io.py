"""Module for input/output for evaluation."""

import json
from pathlib import Path

from sklearn.base import BaseEstimator

from ..preprocess.io import load_pickle


def load_model_pickle(model_folder: Path, file_name: str) -> BaseEstimator:
    """Load the model from a pickle file.

    Args:
        model_folder (Path): The folder where the model is stored.
        file_name (str): The name of the pickle file.

    Returns:
        BaseEstimator or None: The loaded model if successful, None otherwise.
    """
    model = load_pickle(model_folder / file_name)
    return model


def save_metrics(evaluation_metrics: dict, output_folder: Path, file_name: str) -> None:
    """Save the evaluation metrics to a json file.

    Args:
        evaluation_metrics (dict): A dictionary containing the evaluation metrics.
        output_folder (Path): The path to the output folder where the json file will be saved.
        file_name (str): The name of the json file.
    """
    file_path = output_folder / file_name
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(evaluation_metrics, file, ensure_ascii=False, indent=4)
