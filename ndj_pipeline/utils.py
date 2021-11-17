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

import yaml

from ndj_pipeline import config, model, post


def clean_column_names(column_list):
    """Simple string cleaning rules for columns."""
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


def get_model(function):
    """Simple redirection to get named function."""
    return getattr(model, function)


def get_post(function):
    """Simple redirection to get named function."""
    return getattr(post, function)


def load_model_config(model_config_path):
    """Loads model config, either from yaml or json format."""
    config_path = Path(model_config_path)
    if config_path.suffix == ".yaml":
        return yaml.safe_load(config_path.open())
    elif config_path.suffix == ".json":
        return json.load(config_path.open())
    else:
        raise ValueError(f"Unsupported config file type {model_config_path}")


def get_model_path(model_config):
    return Path(config.default_model_folder, model_config["run_name"])


def get_inference_model_path(model_config):
    return Path(*model_config.get("model_folder"))


def create_model_folder(model_config):
    """Simple def to create asset folder for model."""
    model_path = get_model_path(model_config)
    if model_path.exists():
        return None
    else:
        model_path.mkdir()
        config = Path(model_path, "config.json")
        with open(config, "w") as f:
            json.dump(model_config, f, indent=4)
