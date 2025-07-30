# process.py

import math
from typing import Iterable, Callable, Any, Sequence

import numpy as np
import pandas as pd

__all__ = [
    "average_deviation_rate",
    "average_growth_rate",
    "average_win_rate",
    "average_shrink_rate",
    "average_gain_rate",
    "round_decimals_down",
    "weighted_average_win_rate",
    "average_change_rate",
    "cumulative_shrink",
    "cumulative_gain",
    "normalize_calculation",
    "validate_data_length",
    "minimums",
    "maximums",
    "adjust_peaks",
    "peaks",
    "normalize",
    "array",
    "linear_distance_clusters",
    "drop_nan",
    "up_movement",
    "down_movement",
    "spread_deviation_risk_ratio"
]

np.seterr(divide='ignore', invalid='ignore')

def validate_data_length(
        data: Sequence,
        minimum: int = None,
        maximum: int = None
) -> None:
    """
    Validates the length of the data.

    :param data: The data to validate.
    :param minimum: The minimum length.
    :param maximum: The maximum length.
    """

    length = len(data)

    if minimum is None:
        minimum = 0

    if (minimum is not None) and (length < minimum):
        raise ValueError(
            f"Minimum length of {data} is {minimum}, "
            f"but given length is {length}."
        )

    if (maximum is not None) and (length > maximum):
        raise ValueError(
            f"Maximum length of {data} is {maximum}, "
            f"but given length is {length}."
        )

def minimums(data: Iterable[float]) -> np.array:
    """
    Returns an array containing the indexes of the local minimum values.

    :param data: The data to process.

    :return: An array of indexes.
    """

    return (np.diff(np.sign(np.diff(array(data)))) > 0).nonzero()[0] + 1

def maximums(data: Iterable[float]) -> np.array:
    """
    Returns an array containing the indexes of the local maximum values.

    :param data: The data to process.

    :return: An array of indexes.
    """

    return (np.diff(np.sign(np.diff(array(data)))) < 0).nonzero()[0] + 1

def adjust_peaks(
        buy: Iterable[float], sell: Iterable[float]
) -> tuple[np.array, np.array]:
    """
    Processes the minimum and maximum peaks to match the trading process.

    :param buy: The indexes of buying-actions.
    :param sell: The indexes of selling-actions.

    :return: An array of the minimum values indexes and an array of the maximum values indexes.
    """

    buy = array(buy)
    sell = array(sell)

    if (sell.size > 0) and (buy.size > 0) and (sell[0] < buy[0]):
        sell = sell[1:]

    return buy, sell

def peaks(
        data: Iterable[float], adjust: bool = False
) -> tuple[np.array, np.array]:
    """
    Processes the minimum and maximum peaks to match the trading process.

    :param data: The data to process.
    :param adjust: Thw value to adjust the peaks.

    :return: An array of the minimum values indexes and an array of the maximum values indexes.
    """

    data = array(data)

    maxima = maximums(data)
    minima = minimums(data)

    if adjust:
        return adjust_peaks(minima, maxima)

    return minima, maxima

def normalize(data: Iterable[float]) -> np.array:
    """
    Normalizes the values between 0 and 1.

    :param data: The data to normalize.

    :return: The normalized array of values.
    """

    if not isinstance(data, np.ndarray):
        data = np.array(data)

    return (data - np.min(data)) / np.ptp(data)

def array(data: Iterable[float], scale: bool = False) -> np.array:
    """
    Normalizes the values between 0 and 1.

    :param data: The data to normalize.
    :param scale: The valur to normalize the data.

    :return: The normalized array of values.
    """

    if not isinstance(data, np.ndarray):
        data = np.array(data)

    if scale and not ((np.max(data) == 1) and (np.min(data) == 0)):
        data = normalize(data)

    return data

def drop_nan(data: Iterable[float], value: float = 0.0) -> np.array:
    """
    Replaces the nan values in the data with a given value.

    :param data: The data to refactor.
    :param value: The value to replace nan values.

    :return: The refactored data.
    """

    return np.nan_to_num(array(data), nan=value)

