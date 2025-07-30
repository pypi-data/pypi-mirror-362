"""Tests to check that implementation of evalution function matches LightFM's implementation."""

import pytest
import scipy
from lightfm.evaluation import precision_at_k, recall_at_k

from src.models.hybrid_recommender import HybridRecommender
from src.pipeline.evaluate_model.utils import evaluate_model


@pytest.fixture(scope="session", name="load_data")
def load_data_fixture():
    """Load data for testing."""
    train_interactions = scipy.sparse.load_npz("tests/data/train_interactions.npz")
    test_interactions = scipy.sparse.load_npz("tests/data/test_interactions.npz")
    user_features = scipy.sparse.load_npz("tests/data/user_features.npz")
    item_features = scipy.sparse.load_npz("tests/data/item_features.npz")
    yield train_interactions, test_interactions, user_features, item_features


def test_metrics_at_k_computation_without_features(load_data):
    """Test metrics at k computation without user/item features."""

    train_interactions, test_interactions, _, _ = load_data

    rec_sys = HybridRecommender()

    rec_sys.fit(train_interactions, epochs=10)

    rec_sys_lightfm = rec_sys.model

    metrics_at_k = evaluate_model(rec_sys, test_interactions, train_interactions, k=10)

    mean_test_precision_at_k = precision_at_k(
        rec_sys_lightfm,
        test_interactions,
        train_interactions=train_interactions,
        k=10,
        preserve_rows=True,
    ).mean()

    mean_test_recall_at_k = recall_at_k(
        rec_sys_lightfm,
        test_interactions,
        train_interactions,
        k=10,
        preserve_rows=True,
    ).mean()

    assert pytest.approx(metrics_at_k.mean_test_precision_at_k) == mean_test_precision_at_k
    assert pytest.approx(metrics_at_k.mean_test_recall_at_k) == mean_test_recall_at_k


def test_metrics_at_k_computation_with_features(load_data):
    """Test metrics at k computation when a model uses user/item features."""

    train_interactions, test_interactions, user_features, item_features = load_data

    rec_sys = HybridRecommender()

    rec_sys.fit(train_interactions, user_features, item_features, epochs=10)

    rec_sys_lightfm = rec_sys.model

    metrics_at_k = evaluate_model(rec_sys, test_interactions, train_interactions, k=10)

    mean_test_precision_at_k = precision_at_k(
        rec_sys_lightfm,
        test_interactions,
        train_interactions=train_interactions,
        user_features=user_features,
        item_features=item_features,
        k=10,
        preserve_rows=True,
    ).mean()

    mean_test_recall_at_k = recall_at_k(
        rec_sys_lightfm,
        test_interactions,
        train_interactions,
        user_features=user_features,
        item_features=item_features,
        k=10,
        preserve_rows=True,
    ).mean()

    assert pytest.approx(metrics_at_k.mean_test_precision_at_k) == mean_test_precision_at_k
    assert pytest.approx(metrics_at_k.mean_test_recall_at_k) == mean_test_recall_at_k
