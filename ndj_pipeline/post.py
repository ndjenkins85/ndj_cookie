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

"""Post-model fit reporting of results as plots, summary tables and documentation. NJ."""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score

from ndj_pipeline import utils

# Hack to get plots working correctly on command line
try:
    if get_ipython().__class__.__name__ == "ZMQInteractiveShell":  # type: ignore
        logging.debug("Running with ipython support")
except NameError:
    logging.debug("ipython not detected, setting matplotlib backend")
    matplotlib.use("agg")

five_thirty_eight = [
    "#30a2da",
    "#fc4f30",
    "#e5ae38",
    "#6d904f",
    "#8b8b8b",
]

sns.set_palette(five_thirty_eight)
sns.set(rc={"figure.figsize": (8, 5)})


def create_metrics_plot(results: pd.DataFrame, model_config: Dict[str, Any], name: str = "") -> None:
    """Produce metrics and scatterplot for results table.

    No returns; saves assets to model folder.

    Args:
        results: DataFrame with "Actual" and "Prediction" columns
        model_config: Loaded model experiment config
        name: Simple label added to outputs, helpful to distinguish models
    """
    # Metrics
    _r2 = r2_score(results["Actual"], results["Predicted"])
    _mae = mae(results["Actual"], results["Predicted"])
    _mse = mse(results["Actual"], results["Predicted"])

    metrics = {"r2": round(_r2, 2), "mae": round(_mae, 5), "mse": round(_mse, 5)}

    output_path = Path(utils.get_model_path(model_config), "metrics.json")
    with open(output_path, "w") as f:
        json.dump(metrics, f)

    # Plot
    plt.figure()
    plot_fig, plot_ax = plt.subplots()
    logging.debug(f"Creating plot figure {name}")

    metrics_text = ", ".join([f"{name}: {result}" for name, result in metrics.items()])
    title = f"{name} - Predicted {model_config.get('target')} \n {metrics_text}"

    # Done to exclude very wild Predictions from plot, symetrically across the two sets
    lower_clip = model_config.get("plot_min_clip", 0)
    upper_clip = model_config.get("plot_max_clip", 1)
    lower_clip_actual = float(results["Actual"].quantile(lower_clip))
    upper_clip_actual = float(results["Actual"].quantile(upper_clip))
    lower_clip_predicted = float(results["Predicted"].quantile(lower_clip))
    upper_clip_predicted = float(results["Predicted"].quantile(upper_clip))
    lower_clip = min(lower_clip_actual, lower_clip_predicted)
    upper_clip = max(upper_clip_actual, upper_clip_predicted)
    results["Actual"] = results["Actual"].clip(lower=lower_clip, upper=upper_clip)
    results["Predicted"] = results["Predicted"].clip(lower=lower_clip, upper=upper_clip)
    results_min_max = [results.min().min(), results.max().max()]
    line_series = pd.Series(results_min_max, index=results_min_max)

    sns.scatterplot(data=results, x="Actual", y="Predicted", ax=plot_ax).set_title(title)
    sns.lineplot(data=line_series, color="orange", ax=plot_ax)
    logging.debug(f"Plot figure drawn {name}")

    output_path = Path(utils.get_model_path(model_config), f"plots_metrics_{name}.png")
    logging.debug(f"Saving plot to {output_path}")
    plot_fig.savefig(output_path)
    plt.close("all")


def create_univariate_plots(df: pd.DataFrame, reporting_features: List[str], model_config: Dict[str, Any]) -> None:
    """Create scatterplots with linear fit for each feature against target.

    No returns; saves assets to model folder.

    Args:
        df: Full, feature rich dataframe, must contain config specified
          target, and numeric feature columns specified by `reporting_features`
        reporting_features: List of features to produce individual plots
        model_config: Loaded model experiment config
    """
    df[reporting_features] = df[reporting_features].astype(float)

    # Limit sample, if too large this is really slow
    if df.shape[0] > 5000:
        data = df.sample(5000)
    else:
        data = df

    for feature in reporting_features:
        plt.figure()
        plot_fig, plot_ax = plt.subplots()

        title = f"Univariate plot of {model_config['target']} and {feature}"
        sns.regplot(data=data, y=model_config["target"], x=feature, ax=plot_ax).set_title(title)

        # in case <na> comes in from dummy variables
        feature = feature.replace("<", "").replace(">", "")
        output_path = Path(utils.get_model_path(model_config), f"plots_univariate_{feature}.png")
        logging.info(f"Saving to: {output_path}")
        plot_fig.savefig(output_path)
        plt.close("all")


def create_continuous_plots(df: pd.DataFrame, reporting_features: List[str], model_config: Dict[str, Any]) -> None:
    """Create line plot to show how target varies according to feature.

    No returns; saves assets to model folder.

    Args:
        df: Full, feature rich dataframe, must contain config specified
          target, and numeric feature columns specified by `reporting_features`
        reporting_features: List of features to produce individual plots
        model_config: Loaded model experiment config
    """
    df[reporting_features] = df[reporting_features].astype(float)

    for feature in reporting_features:
        plt.figure()
        plot_fig, plot_ax = plt.subplots()

        data = df.groupby(feature)[model_config["target"]].mean()

        title = f"Continuous plot of {model_config['target']} and {feature}"
        sns.lineplot(data=data, ax=plot_ax).set_title(title)

        # in case <na> comes in from dummy variables
        feature = feature.replace("<", "").replace(">", "")
        output_path = Path(utils.get_model_path(model_config), f"plots_continuous_{feature}.png")
        logging.info(f"Saving to: {output_path}")
        plot_fig.savefig(output_path)
        plt.close("all")


def create_correlation_matrix(df: pd.DataFrame, reporting_features: List[str], model_config: Dict[str, Any]) -> None:
    """Create correlation matrix between subset of reported features.

    No returns; saves assets to model folder.

    Args:
        df: Full, feature rich dataframe, must contain config specified
          target, and numeric feature columns specified by `reporting_features`
        reporting_features: List of features to produce individual plots
        model_config: Loaded model experiment config
    """
    plt.figure()

    corr_matrix = df[reporting_features].corr()
    for col in corr_matrix.columns:
        corr_matrix.loc[col, col] = corr_matrix[col].mean()

    # Check for problems
    if corr_matrix.isna().any().any():
        problem = corr_matrix.isna().sum().idxmax()
        logging.warning(f"Problem with at least one feature column {problem}, no variation in corr matrix")
        corr_matrix = corr_matrix.fillna(0)

    plot = sns.clustermap(corr_matrix)

    output_path = Path(utils.get_model_path(model_config), "plots_correlation.png")
    logging.info(f"Saving plot to {output_path}")
    plot.savefig(output_path)
    plt.close("all")
