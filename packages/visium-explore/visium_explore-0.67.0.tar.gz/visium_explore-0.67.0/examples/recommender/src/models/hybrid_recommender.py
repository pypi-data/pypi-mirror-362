"""Implementation of a hybrid recommender system using LightFM."""

import numpy as np
from lightfm import LightFM

from src.models.recommender import RecommenderSystem


class HybridRecommender(RecommenderSystem):
    """Hybrid Recommender System using LightFM."""

    def __init__(self, no_components=10, loss="logistic", learning_rate=0.05, random_state=42) -> None:
        super().__init__()
        self.model = LightFM(
            no_components=no_components, loss=loss, learning_rate=learning_rate, random_state=random_state
        )

    def fit(self, interactions, user_features=None, item_features=None, epochs=1):
        """Fit the model and compute the propensity scores."""
        self.model.fit(
            interactions=interactions, user_features=user_features, item_features=item_features, epochs=epochs
        )
        self.propensity_score_matrix = self.compute_propensity_scores(user_features, item_features)

    def compute_propensity_scores(self, user_features=None, item_features=None):
        """Compute the propensity scores.

        The propensity scores are computed as the dot product of the user and item embeddings/biases.
        """
        user_biases, user_embeddings = self.get_user_representations(features=user_features)
        item_biases, item_embeddings = self.get_item_representations(features=item_features)
        bias = user_biases[:, np.newaxis] + item_biases
        return user_embeddings @ item_embeddings.T + bias

    def get_user_representations(self, features=None):
        """Get user representations.

        These are the vectores that represent the users in the latent space.
        """
        return self.model.get_user_representations(features=features)

    def get_item_representations(self, features=None):
        """Get item representations.

        These are the vectores that represent the items in the latent space.
        """
        return self.model.get_item_representations(features=features)
