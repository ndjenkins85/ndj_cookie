# Copyright © 2021 by Nick Jenkins. All rights reserved

"""Tests for utils.py."""
import pytest

from my_project import utils


def test_fail() -> None:
    """It tests nothing useful."""
    with pytest.raises(FileNotFoundError):
        utils.update_environments()
