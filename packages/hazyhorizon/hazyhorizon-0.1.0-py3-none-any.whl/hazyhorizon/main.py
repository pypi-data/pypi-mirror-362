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


import numpy as np
import pandas as pd


def rolling_variation_coefficients(
    x: pd.Series | np.ndarray, n: int = -2, ddof: int = 1, return_array: bool = False
) -> pd.Series | np.ndarray:
    """
    Calculate the rolling coefficient of variation over a time series.

    The coefficient of variation is defined as the ratio of the rolling standard deviation 
    to the rolling mean. This function supports both backward-looking and forward-looking 
    rolling windows.

    Parameters
    ----------
    x : pd.Series or np.ndarray
        Input time series data.
    n : int, default=-2
        Window size for the rolling calculation. If positive, a forward-looking window is used.
        If negative, a backward-looking window of size `abs(n)` is used.
    ddof : int, default=1
        Delta degrees of freedom for standard deviation calculation.
    return_array : bool, default=False
        If True, returns a NumPy array. If False, returns a pandas Series.

    Returns
    -------
    pd.Series or np.ndarray
        Rolling coefficient of variation. The type depends on the `return_array` flag.

    Notes
    -----
    - Forward-looking windows use `pd.api.indexers.FixedForwardWindowIndexer`, which requires 
      pandas 1.3.0 or newer.
    - NaN values will appear at the beginning or end of the result depending on the window direction.

    Examples
    --------
    >>> import pandas as pd
    >>> data = pd.Series([1, 2, 3, 4, 5])
    >>> rolling_variation_coefficients(data, n=-2)
    0         NaN
    1    0.353553
    2    0.353553
    3    0.353553
    4         NaN
    dtype: float64
    """
    if not isinstance(x, pd.Series):
        x = pd.Series(x)

    if n > 0:
        # indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=n)
        # rolling = x.rolling(indexer)
        rolling = x.rolling(pd.api.indexers.FixedForwardWindowIndexer(window_size=n))
    else:
        n = abs(n)
        rolling = x.rolling(n)

    coefficients = rolling.std(ddof=ddof) / rolling.mean()

    return coefficients.to_numpy() if return_array else coefficients


def outlier_indicators(
    x: pd.Series | np.ndarray,
    n: int = 2,
    ddof: int = 1,
    n_left: int | None = None,
    n_right: int | None = None,
    ddof_left: int | None = None,
    ddof_right: int | None = None,
    return_array: bool = False
) -> pd.Series | np.ndarray:
    """
    Compute outlier indicators based on the minimum of rolling variation coefficients from both left and right directions.

    This function calculates rolling variation coefficients (standard deviation divided by mean)
    over a window of size `n` (or `n_left` and `n_right` if specified) and returns the minimum
    of the left and right variation scores for each point in the input series or array.
    These scores can be used as indicators of potential outliers.

    Parameters
    ----------
    x : pd.Series or np.ndarray
        Input data series or array.
    n : int, optional
        Default window size for both directions if `n_left` and `n_right` are not specified.
        Default is 2.
    ddof : int, optional
        Delta degrees of freedom for standard deviation calculation. Default is 1.
    n_left : int or None, optional
        Window size for the left-side rolling variation. Defaults to `-n`.
    n_right : int or None, optional
        Window size for the right-side rolling variation. Defaults to `n`.
    ddof_left : int or None, optional
        Degrees of freedom for left-side variation. Defaults to `ddof`.
    ddof_right : int or None, optional
        Degrees of freedom for right-side variation. Defaults to `ddof`.
    return_array : bool, optional
        If True, returns a NumPy array; otherwise, returns a pandas Series. Default is False.

    Returns
    -------
    pd.Series or np.ndarray
        Outlier indicator scores. Lower values may indicate potential outliers.
    """
    if n_left is None:
        n_left = -n
    if n_right is None:
        n_right = n
    if ddof_left is None:
        ddof_left = ddof
    if ddof_right is None:
        ddof_right = ddof

    # if not isinstance(x, pd.Series):
    #     x = pd.Series(x)
    # left_scores = rolling_variation_coefficients(
    #     x, n=n_left, ddof=ddof_left, return_array=True
    # )
    # right_scores = rolling_variation_coefficients(
    #     x, n=n_right, ddof=ddof_right, return_array=True
    # )
    # outlier_scores = np.minimum(left_scores, right_scores)
    # 
    # return scores if return_array else pd.Series(scores, index=x.index)

    scores = np.fmin(
        rolling_variation_coefficients(x=x, n=n_left, ddof=ddof_left, return_array=True),
        rolling_variation_coefficients(x=x, n=n_right, ddof=ddof_right, return_array=True)
    )

    if return_array is False:
        scores = pd.Series(scores)
        if isinstance(x, pd.Series):  # if type(x) == pd.Series:
            scores.index = x.index.copy()

    return scores


