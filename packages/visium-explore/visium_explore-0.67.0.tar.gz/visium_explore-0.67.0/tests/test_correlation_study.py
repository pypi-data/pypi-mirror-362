"""Test correlation study functions."""

import pandas as pd

from explore.containers.correlations.mutual_info import compute_mutual_info


def test_compute_mutual_info() -> None:
    """Test function for computing mutual information.

    This function creates a sample DataFrame for testing and defines the expected results.
    It also defines the discrete features dictionary and calls the function to compute mutual information.
    Finally, it asserts that the computed results match the expected results.

    Raises:
        AssertionError: If the computed results do not match the expected results.
    """
    # Create a sample DataFrame for testing
    df = pd.DataFrame({"Feature1": ["A", "B", "C", "A", "B", "C"], "Target": [0, 1, 0, 1, 0, 1]})

    # Define the expected results
    expected_results = pd.DataFrame({"Pairwise Null Ratio": [0.0], "Mutual Information": [0.0]}, index=["Feature1"])

    # Define the discrete features dictionary
    discrete_feat = {"Feature1": True, "Target": False}

    # Call the function to compute mutual information
    results = compute_mutual_info(df, "Target", discrete_feat)

    # Assert that the computed results match the expected results
    assert results.astype(float).equals(expected_results.astype(float))


def test_mi_less_4_neighbours() -> None:
    """Test case for the `compute_mutual_info` function when there are less than 4 neighbors.

    This test case checks if the `compute_mutual_info` function correctly sets the mutual information
    to None when there are less than 4 rows for a given feature (mutual_info_regression needs 3
    neighbours for numerical approximation).

    This function creates a sample DataFrame for testing and defines the expected results.
    It also defines the discrete features dictionary and calls the function to compute mutual information.
    Finally, it asserts that the computed results match the expected results.

    Raises:
        AssertionError: If the computed results do not match the expected results.
    """

    # Create a sample DataFrame for testing
    df = pd.DataFrame({"Feature1": ["A", None, "C", "A", "B", None], "Target": [0, None, None, 1, None, 1]})

    # Define the expected results
    expected_results = pd.DataFrame({"Pairwise Null Ratio": [0.6667], "Mutual Information": [None]}, index=["Feature1"])

    # Define the discrete features dictionary
    discrete_feat = {"Feature1": True, "Target": False}

    # Call the function to compute mutual information
    results = compute_mutual_info(df, "Target", discrete_feat)

    # Assert that the computed results match the expected results
    assert results.astype(float).equals(expected_results.astype(float))


def test_mi_not_enough_info() -> None:
    """Test case for the `compute_mutual_info` function when a categorical variable has
    not enough information to compute mutual information.

    This test case checks if the `compute_mutual_info` function correctly sets the mutual information
    to None when one of the variables in question (feature or target) that is categorical has only null
    values or only unique values.

    This function creates a sample DataFrame for testing and defines the expected results.
    It also defines the discrete features dictionary and calls the function to compute mutual information.
    Finally, it asserts that the computed results match the expected results.

    Raises:
        AssertionError: If the computed results do not match the expected results.
    """
    # Create a sample DataFrame for testing
    df = pd.DataFrame({"Feature1": ["A", "B", "C", "A", "B", "C"], "Target": [0, 1, 2, 3, 4, 5]})

    # Define the expected results
    expected_results = pd.DataFrame({"Pairwise Null Ratio": [0.0], "Mutual Information": [None]}, index=["Feature1"])

    # Define the discrete features dictionary
    discrete_feat = {"Feature1": True, "Target": True}

    # Call the function to compute mutual information
    results = compute_mutual_info(df, "Target", discrete_feat)

    # Assert that the computed results match the expected results
    assert results.astype(float).equals(expected_results.astype(float))