def linear_distance_clusters(
        data: Iterable[float | np.ndarray],
        index: Iterable = None,
        source: float | np.ndarray = None
) -> tuple[list[list], list[list]]:
    """
    Clusters the data into clusters, with small distance between each element in the cluster.

    :param data: The data to cluster by linear distance.
    :param index: The index of the data.
    :param source: The relative source for the data.

    :return: The clusters of the data index.
    """

    data = array(data)

    if data.size == 0:
        raise ValueError(f"Empty data sequence given.")

    if index is None:
        index = range(data.size)

    dataset = list(zip(index, data))

    dataset.sort(
        key=lambda pair: (
            (np.linalg.norm(pair[1] - source)
             if (source is not None) else
             np.linalg.norm(pair[1]))
        )
    )

    indexes = [pair[0] for pair in dataset]
    data = [pair[1] for pair in dataset]

    data_clusters = [[data[0]]]
    index_clusters = [[indexes[0]]]

    if len(data) == 1:
        return index_clusters, data_clusters

    for i, value in enumerate(data[1:], start=1):
        if i in index_clusters[-1]:
            continue

        if (
            (len(data_clusters[-1]) >= 2) and
            (
                np.linalg.norm(value - data_clusters[-1][-1]) >
                np.linalg.norm(data_clusters[-1][-1] - data_clusters[-1][-2])
            )
        ):
            if (i + 1 < len(data)) and (
                np.linalg.norm(data[i + 1] - value) <
                np.linalg.norm(value - data_clusters[-1][-1])
            ):
                data_clusters.append([value, data[i + 1]])
                index_clusters.append([indexes[i], indexes[i + 1]])

            else:
                data_clusters.append([value])
                index_clusters.append([indexes[i]])

        else:
            data_clusters[-1].append(value)
            index_clusters[-1].append(indexes[i])

    return index_clusters, data_clusters

def normalize_calculation(calculation: Callable) -> Callable:
    """
    Creates a decorator to normalize the mathematical calculation.

    :param calculation: The calculation function.

    :return: The wrapper function to wrap the calculation.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Runs the given calculation with its parameters.

        :param args: The arguments for the calculation.
        :param kwargs: The keyword arguments for the calculation.

        :return: The returned results from the calculation.
        """

        try:
            return calculation(*args, **kwargs)

        except (ValueError, ZeroDivisionError):
            return 0

    return wrapper

def round_decimals_down(number: float, decimals: int = 0) -> float:
    """
    Returns a value rounded down to a specific number of decimal places.

    :param number: The number to round
    :param decimals: The amount of decimal places to leave in the number.

    :return: The rounded value.

    """

    if not isinstance(decimals, int):
        raise TypeError("Decimal places must be an integer.")

    elif decimals < 0:
        raise ValueError("Decimal places has to be 0 or more.")

    elif decimals == 0:
        return float(math.floor(number))

    string_number = str(float(number))

    return float(string_number[:string_number.find(".") + decimals + 1])

def average_growth_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        if change.size == 0:
            return 0

        s = np.sum(change)

        if np.isnan(s):
            return 0

        return np.sum(s) / change.size

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def average_shrink_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        change = np.where(change < 0, change, 0)
        change = np.array(
            [np.sum(change[:i + 1]) for i in range(change.size)]
        )
        change = change[1:] - pd.Series(change).shift(1)[1:]

        if change.size == 0:
            return 0

        s = np.sum(change)

        if np.isnan(s):
            return 0

        return abs(s / change.size)

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def down_movement(data: Iterable[float]) -> np.array:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        values = [0]

        for i, value in enumerate(data[1:], start=1):
            values.append(
                value - data[i - 1]
                if value < data[i - 1]
                else values[-1]
            )

        values = array(values)

        return np.array(
            [
                np.sum(np.unique(values[:i + 1]))
                for i in range(values.size)
            ]
        )

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def up_movement(data: Iterable[float]) -> np.array:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        return -down_movement(data) + data

    except (ValueError, ZeroDivisionError):
        return 0