def rolling_window(x: pd.Series | np.ndarray, window: int = 3) -> np.ndarray:
    """
    Create a rolling window view of the input array or Series.

    This function returns a view of the input data with overlapping windows of a specified size.
    It uses NumPy's stride tricks to avoid copying data, making it efficient for large arrays.
    The resulting array has shape `(len(x) - window + 1, window)`.

    Parameters
    ----------
    x : pd.Series or np.ndarray
        Input data. If a pandas Series is provided, its underlying NumPy array is used.
    window : int, optional
        Size of the rolling window. Must be less than or equal to the length of `x`. Default is 3.

    Returns
    -------
    np.ndarray
        A 2D array where each row is a rolling window of the input data.

    Notes
    -----
    This function does not pad the input. The output will have `len(x) - window + 1` rows.
    It uses `np.lib.stride_tricks.as_strided`, which returns a view, not a copy. Be cautious
    when modifying the output. TODO: Review this note.

    References
    ----------
    https://stackoverflow.com/questions/48883784/pandas-rolling-values

    Examples
    --------
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 3, 4, 5])
    >>> rolling_window(s, window=3)
    array([[1, 2, 3],
           [2, 3, 4],
           [3, 4, 5]])
    """
    # TODO: Consider using only a view. Drop support for pandas Series if necessary.
    # if isinstance(x, pd.Series):
    #     a = x.to_numpy()
    # else:
    #     a = x.copy()
    a = x.to_numpy() if isinstance(x, pd.Series) else x.copy()

    if not isinstance(a, np.ndarray):
        raise TypeError("Input must be a pandas Series or a NumPy array.")

    if window <= 0:
        raise ValueError("Window size must be a positive integer.")
    if window > len(x):
        raise ValueError("Window size must be less than or equal to the length of the input data.")

    # TODO: Review support for multi-dimensional arrays.

    # 1D version:
    # shape = (len(a) - window + 1, window)
    # strides = a.strides * 2

    # General version for any number of dimensions:
    # a = np.concatenate([[np.nan] * (window - 1), a, [np.nan] * (window - 1)])
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)

    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def two_way_averages(
    x: pd.Series | np.ndarray,
    n: int = 2,
    pandas_stat: str = "mean",
    n_left: int | None = None,
    n_right: int | None = None,
    return_array: bool = False,
    skipna: bool = False,
) -> pd.Series | np.ndarray:
    """
    Compute two-sided rolling statistics over a 1D array or Series.

    This function calculates a centered rolling statistic (e.g., mean, median) over a window
    that includes `n_left` elements before and `n_right` elements after each point. The
    statistic is computed using pandas' DataFrame methods and supports NaN skipping.

    Parameters
    ----------
    x : pandas.Series or numpy.ndarray
        Input 1D data.
    n : int, optional
        Default number of elements to include on each side of the center. Used if `n_left`
        or `n_right` are not specified. Default is 2.
    pandas_stat : str, optional
        Name of the pandas statistical method to apply (e.g., "mean", "median", "std").
        Default is "mean".
    n_left : int or None, optional
        Number of elements to include to the left of each point. Defaults to `n`.
    n_right : int or None, optional
        Number of elements to include to the right of each point. Defaults to `n`.
    return_array : bool, optional
        If True, returns a NumPy array; otherwise, returns a pandas Series. Default is False.
    skipna : bool, optional
        Whether to skip NaN values when computing the statistic. Default is False.

    Returns
    -------
    pandas.Series or numpy.ndarray
        The computed rolling statistic for each point in the input. The output is aligned
        with the original index if the input was a Series and `return_array` is False.

    Notes
    -----
    - The function pads the input with NaNs on both sides to allow centered windowing.
    - The rolling operation is implemented using a custom `rolling_window` function and
      pandas DataFrame methods.
    - If `skipna` is False, NaNs in the window will result in NaN outputs.

    Examples
    --------
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 3, 4, 5])
    >>> two_way_averages(s, n=1)
    0    1.5
    1    2.0
    2    3.0
    3    4.0
    4    4.5
    dtype: float64
    """
    # TODO: Include support for other statistics like weighted averages or exponential smoothing.

    # averages = getattr(x, pandas_stat)()
    # averages = x.rolling(pd.api.indexers.FixedForwardWindowIndexer(window_size=n)).mean()
    # averages = getattr(x.rolling(pd.api.indexers.FixedForwardWindowIndexer(window_size=n)), pandas_stat)()

    if n_left is None:
        n_left = n
    if n_right is None:
        n_right = n

    # if not isinstance(x, pd.Series):
    #     x = pd.Series(x)
    if isinstance(x, pd.Series):
        a = x.to_numpy()
    else:
        a = x.copy()

    # Pad the input with NaNs on both sides:
    # padded_x = pd.Series(np.concatenate([[np.nan] * n_left, x.to_numpy(), [np.nan] * n_right]))
    a = np.concatenate([[np.nan] * n_left, a, [np.nan] * n_right])

    # Create rolling windows:
    # windows = rolling_window(padded_x, window=n_left + n_right + 1)
    windows = rolling_window(a, window=n_left + n_right + 1)

    # Convert to DataFrame for easier statistical calculations:
    windows = pd.DataFrame(windows)

    # Apply the specified pandas statistic:
    averages = getattr(windows, pandas_stat)(axis=1, skipna=skipna)
    if isinstance(x, pd.Series) and not return_array:
        # averages = pd.Series(averages, index=x.index.copy())
        averages.index = x.index.copy()  

    return averages.to_numpy() if return_array else averages


