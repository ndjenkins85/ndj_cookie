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

"""Schemas and assertions for raw data inputs.
Schema checks are useful to standardize certain information in raw data including:

* Clean column names (lowercase, underscore)
* Ensure an understanding of primary keys of data (uniqueness)
* Set data types of columns, i.e. boolean->int, datetime, string, nullable integer
* Pandera schema checks to attempt to lock some checks about a datafile. This helps
  to quickly assess if a file has changed, or a similar file is same or different.
  Some examples:

  * Contains exact list of columns (no more no less)
  * Nullable column
  * Data type correct
  * Data range checks (must not be 0 or less, must contain only these values)

Schemas can often be re-applied to similar data files, i.e. tabs of an excel, or train/test data.
"""
import logging
from pathlib import Path

import pandas as pd
import pandera as pa
from pandera import io

from ndj_pipeline import utils


def check_titanic() -> pd.DataFrame:
    """Data schema and typing validations.

    Returns:
        Loaded pandas dataframe with typing and schema checks.
    """
    # Standardize column names
    input_path = Path("data", "titanic.csv")
    logging.info(f"Loading data from {input_path}")
    df = pd.read_csv(input_path)

    df = df.rename(columns=utils.clean_column_names(df))

    # Checks for duplicates
    assert df.shape == df.drop_duplicates().shape

    # Recoding of string variables
    df["sex"] = df["sex"].replace({"male": 1, "female": 0}).astype("Int64")

    # Full expressive list of variables, assumptions and questions
    schema_path = Path("schemas", "titanic.yaml")
    with open(schema_path, "r") as f:
        pandera_schema_check = io.from_yaml(f)
    df = pandera_schema_check.validate(df)
    logging.info("Validation checks passed")
    return df
