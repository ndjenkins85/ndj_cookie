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

"""Data transformations (ETL) from raw (checked) files into single, feature rich dataframe.

Can be run from command line, or as imported functions in other python
scripts and jupyter notebooks."""
import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from ndj_pipeline import data_checks


def create_titanic_features(df):
    """Creates some basic features from titanic data."""
    # Example of custom filter
    df["_filter"] = ""
    df.loc[0, "_filter"] = "remove_me"
    df.loc[1, "_filter"] = "remove_me, condition_2"

    # Example of custom split field for men vs women; excludes other titles
    df["my_split_field"] = np.nan
    # Single men
    df.loc[df["name"].str.lower().str.contains("mr."), "my_split_field"] = 1
    # Vs women, or / and accompanying men
    df.loc[df["name"].str.lower().str.contains("mrs"), "my_split_field"] = 0

    output_path = Path("data", "processed", "titanic.parquet")
    logging.info(f"Saving data to {output_path}")
    df.to_parquet(output_path)


def run():
    """Perform all data transformation steps."""
    df = data_checks.check_titanic()
    create_titanic_features(df)


def main():
    """Run transformations from command line using...`
    python -m ndj_pipeline.transform
    `
    """
    parser = argparse.ArgumentParser(description="ndj_pipeline transformations")
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

    run()


if __name__ == "__main__":
    main()