def cumulative_shrink(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        return np.sum(np.array(np.where(change < 0, -change, 0))) / data[0]

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def cumulative_gain(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        return np.sum(np.array(np.where(change > 0, change, 0))) / data[0]

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def average_gain_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        change = np.where(change > 0, change, 0)
        change = np.array([np.sum(change[:i + 1]) for i in range(change.size)])
        change = change[1:] - pd.Series(change).shift(1)[1:]

        s = np.sum(change)

        if np.isnan(s):
            return 0

        if change.size == 0:
            return 0

        return abs(s / change.size)

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def average_deviation_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = np.abs(data[1:] - pd.Series(data).shift(1)[1:])

        s = np.sum(change)

        if np.isnan(s):
            return 0

        return s / change.size

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def min_change_factor(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        return np.min(data[1:] - pd.Series(data).shift(1)[1:])

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def max_change_factor(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        return np.max(data[1:] - pd.Series(data).shift(1)[1:])

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def average_change_factor(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        return np.sum(
            data[1:] - pd.Series(data).shift(1)[1:]
        ) / data[1:].size

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def average_win_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        values = np.where(change > 1, 1, 0)

        profit = np.count_nonzero(values)
        loss = values.size - profit

        if profit == 0:
            return 0.0

        if profit + loss == 0:
            return 1.0

        return profit / (profit + loss)

    except (ValueError, IndexError):
        return 0

def average_change_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        values = np.where(change == 0, 1, 0)

        constant = np.count_nonzero(values)
        changes = values.size - constant

        if changes == 0:
            return 0.0

        if constant + changes == 0:
            return 1.0

        return changes / (constant + changes)

    except (ValueError, IndexError):
        return 0

def weighted_average_win_rate(data: Iterable[float]) -> float:
    """
    Calculates the average change rate.

    :param data: The simulation data.

    :return: The calculated number.
    """

    data = array(data)

    validate_data_length(data)

    try:
        change = data[1:] - pd.Series(data).shift(1)[1:]

        profit = np.sum(np.where(change > 0, change, 0))
        loss = np.sum(np.where(change < 0, change, 0))

        if profit == 0:
            return 0.0

        if profit + loss == 0:
            return 1.0

        return profit / (profit + loss)

    except (ValueError, ZeroDivisionError, IndexError):
        return 0

def spread_deviation_risk_ratio(
        bids: Iterable[float],
        asks: Iterable[float],
        window: int = None,
        accurate: bool = True,
        weighted: bool = True
) -> float:
    """
    Calculates the risk of an asset reversing more than the difference.

    :param bids: The bid prices for the asset.
    :param asks: The ask prices for the asset.
    :param window: The window of data points to calculate the risk with.
    :param weighted: The value to calculate the weighted risk.
    :param accurate: The value to calculate the accurate risk.

    :return: The rist ratio according to standard deviation.
    """

    bids = array(bids)
    asks = array(asks)

    window = window or min([bids.size, asks.size])

    if window == 0:
        raise ValueError("No data was given.")

    if (window > bids.size) or (window > asks.size):
        raise ValueError(
            f"Bids length: {bids.size} and asks: {asks.size} "
            f"length don't match window the window: {window}."
        )

    bids = bids[-window:]
    asks = asks[-window:]

    difference = (bids - asks) / asks

    asks_std = np.std(asks)
    bids_std = np.std(bids)

    deviation = (bids_std - asks_std) / asks_std

    if np.isnan(deviation):
        deviation = 0

    if deviation <= 0:
        return deviation + 1

    risk = float(np.sum(difference) / difference.size + deviation) / 2

    if accurate or weighted:
        win = np.where(bids > asks, bids - asks, 0)
        lose = np.where(bids <= asks, asks - bids, 0)

    else:
        win = None
        lose = None

    accuracy = None

    if accurate:
        win_count = np.count_nonzero(win)
        lose_count = np.count_nonzero(lose)

        accuracy = win_count / (win_count + lose_count)

    if weighted:
        win_sum = float(np.sum(win))
        lose_sum = float(np.sum(lose))

        weighted_accuracy = win_sum / (win_sum + lose_sum)
        accuracy = accuracy or weighted_accuracy
        accuracy = (accuracy + weighted_accuracy) / 2

    if accuracy is not None:
        mistake = 1 - accuracy

    else:
        mistake = risk

    return (risk + mistake) / 2
