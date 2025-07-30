"""Implementation of a Most Popular Recommender System."""

import numpy as np

from src.models.recommender import RecommenderSystem


class MostPopularRecommender(RecommenderSystem):
    """Most Popular Recommender System."""

    def __init__(self) -> None:
        super().__init__()
        self.nb_users = 0
        self.item_popularity = None

    def fit(self, interactions):
        """Fit the model and compute the propensity scores."""
        self.item_popularity = np.array(interactions.sum(axis=0))
        self.nb_users = interactions.shape[0]
        self.propensity_score_matrix = self.compute_propensity_scores()

    def compute_propensity_scores(self):
        """Compute the propensity scores.

        The propensity scores correspond to the historical popularity of the items.
        """
        return np.tile(self.item_popularity, (self.nb_users, 1)).astype(np.float32)
