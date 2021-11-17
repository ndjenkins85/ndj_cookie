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

"""Contains custom ML model functions and pipeline for running modeling."""
import argparse
import logging
from pathlib import Path

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

from ndj_pipeline import post, prep, utils

pd.options.mode.chained_assignment = None


def baseline(train, test, features, config):
    """Run naive baseline model."""
    target = config["target"]
    baseline = config.get("baseline", config["target"])
    logging.info("Fitting Baseline model")

    results = pd.DataFrame(test[target])
    results.columns = ["Actual"]
    results["Predicted"] = test[baseline]

    logging.debug("Creating plot")
    post.create_metrics_plot(results, config, name="baseline")

    reporting_features = features
    return None, features


def gbr(train, test, features, config):
    """Run ridge regression and return metrics."""
    model = GradientBoostingRegressor(**config.get("model_params", {}))

    target = config["target"]
    logging.info("Fitting GBR model")
    model.fit(train[features], train[target])
    logging.info("Fit finished GBR model")

    results = pd.DataFrame(test[target])
    results.columns = ["Actual"]
    logging.debug("Predicting results")
    results["Predicted"] = model.predict(test[features])

    logging.debug("Creating plot")
    post.create_metrics_plot(results, config, name="gbr")

    importance_groups_sub = pd.DataFrame(
        pd.Series(dict(zip(features, model.feature_importances_)), name="temp")
    ).reset_index()

    importance_groups_sub = importance_groups_sub.join(
        importance_groups_sub["index"].str.split("_##_", expand=True)
    ).sort_values("temp", ascending=False)
    importance_groups_sub.columns = [
        "feature",
        "importance",
        "feature_group",
        "feature_subgroup",
    ]

    output_path = Path(utils.get_model_path(config), "importance_subgroups.csv")
    logging.info(f"Saving to: {output_path}")
    importance_groups_sub.to_csv(output_path)

    importance_grouped = importance_groups_sub.groupby("feature_group").sum().sort_values("importance", ascending=False)

    output_path = Path(utils.get_model_path(config), "importance.csv")
    logging.info(f"Saving to: {output_path}")
    importance_grouped.to_csv(output_path)

    reporting_features = importance_groups_sub.head()["feature"].to_list()
    return model, reporting_features


def run_model_training(model_config):
    """Run all modeling transformations."""
    # Create resource folder if not exist
    utils.create_model_folder(model_config)

    # Load data
    input_path = Path(*model_config["data_file"])
    logging.info(f"Loading parquet from {input_path}")
    data = pd.read_parquet(input_path)

    # Create dummy features
    data, dummy_features = prep.create_dummy_features(data, model_config)

    # Apply filtering to the filter field, if present in model_config
    data = prep.apply_filtering(data, model_config)

    # Target variable may have missing data; drop all rows with missing
    data = prep.filter_target(data, model_config)

    # Train test split according to config
    train, test = prep.split(data, model_config)

    # Fill missing features (using train) according to config (i.e. mean, mode)
    aggregates = prep.get_simple_feature_averages(train, model_config)
    train = prep.apply_feature_averages(train, aggregates, model_config)
    test = prep.apply_feature_averages(test, aggregates, model_config)

    if model_config.get("save_data"):
        prep.save_data(train, test, model_config)

    # Get features
    features = prep.collate_features(model_config, dummy_features)

    # Train model
    model_function_name = model_config.get("model_function_name")
    if model_function_name:
        model_function = utils.get_model(model_function_name)
        model, reporting_features = model_function(train, test, features, model_config)

    # Produce diagnostic info
    post.create_univariate_plots(train, reporting_features, model_config)
    post.create_correlation_matrix(train, reporting_features, model_config)


def main():
    """Runs either model training or inference depending given command line inputs.
    Can be run using...`
    python -m ndj_pipeline.model -p {path_to_experiment.yaml}
    `
    """
    parser = argparse.ArgumentParser(description="ndj_pipeline model training")
    parser.add_argument("-p", type=str, help="Path to model experiment yaml")
    parser.add_argument("-v", action="store_true", help="Debug mode")

    args = parser.parse_args()

    model_config = utils.load_model_config(args.p)
    utils.create_model_folder(model_config)

    log_level = logging.DEBUG if args.v else logging.INFO
    log_path = Path(utils.get_model_path(model_config), "_log.txt")
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

    logging.info(f"Running in training mode")
    run_model_training(model_config)


if __name__ == "__main__":
    main()
