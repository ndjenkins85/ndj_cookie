# Copyright © 2021 by Nick Jenkins. All rights reserved

"""Tests for utils.py."""
import pytest

from my_project import utils


@pytest.mark.xfail(raises=FileNotFoundError)
def test_fail() -> None:
    """It tests nothing useful."""
    utils.update_environments()