def clip_outliers(
    x: pd.Series,
    q: float = 99.9,
    n: int = 2,
    n_averaging: int = 2,
    outlier_threshold: float = 0.05,
    ddof: int = 1,
    average: str = "mean",
    n_left: int | None = None,
    n_right: int | None = None,
    n_averaging_left: int | None = None,
    n_averaging_right: int | None = None,
    ddof_left: int | None = None,
    ddof_right: int | None = None,
    return_array: bool = False,
    skipna: bool = False,
) -> pd.Series | np.ndarray:
    """
    Detect and smooth outliers in a time series using rolling variation and two-way averaging.

    This function identifies outliers based on local variation coefficients and smooths them
    by interpolating and adjusting values that deviate significantly from a two-sided rolling
    average. It is designed for use with time-indexed pandas Series.

    Parameters
    ----------
    x : pandas.Series
        Input time series data.
    q : float, optional
        Quantile threshold (in percent) for determining extreme deviations. Default is 99.9.
    n : int, optional
        Window size for computing variation coefficients. Default is 2.
    n_averaging : int, optional
        Window size for computing the two-way rolling average. Default is 2.
    outlier_threshold : float, optional
        Threshold for the variation coefficient above which a point is considered an outlier. Default is 0.05.
    ddof : int, optional
        Delta degrees of freedom for standard deviation in variation coefficient. Default is 1.
    average : str, optional
        Statistical method to use for averaging (e.g., "mean", "median"). Default is "mean".
    n_left : int or None, optional
        Left window size for variation coefficient. Defaults to `-n`.
    n_right : int or None, optional
        Right window size for variation coefficient. Defaults to `n`.
    n_averaging_left : int or None, optional
        Left window size for averaging. Defaults to `n_averaging`.
    n_averaging_right : int or None, optional
        Right window size for averaging. Defaults to `n_averaging`.
    ddof_left : int or None, optional
        Left-side degrees of freedom for variation. Defaults to `ddof`.
    ddof_right : int or None, optional
        Right-side degrees of freedom for variation. Defaults to `ddof`.
    return_array : bool, optional
        If True, returns a NumPy array; otherwise, returns a pandas Series. Default is False.
    skipna : bool, optional
        Whether to skip NaNs when computing the rolling average. Default is False.

    Returns
    -------
    pandas.Series or numpy.ndarray
        The input series with outliers smoothed or adjusted. Output type matches `return_array`.

    Notes
    -----
    - The function uses time-based interpolation to fill missing values before and after outlier detection.
    - Outliers are identified using a combination of local variation and deviation from a rolling average.
    - Detected outliers are adjusted by clipping their deviation to a quantile-based threshold.

    Examples
    --------
    >>> import pandas as pd
    >>> s = pd.Series([1, 2, 100, 4, 5], index=pd.date_range("2023-01-01", periods=5))
    >>> remove_outliers(s)
    2023-01-01     1.0
    2023-01-02     2.0
    2023-01-03    4.95
    2023-01-04     4.0
    2023-01-05     5.0
    dtype: float64
    """
    # TODO: Let me know if you'd like to generate a version that works with NumPy arrays
    # # directly or supports plotting the outlier detection process!

    x_copy = x.copy()
    x_copy_interpolated = x.interpolate(method="time", limit_area="inside")
    # output = pd.Series(output)

    indicators = outlier_indicators(
        x=x_copy_interpolated,
        n=n,
        ddof=ddof,
        n_left=n_left,
        n_right=n_right,
        ddof_left=ddof_left,
        ddof_right=ddof_right,
        # return_array=return_array,
        return_array=False,
    )
    # f = indicators >= outlier_threshold
    # x_copy[f] = np.nan
    x_copy[indicators >= outlier_threshold] = np.nan

    # TODO: Add the time method fallback for when output is ndarray:
    x_copy = x_copy.interpolate(method="time", limit_direction="both")

    # if skipna is False:
    x_copy[np.isnan(x)] = np.nan
    # x_copy.plot(figsize=(20, 8))

    averages = two_way_averages(
        x=x_copy,
        n=n_averaging,
        pandas_stat=average,
        n_left=n_averaging_left,
        n_right=n_averaging_right,
        return_array=False,
        skipna=skipna,
    )
    averages.fillna(x_copy, inplace=True)  # type: ignore  # TODO: Add support for ndarray output.
    # averages.plot(figsize=(20, 8))
    # differences = x_copy_interpolated - averages
    differences = x - averages
    absolute_differences = np.abs(differences)  # np.abs(x - averages)
    # absolute_differences.plot(figsize=(20, 8))
    quantile = np.percentile(a=pd.Series(absolute_differences).dropna(), q=q)
    # print(quantile)

    output = x.copy()
    # output = pd.Series(output)
    f0 = absolute_differences >= quantile
    f1 = f0 & (differences > 0)
    f2 = f0 & (differences < 0)
    output[f1] -= (differences[f1] - quantile) # type: ignore
    output[f2] -= (differences[f2] + quantile)

    # (x - output).hist(bins=50)

    if return_array is True:
        output = output.to_numpy()
    elif isinstance(x, pd.Series):
        output.index = x.index.copy()

    return output


