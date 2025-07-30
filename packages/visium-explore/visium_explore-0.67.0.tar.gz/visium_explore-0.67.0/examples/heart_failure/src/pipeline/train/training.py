"""Module for training the models."""

import importlib
from inspect import signature
from pathlib import Path

import pandas as pd
import typer
from sklearn.base import BaseEstimator

# isort: off
from params import TrainEvalParams

# isort: on
from src.pipeline.preprocess.io import load_splits
from src.pipeline.split.constants import SplitConstants
from src.pipeline.train.io import save_model_pickle


def init_model(model_params: dict) -> BaseEstimator:
    """Initialize a ML model based on the provided model parameters.

    Args:
        model_params (dict): A dictionary containing the model parameters.

    Returns:
        BaseEstimator: An instance of the machine learning model.
    """
    # Split the module path and class name
    module_path, class_name = model_params["model_import"].rsplit(".", 1)

    # Dynamically import the module
    module = importlib.import_module(module_path)
    model_class = getattr(module, class_name)

    # Get the constructor signature
    init_signature = signature(model_class.__init__)

    # Filter model_params to only include valid constructor arguments (excluding 'self')
    valid_params = {k: v for k, v in model_params.items() if k in init_signature.parameters and k != "self"}

    # Get the class and instantiate it with any keyword arguments
    model = model_class(**valid_params)
    return model


def train_model(
    model: BaseEstimator,
    data_set: pd.DataFrame,
    label: str,
) -> BaseEstimator:
    """Train an initialized model.

    Args:
        model (BaseEstimator): The initialized model to train.
        data_set (pd.DataFrame): The dataset used for training.
        label (str): The label column in the dataset.

    Returns:
        BaseEstimator: The trained model.
    """
    model.fit(data_set.drop([label], axis=1, inplace=False), data_set[label])
    return model


def main(
    preprocessed_folder: Path = typer.Option(...),
    output_folder: Path = typer.Option(...),
) -> None:
    """Initialize the models, train the models, then save the models.

    Args:
        preprocessed_folder (Path): Path to the folder containing the preprocessed data.
        output_folder (Path): Path to the folder where the trained models will be saved.
    """
    output_folder.mkdir(exist_ok=True, parents=True)

    # Load the preprocessed train and test splits
    train_set, _ = load_splits(SplitConstants.TRAIN_FILE_NAME, SplitConstants.TEST_FILE_NAME, preprocessed_folder)

    # Initialize, train and save all models
    for _, model_param in TrainEvalParams.model_config.items():
        model = init_model(model_param)
        model = train_model(model, train_set, SplitConstants.LABEL)
        save_model_pickle(model, output_folder, model_param["model_file"])


if __name__ == "__main__":
    typer.run(main)
