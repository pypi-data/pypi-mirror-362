"""Module for input/output for training."""

from pathlib import Path

from sklearn.base import BaseEstimator

from ..preprocess.io import save_pickle


def save_model_pickle(model: BaseEstimator, output_folder: Path, file_name: str) -> None:
    """Save a model to a pickle file.

    Args:
        model (BaseEstimator): The model to be saved.
        output_folder (Path): The folder where the model will be saved.
        file_name (str): The name of the file to save the model as.
    """
    save_pickle(model, output_folder / file_name)
