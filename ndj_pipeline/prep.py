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

"""Config driven preprocessing functions used in model pipeline."""
import argparse
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tts

from ndj_pipeline import utils


def apply_filtering(df, model_config):
    """Filters a dataframe given a config containing list of filter strings.

    Expects a '_filter' column in the processed data.
    Any string mentioned in 'filters' config, which is found in `_filter` column results in row exclude.

    Raises:
        ValueError: Expects '_filter' column in processed data.
    """
    if "_filter" not in df.columns:
        raise ValueError("Expects `_filter` column in processed data.")

    if not model_config.get("filters", []):
        logging.debug("No filter conditions from config, passing")
        return df

    master_filter = pd.Series(0, index=df.index)
    for _filter in model_config.get("filters", []):
        master_filter = master_filter | df["_filter"].str.contains(_filter)
    master_filter = ~master_filter

    logging.info(f"Applying filters {model_config.get('filters', [])} to dataset, pre shape {df.shape}")
    df = df.loc[master_filter]
    logging.info(f"Post filter shape {df.shape}")
    return df


def create_compressed_dummies(df, dummy, min_dummy):
    """Given dataframe, column specification and minimum percentage, create dummy info.
    If any of the resulting dummy columns does not match minimum percentage, group into an 'other' category.
    Returns dummy frame and col list."""
    # Added cleaning to avoid weird characters in string
    df[dummy] = df[dummy].astype(str)
    values = list(df[dummy].unique())
    df[dummy] = df[dummy].replace(utils.clean_column_names(values))

    raw_dummies = pd.get_dummies(df[dummy], prefix=f"{dummy}_##")
    dummies_min_test = raw_dummies.mean() < min_dummy

    insufficient = dummies_min_test[dummies_min_test].index
    sufficient = dummies_min_test[~dummies_min_test].index

    selected_dummies = raw_dummies[sufficient]
    selected_dummies[f"{dummy}_##_other_combined"] = (raw_dummies[insufficient].sum(axis=1) > 0).astype(int)
    return selected_dummies, selected_dummies.columns.tolist()


def create_dummy_features(df, model_config):
    """Iterate through dummy features and add to dataset."""
    dummy_features = []
    min_dummy = model_config.get("min_dummy_percent", 0.001)
    for col in model_config.get("dummy_features", []):
        _features, _cols = create_compressed_dummies(df, col, min_dummy)
        df = df.join(_features)
        dummy_features += _cols
    return df, dummy_features


def filter_target(df, model_config):
    """Ensure no missing data in target variable."""
    logging.info(f"Original data size {df.shape}")
    df = df.dropna(subset=[model_config["target"]])
    logging.info(f"Dropped target size {df.shape}")
    return df


def split(df, model_config):
    """Create train test split using model config.

    Can use pre-calculated column from processed data, or sklearn style split params, (or no split).
    """
    split_params = model_config.get("split", {})
    split_field = split_params.get("field", None)

    if split_field:
        logging.info(f"Splitting sample at using existing {split_field} column")
        train = df.loc[df[split_field] == 1]
        test = df.loc[df[split_field] == 0]
    elif split_params:
        logging.info("Splitting sample at random")
        train, test = tts(df, **split_params)
    else:
        logging.warning("No test set specified")
        train = df
        test = pd.DataFrame(columns=df.columns)

    logging.info(f"Training size: {train.shape}, Test size: {test.shape}")

    return train, test


def get_simple_feature_averages(df, model_config):
    """Validates config specified aggregations then calculate values from data."""
    simple_features_agg = model_config.get("simple_features", {})

    # Validate to ensure no features contain infinity
    problems = []
    for feature in simple_features_agg:
        logging.debug(f"{feature} has {str(df[feature].dtype)}")
        isinf = df[feature].dropna().apply(np.isinf)
        if isinf.any():
            problems.append(feature)
    if problems:
        raise ValueError(f"One or more features contains -inf/inf, fix these; {', '.join(problems)}")

    agg = df.agg(simple_features_agg)
    try:
        agg = agg.loc[0]
    except KeyError:
        logging.debug("No 'mode' values detected in aggregations")

    aggregates = pd.Series(agg, name="aggregates")

    model_path = utils.get_model_path(model_config)
    output_path = Path(model_path, "calc_train_aggregates.csv")
    logging.info(f"Saving to: {output_path}")
    pd.DataFrame(aggregates).to_csv(output_path)

    return aggregates


def apply_feature_averages(df, aggregates, model_config):
    """Validates and applies feature averages to a dataframe."""
    try:
        df[aggregates.index] = df[aggregates.index].fillna(aggregates)
        return df
    except:
        # If there is a problem, try one by one and report.
        problems = []
        for col, agg in aggregates.items():
            try:
                df[col].fillna(agg)
            except TypeError:
                problems.append(col)
        if problems:
            raise ValueError(f"These features set to mean replace, should probably be mode {', '.join(problems)}")


def save_data(train, test, model_config):
    """Optionally save train, test and combined datasets to experiment folder."""
    model_path = utils.get_model_path(model_config)

    output_path = Path(model_path, "prep_train.parquet")
    logging.info(f"Saving to: {output_path}")
    train.to_parquet(output_path)

    output_path = Path(model_path, "prep_test.parquet")
    logging.info(f"Saving to: {output_path}")
    test.to_parquet(output_path)

    output_path = Path(model_path, "prep_train_test.parquet")
    logging.info(f"Saving to: {output_path}")
    pd.concat([train, test]).sort_index().to_parquet(output_path)


def collate_features(model_config, dummy_features):
    """Creates list of simple and dummy features."""
    simple_features = list(model_config.get("simple_features", {}).keys())
    features = simple_features + dummy_features
    logging.info(
        f"""
        "Model uses {len(simple_features)} simple features and
        {len(dummy_features)} dummy features
        for {len(features)} features total"
    """
    )
    return features