def adjust_forecast(
    forecast: pd.DataFrame,
    f0,
    f1,
    columns_to_adjust: list,
    # historical_data: pd.DataFrame,
    trend_ceiling_multiplier: float | None = None,
    trend_floor_multiplier: float | None = None,
    lower_clip: float | None = None,
    minimum_threshold: float | None = None,
) -> pd.DataFrame:
    """Clip the forecasts by placing upper and lower limits on the underlying trend.

    TODO: Add docstring.
    TODO: Add parameters: f0, f1; use forecast.copy(); general refactoring.
    """
    forecast["trend_delta"] = 0.0
    if trend_ceiling_multiplier is None and trend_floor_multiplier is None:
        if lower_clip is not None:
            forecast.loc[f0, "trend_delta"] = forecast["trend"].clip(lower=lower_clip) - forecast["trend"]
        else:
            forecast.loc[f0, "trend_delta"] = 0
    else:
        trend_ceiling_multiplier = 1 if trend_ceiling_multiplier is None else trend_ceiling_multiplier
        trend_floor_multiplier = 0 if trend_floor_multiplier is None else trend_floor_multiplier
        forecast.loc[f0, "trend_delta"] = forecast["trend"].clip(
            lower=forecast.loc[f1, "trend"] * trend_floor_multiplier, # type: ignore
            upper=forecast.loc[f1, "trend"] * trend_ceiling_multiplier, # type: ignore
        ) - forecast["trend"]
    for c in columns_to_adjust:  # TODO: Try instead: `forecast[columns_to_adjust].add(forecast["trend_delta"], axis=0)`.
        forecast[c] += forecast["trend_delta"]
        if lower_clip is not None:
            forecast[c].clip(lower=lower_clip, inplace=True)
    # forecast.set_index("ds", inplace=True)
    # forecast["y"] = historical_data.set_index("ds")["y"]
    if minimum_threshold is not None:  # TODO: Implement it more accurately, considering 1-day and 2-day cycles (2-day rolling sum?).
        forecast[forecast["y"].isna() & (forecast["yhat"] < minimum_threshold)] = np.nan  # TODO: Refactoring, e.g., other values as a parameter.
    return forecast


