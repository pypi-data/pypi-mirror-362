"""Read the model from the train model step."""

import pathlib
import pickle

import sklearn


def read_model(train_model_dir: pathlib.Path) -> sklearn.base.ClassifierMixin:
    """Read the model from the train model step."""
    with open(train_model_dir / "model.pkl", "rb") as file:
        model = pickle.load(file)
    return model
