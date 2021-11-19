# -*- coding: utf-8 -*-
# Copyright © 2021 by Nick Jenkins. All rights reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Mix of utilities."""
import json
from pathlib import Path
from typing import Any, Callable, Dict, List

import yaml

from ndj_pipeline import config, model, post


def clean_column_names(column_list: List[str]) -> Dict[str, str]:
    """Simple string cleaning rules for columns.

    Args:
        column_list: Column names to be cleaned

    Returns:
        A dict mapping old and cleaned column names.
    """
    new_column_list = [
        (
            col.lower()
            .strip()
            .replace("  ", "_")
            .replace(r"/", "_")
            .replace(r"\n", "_")
            .replace(r"\\", "_")
            .replace(r"\t", "_")
            .replace(" ", "_")
            .replace("^", "")
        )
        for col in column_list
    ]
    return dict(zip(column_list, new_column_list))


def get_model(function: str) -> Callable:
    """Simple redirection to get named function from model.py."""
    return getattr(model, function)


def get_post(function: str) -> Callable:
    """Simple redirection to get named function from post.py."""
    return getattr(post, function)


def load_model_config(model_config_path: str) -> Dict[str, Any]:
    """Loads model config, either from yaml or json format."""
    config_path = Path(model_config_path)
    if config_path.suffix == ".yaml":
        return yaml.safe_load(config_path.open())
    elif config_path.suffix == ".json":
        return json.load(config_path.open())
    else:
        raise ValueError(f"Unsupported config file type {model_config_path}")


def get_model_path(model_config: Dict[str, Any]) -> Path:
    """Returns the model path from config file."""
    return Path(config.default_model_folder, model_config["run_name"])


def create_model_folder(model_config: Dict[str, Any]) -> None:
    """Create model asset folder and write config if it doesn't exist."""
    model_path = get_model_path(model_config)
    if model_path.exists():
        return None
    else:
        model_path.mkdir()
        config = Path(model_path, "config.json")
        with open(config, "w") as f:
            json.dump(model_config, f, indent=4)
