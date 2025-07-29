# Copyright 2025 Paweł Kranzberg
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pandas as pd
import numpy as np
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    explained_variance_score, max_error
)
# from scipy.stats import pearsonr

# Built-in metric functions
def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, np.nan, y_true))) * 100

def smape(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100

def evaluate_forecast_performance(
        df : pd.DataFrame,
        actual_col : str,
        forecast_col : str,
        metrics : list = ['mean_absolute_error', 'mean_squared_error', 'r2_score'],
        frequency : str = 'M',
        custom_metrics : dict | None = None,
    ):
    """
    Evaluate the performance of a time series forecast against actual values using multiple metrics.

    Parameters
    ----------
    df (pd.DataFrame): DataFrame containing the actual and forecasted values.
    actual_col (str): Column name for actual values.
    forecast_col (str): Column name for forecasted values.
    metrics (list): List of built-in metric names to evaluate.
    frequency (str): Resampling period (e.g., 'M' for monthly, 'W' for weekly). Defaults to monthly ('M').
    custom_metrics (dict): Dictionary of custom metric names and functions to evaluate.

    Returns
    -------
    pd.DataFrame: DataFrame with metrics as columns and periods as rows.
    """
    # Resample the DataFrame based on the specified period:
    df_resampled = df.resample(frequency).mean()

    # Initialize a dictionary to store the results:
    results = {metric: [] for metric in metrics}
    if custom_metrics:
       for metric in custom_metrics:
           results[metric] = []
    results['Period'] = []

    # Iterate over each period:
    # TODO: Time performance vs other iteration methods.
    for period, group in df_resampled.groupby(df_resampled.index):
        y_true = group[actual_col]
        y_pred = group[forecast_col]

        # Calculate each metric and store the result:
        for metric in metrics:
            # if metric == 'mean_absolute_error':
            #     results[metric].append(mean_absolute_error(y_true, y_pred))
            # elif metric == 'mean_squared_error':
            #     results[metric].append(mean_squared_error(y_true, y_pred))
            # elif metric == 'r2_score':
            #     results[metric].append(r2_score(y_true, y_pred))
            # elif metric == 'explained_variance_score':
            #     results[metric].append(explained_variance_score(y_true, y_pred))
            # elif metric == 'max_error':
            #     results[metric].append(max_error(y_true, y_pred))
            # # elif metric == 'pearson_correlation':
            # #     results[metric].append(pearsonr(y_true, y_pred)[0])
            # elif metric == 'mape':
            #     results[metric].append(mape(y_true, y_pred))
            # elif metric == 'smape':
            #     results[metric].append(smape(y_true, y_pred))
            results[metric].append(eval(f"{metric}({y_true}, {y_pred})"))

        if custom_metrics:
            for name, func in custom_metrics.items():
                results[name].append(func(y_true, y_pred))

        # Append the period to the results:
        results['Period'].append(period)

    # Convert the results dictionary to a DataFrame:
    return pd.DataFrame(results)
