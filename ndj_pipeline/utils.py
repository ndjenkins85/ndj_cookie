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
import argparse
import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List

import pandas as pd
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


def create_tables_html() -> None:
    """Scan schemas directory to create HTML page for data documentation."""
    schema_paths = Path("schemas").glob("*.yaml")

    html = []
    for schema_path in schema_paths:
        logging.info(f"Loading schema from {schema_path}")
        with open(schema_path, "r") as f:
            schema = yaml.safe_load(f)

        table_name = f"<h1>{schema_path.stem.title()}</h1>"
        html.append(table_name)
        table_comment = schema.get("comment", "")
        html.append(table_comment)
        table_html = parse_schema_to_table(schema)
        html.append(table_html)

    output_path = Path("docs", "data_dictionary.html")
    logging.info(f"Saving data dictionary to {output_path}")

    html = "\n<p>\n".join(html)

    with open(output_path, "w") as f:
        f.write(html)


def parse_schema_to_table(schema: Dict[str, Any]) -> str:
    """Parses a table schema into a HTML table for use in documentation."""
    data = pd.DataFrame.from_dict(schema["columns"], orient="index")
    data.index.name = "name"

    data["comment"] = data["comment"].str.replace(r"\n", "")

    data = data.drop(["coerce", "required"], axis=1)
    data[["nullable", "allow_duplicates"]] = data[["nullable", "allow_duplicates"]].replace({True: "✓", False: "✗"})

    html = data.reset_index().to_html(index=False, na_rep="", classes="docutils align-default")
    return html


def main() -> None:
    """Run selected utility function

    Can be run from command line using...
    `python -m ndj_pipeline.utils --tables`
    """
    parser = argparse.ArgumentParser(description="ndj_cookie utils")
    parser.add_argument("--tables", action="store_true", help="Create html tables")
    parser.add_argument("-v", action="store_true", help="Debug mode")

    args = parser.parse_args()
    log_level = logging.DEBUG if args.v else logging.INFO
    log_path = Path("logs", "_log.txt")

    try:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
        )
    except FileNotFoundError:
        msg = f"""Directory '{log_path}' missing, cannot create log file.
                  Make sure you are running from base of repo, with correct data folder structure.
                  Continuing without log file writing."""
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.warning(msg)

    if args.tables:
        logging.info(f"Running html table creation for data dictionary")
        create_tables_html()


if __name__ == "__main__":
    main()
