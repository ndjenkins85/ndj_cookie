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
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tts

from ndj_pipeline import utils


def load_data_and_key(model_config: Dict[str, Any]) -> pd.DataFrame:
    """Uses config to load data and assign key.

    Args:
        model_config: Loaded model experiment config, specifically for
          data path and index column(s)

    Returns:
        Pandas dataframe with optionally assigned index
    """
    input_path = Path(*model_config["data_file"])
    logging.info(f"Loading parquet from {input_path}")
    data = pd.read_parquet(input_path)

    unique_key = model_config.get("unique_key")
    if unique_key:
        data = data.set_index(unique_key)
        if not data.index.is_unique:
            raise ValueError(f"Config specified key not unique {unique_key}")
    return data


def apply_filtering(df: pd.DataFrame, model_config: Dict[str, Any]) -> pd.DataFrame:
    """Filters dataframe according to config specified labels.

    Any row containing a specified label is filtered from the data.

    Args:
        df: Pandas dataframe, must contain `_filter` column with string type.
        model_config: Loaded model experiment config, specifically for
          list of filter labels.

    Returns:
        Pandas dataframe with optionally assigned index

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


def create_compressed_dummies(df: pd.DataFrame, dummy: str, min_dummy: float) -> Tuple[pd.DataFrame, List[str]]:
    """Creates enhanced feature dummies for a single dataframe column.

    Improves on standard pandas.get_dummies by combining low-incidence dummy columns
      into a single `_other_combined` column. Dummy columns are named according to
      `{col_name}_##_{value}`

    Args:
        df: Pandas dataframe, must contain specified dummy column.
        dummy: string label of DataFrame to create dummy features
        min_dummy: minimum percentage incidence to create standalone
          dummy feature, otherwise group into `_other_combined`.

    Returns:
        Dummified Pandas DataFrame for a single feature.
        Also returns dummy column names as a list of strings.
    """
    # Cleaning steps to avoid weird characters in string
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


def create_dummy_features(df: pd.DataFrame, model_config: Dict[str, Any]) -> Tuple[pd.DataFrame, List[str]]:
    """Create dummy features for each config specified dummy_variable.

    Iterates through all specified dummy features and adds to DataFrame.

    Args:
        df: Pandas dataframe, must contain specified dummy columns.
        model_config: Loaded model experiment config, specifically for
          list of dummy features.

    Returns:
        Pandas DataFrame with original data plus all new dummy fields.
        Also returns full list of created dummy column names
    """
    logging.info("Creating dummy features")
    dummy_features = []
    min_dummy = model_config.get("min_dummy_percent", 0.001)
    for col in model_config.get("dummy_features", []):
        logging.debug(f"Creating dummy features for {col}")
        _features, _cols = create_compressed_dummies(df, col, min_dummy)
        df = df.join(_features)
        dummy_features += _cols
    return df, dummy_features


def filter_target(df: pd.DataFrame, model_config: Dict[str, Any]) -> pd.DataFrame:
    """Filters Dataframe to ensure no missing data in target variable.

    Args:
        df: Pandas dataframe, must contain config specified target colunn.
        model_config: Loaded model experiment config, specifically for
          target column name.

    Returns:
        Filtered Pandas DataFrame.
    """
    logging.info(f"Original data size {df.shape}")
    df = df.dropna(subset=[model_config["target"]])
    logging.info(f"Dropped target size {df.shape}")
    return df


def split(df: pd.DataFrame, model_config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Create train test split using model config.

    Config may specify a pre-calculated column present in the DataFrame,
      or use sklearn style split params. No config results in no split,
      with the creation of an empty test dataframe.

    Args:
        df: Pandas dataframe, must contain a pre-calculated split column
          if this is specified in the `model_config`.
        model_config: Loaded model experiment config, specifically for
          split approach, either a `field` or sklearn style params.

    Returns:
        Two Pandas DataFrames intended for training, test sets.
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


def get_simple_feature_aggregates(df: pd.DataFrame, model_config: Dict[str, Any]) -> pd.Series:
    """Generates config specified feature aggregates.

    These are used to inform missing data replacement strategy. Ideally this is
      run on training data, and used to replace train and test data.

    Performs validations and raises errors as part of process.

    Args:
        df: Pandas dataframe. Must include columns specified in the `simple_features`
          section of config, and these must be numeric type columns with no infinite values.
        model_config: Loaded model experiment config, specifically for
          `simple_features` dictionary of column names and aggregation strategy.

    Returns:
        Pandas Series with specified feature columns: value of aggregation.

    Raises:
        ValueError: If any features contain infinate values that need fixing.
    """
    simple_features_agg = model_config.get("simple_features", {})

    # Validate to ensure no features contain infinity
    problems = []
    for feature in simple_features_agg:
        logging.debug(f"{feature} has {str(df[feature].dtype)}")
        try:
            isinf = df[feature].dropna().apply(np.isinf)
        except TypeError:
            problems.append(feature)
        if isinf.any():
            problems.append(feature)
    if problems:
        raise ValueError(f"One or more features contains -inf/inf, fix these; {', '.join(problems)}")

    agg = df.agg(simple_features_agg)
    try:
        agg = agg.loc[0]  # type: ignore
    except KeyError:
        logging.debug("No 'mode' values detected in aggregations")

    aggregates = pd.Series(agg, name="aggregates")

    model_path = utils.get_model_path(model_config)
    output_path = Path(model_path, "calc_train_aggregates.csv")
    logging.info(f"Saving to: {output_path}")
    pd.DataFrame(aggregates).to_csv(output_path)

    return aggregates


def apply_feature_aggregates(df: pd.DataFrame, aggregates: pd.Series) -> pd.DataFrame:
    """Applies feature aggregates to a DataFrame's missing values.

    Performs validations and raises errors as part of process.

    Args:
        df: Pandas dataframe. Must include same columns as aggregates.
        aggregates: Pandas series with labels and aggregate values.

    Returns:
        Pandas Dataframe with missing data replaced.

    Raises:
        ValueError: If unable to apply aggregation value to a column.
          This is commonly due to the datatypes not working i.e. float into Int64.
    """
    try:
        df[aggregates.index] = df[aggregates.index].fillna(aggregates)
    except BaseException:
        # If there is a problem, try one by one and report.
        problems = []
        for col, agg in aggregates.items():
            try:
                df[col].fillna(agg)
            except TypeError:
                problems.append(col)
        if problems:
            raise ValueError(f"Unable to parse some fields due to type issues {', '.join(problems)}")
    return df


def save_data(train: pd.DataFrame, test: pd.DataFrame, model_config: Dict[str, Any]) -> None:
    """Saves train, test and combined datasets to the model folder as parquet."""
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


def collate_features(model_config: Dict[str, Any], dummy_features: List[str]) -> List[str]:
    """Saves and returns final list of simple and dummy features."""
    simple_features = list(model_config.get("simple_features", {}).keys())
    features = simple_features + dummy_features
    logging.info(
        f"Model uses {len(simple_features)} simple features and"
        + f"{len(dummy_features)} dummy features"
        + f"for {len(features)} features total"
    )
    output_path = Path(utils.get_model_path(model_config), "features.txt")
    logging.info(f"Saving list of features to {output_path}")
    with open(output_path, "w") as f:
        for feature in features:
            f.write(feature)
            f.write("\n")

    return features
