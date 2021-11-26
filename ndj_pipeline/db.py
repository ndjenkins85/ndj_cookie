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

"""Standalone module to assist database creation and querying.

Useful for practicing SQL techniques and scripts.
"""
import logging
import sqlite3
from pathlib import Path

import pandas as pd

from ndj_pipeline import config


def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a sqlite DB connection."""
    logging.info(f"Connecting to database at {config.database_path}")
    conn = sqlite3.connect(config.database_path)
    return conn


def create_db() -> None:
    """Converts processed titanic data into an SQLite3 DB."""
    conn = get_db_connection()

    input_path = Path("data", "processed", "titanic.parquet")
    logging.info(f"Loading data from {input_path}")
    data = pd.read_parquet(input_path)

    logging.info(f"Saving data to {config.database_path}")
    data.to_sql("titanic", conn, if_exists="replace", index_label="id")


def query_db(sql_string: str) -> pd.DataFrame:
    """Query the titanic database and return pandas dataframe."""
    with get_db_connection() as conn:
        df = pd.read_sql(sql_string, conn)
    return df