def get_tunnel_scaler(
        X: np.ndarray | pd.Series,
        lower_limit: np.ndarray | float,
        upper_limit: np.ndarray | float,
) -> np.ndarray | pd.Series:
    """Get a scaling multiplication array for scaling to a trend tunnel.

    TODO: Add docstring.
    TODO: Check if works with 2D arrays and pd.DataFrame.
    """
    # limit_span = upper_limit - lower_limit
    array_span = X.max(axis=0) - X.min(axis=0)
    normalised_array = (X - X.min(axis=0)) / array_span
    scaled_array = normalised_array * (upper_limit - lower_limit) + lower_limit
    return scaled_array / X


def add_investment_yields(
    forecast: pd.DataFrame,
    f0,
    f1,
    columns_to_adjust: list,
    annual_delta,
) -> pd.DataFrame:
    """TODO: Add docstring."""
    forecast["yield_delta"] = np.nan
    # forecast.loc[~f0.to_numpy(), "yield_delta"] = 0
    forecast.loc[~f0, "yield_delta"] = 0
    anniversary = forecast.index[f1] + pd.Timedelta(366, "d")
    forecast.loc[anniversary, "yield_delta"] = annual_delta  # TODO: Refactoring.
    forecast.loc[forecast.index[-1], "yield_delta"] = annual_delta * f0.sum() / 365.25
    forecast["yield_delta"].interpolate(method="time", inplace=True)

    for c in columns_to_adjust:
        forecast[c] += forecast["yield_delta"]
        forecast[c].clip(lower=0, inplace=True)

    return forecast


def round_to_base(x: np.ndarray | float, base: int = 1) -> np.ndarray | float:
    """
    Round numbers to the nearest base.

    Parameters
    ----------
    x (numpy array or scalar): The number(s) to be rounded.
    base (int): The base to which to round the numbers. Default is 1.

    Returns
    -------
    numpy array or scalar: The rounded number(s).
    """
    return base * np.round(x / base)


def round_up_to_base(x: np.ndarray | float, base: int = 1) -> np.ndarray | float:
    """
    Round up numbers to the nearest base.

    Parameters
    ----------
    x (numpy array or scalar): The number(s) to be rounded.
    base (int): The base to which to round the numbers up.

    Returns
    -------
    numpy array or scalar: The rounded number(s).
    """
    return base * np.ceil(x / base)


def skewness(x: pd.Series | np.ndarray, periods_to_check: int = 731, quantile_fraction: float = 0.25):
    """
    Calculate the skew of the specified data.

    Parameters
    ----------
    x (pd.Series or np.ndarray): The data to calculate the skew for.
    temp_df (DataFrame): The DataFrame containing the data.
    periods_to_check (int): The number of days to check. Default is 731.
    quantile_fraction (float): The fraction to determine the quantile. Default is 0.25.

    Returns
    -------
    float: The skew of the specified data.
    """
    # TODO: Add output type hint.
    temp_s = pd.Series(x).iloc[-periods_to_check:].dropna()
    length = temp_s.size
    quantile = int(np.round(length * quantile_fraction, 0))

    return temp_s.nlargest(length - quantile).tail(length - 2 * quantile).skew()


def YoY_dynamics(time_series, unit: str = "month", time_index: str = "ds") -> pd.Series:
    """TODO: Include `time_index` input as array; typing, -1 replacement, `dropna`."""
    if type(time_index) is str:
        data = time_series.reset_index(drop=False)
    else:
        raise Exception("Not implemented.")

    if unit == "year":
        data[time_index] = data[time_index].dt.year
        shift_periods = 1
    elif unit == "quarter":
        data[time_index] = data[time_index] - pd.Timedelta(1, "d") + pd.offsets.QuarterEnd()
        shift_periods = 4
    elif unit in ["month", None]:
        data[time_index] = data[time_index] - pd.Timedelta(1, "d") + pd.offsets.MonthEnd()
        shift_periods = 12
    else:
        raise Exception("Not implemented.")

    data = data.groupby(time_index, dropna=False).sum()
    # display(data.shift(periods=shift_periods))

    return ((data / data.shift(periods=shift_periods)) - 1).replace(-1, np.nan).dropna(how="all")
