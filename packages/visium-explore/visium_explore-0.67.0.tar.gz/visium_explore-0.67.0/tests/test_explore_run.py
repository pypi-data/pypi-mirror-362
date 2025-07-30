"""Test that explore can be run from a bash shell"""

import subprocess

import pytest


def test_explore_run() -> None:
    """Test that explore can be run from a bash shell"""

    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(["explore"], capture_output=True, timeout=1, check=True)
