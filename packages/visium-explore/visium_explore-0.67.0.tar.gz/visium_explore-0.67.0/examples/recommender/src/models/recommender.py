"""Defines the Recommender class."""

from abc import ABC, abstractmethod


class RecommenderSystem(ABC):
    """Recommender System base class."""

    @abstractmethod
    def __init__(self) -> None:
        self.propensity_score_matrix = None

    @abstractmethod
    def fit(self, interactions):
        """Fit the model and compute the propensity score matrix."""

    @abstractmethod
    def compute_propensity_scores(self):
        """Compute the propensity scores.

        Higher score indicates higher likelihood of the user interacting with the item.
        """
