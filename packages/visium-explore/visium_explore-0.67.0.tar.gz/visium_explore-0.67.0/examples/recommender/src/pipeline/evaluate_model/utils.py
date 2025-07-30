"""Evaluate the model."""

import numpy as np
from scipy.sparse import csr_matrix


class MetricsAtK:
    """Metrics at k."""

    def __init__(self, test_precision_at_k, test_recall_at_k):
        self.mean_test_precision_at_k = test_precision_at_k
        self.mean_test_recall_at_k = test_recall_at_k


def evaluate_model(model, test_interactions, train_interactions=None, k=10):
    """Evaluate model."""
    propensity_score_matrix = model.propensity_score_matrix
    if train_interactions is not None:
        # We set the propensity score of the training interactions to -inf
        propensity_score_matrix[train_interactions.nonzero()] = -float("inf")
    metrics_at_k = compute_metrics_at_k(propensity_score_matrix, test_interactions, k)
    return metrics_at_k


def compute_metrics_at_k(propensity_score_matrix, test_interactions, k=10):
    """Compute metrics at k.

    Metrics computed:
        - Precision at k
        - Recall at k
    """
    # TODO: Implement MAP@K as well
    num_users, num_items = propensity_score_matrix.shape
    top_k_items = np.argpartition(propensity_score_matrix, -np.arange(1, k + 1))[:, -k:]
    sparse_reco = csr_matrix(
        (np.ones(num_users * k), (np.repeat(np.arange(num_users), k), top_k_items.flatten())),
        shape=(num_users, num_items),
    )
    pr_at_k = test_interactions.multiply(sparse_reco).sum(axis=1) / k
    rec_at_k = test_interactions.multiply(sparse_reco).sum(axis=1) / test_interactions.sum(axis=1)
    return MetricsAtK(pr_at_k.mean(), rec_at_k.mean())
