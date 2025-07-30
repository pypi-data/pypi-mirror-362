# dataset.py

import os
import datetime as dt
import json
from pathlib import Path
from typing import Iterable, Any, Callable

import numpy as np
import pandas as pd
from pandas.core.resample import Resampler

from market_break.interval import interval_total_time
from market_break.labels import (
    DATETIME, VOLUME, ORDERBOOK_COLUMNS, BID, OHLC_COLUMNS, BID_VOLUME
)

__all__ = [
    "row_to_dataset",
    "save_dataset",
    "load_dataset",
    "update_dataset",
    "split_dataset",
    "strip_dataset",
    "validate_dataset",
    "find_column",
    "validate_file_extension",
    "dataset_to_json",
    "dataset_from_json",
    "EXTENSIONS",
    "validate_file_path",
    "is_valid_location",
    "prepare_saving_location",
    "CSV_EXTENSION",
    "JSON_EXTENSION",
    "DEFAULT_EXTENSION",
    "bid_ask_to_ohlcv",
    "create_dataset",
    "adjust_series",
    "interval_adjuster",
    "index_to_datetime",
    "new_dataset_index"
]

def index_to_datetime(index: Any, adjust: bool = True) -> dt.datetime:
    """
    Converts the index into a datetime object.

    :param index: The value to convert.
    :param adjust: The value to adjust the process for errors.

    :return: The datetime object.
    """

    try:
        if isinstance(index, str):
            index = dt.datetime.fromisoformat(index)

        elif isinstance(index, (int, float)):
            index = dt.datetime.fromtimestamp(index)

        elif isinstance(index, pd.Timestamp):
            index = index.to_pydatetime()

        elif isinstance(index, np.datetime64):
            index = index.astype(dt.datetime)

    except (TypeError, ValueError) as e:
        if adjust:
            pass

        else:
            raise e

    return index

def row_to_dataset(
        dataset: pd.DataFrame | pd.Series,
        index: int = None
) -> pd.DataFrame:
    """
    Creates a dataframe from the row.

    :param dataset: The base dataset from witch the row came.
    :param index: The index of the row to create a dataset for.

    :return: The dataset from the row.
    """

    if isinstance(dataset, pd.DataFrame):
        if index is None:
            raise ValueError(
                f"Index must an int when dataset "
                f"is of type {pd.DataFrame}."
            )

        return pd.DataFrame(
            {
                column: [value] for column, value in
                dict(dataset.iloc[index]).items()
            },
            index=[dataset.index[index]]
        )

    elif isinstance(dataset, pd.Series):
        return pd.DataFrame(
            {
                column: [value] for column, value in
                dict(dataset).items()
            },
            index=[index or 0]
        )

    else:
        raise TypeError(
            f"Dataset must be either of type {pd.DataFrame}, "
            f"or {pd.Series}, not {type(dataset)}."
        )

def update_dataset(base: pd.DataFrame, new: pd.DataFrame) -> None:
    """
    Updates the ba se dataframe with new columns from the new dataframe.

    :param base: The base dataframe to update.
    :param new: The new dataframe with the new columns.
    """

    if not len(base) == len(new):
        raise ValueError(
            f"DataFrames lengths must match "
            f"(got {len(base)} and {len(new)} instead)."
        )

    for column in new.columns:
        if column not in base.columns:
            base[column] = new[column]

def split_dataset(
        dataset: pd.DataFrame | pd.Series,
        size: int | float = None,
        length: int = None
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the new_dataset into to parts at the point of the given size.

    :param dataset: The new_dataset to split.
    :param size: The size of the first part.
    :param length: The length of the split.

    :return: The two datasets.
    """

    if (size is None) and (length is None):
        raise ValueError(
            "Cannot split the dataset when neither "
            "size nor length parameters are defined."
        )

    length = length or int(len(dataset) * size)

    return dataset[:length], dataset[length:]

def strip_dataset(dataset: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """
    Strips the columns from the new_dataset.

    :param dataset: The new_dataset to remove features from.
    :param columns: The columns to validate.

    :return: The new new_dataset.
    """

    return dataset.drop(
        [
            column for column in columns
            if column in dataset.columns
        ], axis=1
    )

def validate_dataset(
        dataset: pd.DataFrame,
        columns: Iterable[str] = None,
        length: int = None
) -> None:
    """
    Validates the new_dataset to have the columns.

    :param dataset: The new_dataset to validate.
    :param columns: The columns to validate.
    :param length: The length of the valid dataset.
    """

    if (
        (columns is not None) and
        not all(column in dataset.columns for column in columns)
    ):
        missing = [
            column for column in columns
            if column not in list(dataset.columns)
        ]

        redundant = [
            column for column in list(dataset.columns)
            if column not in columns
        ]

        raise ValueError(
            f"DataFrame must include the "
            f"columns by the names: {columns}.\n"
            f"Given columns: {', '.join(dataset.columns)}.\n"
            f"Missing columns: {missing}.\n"
            f"Redundant columns: {redundant}."
        )

    if (length is not None) and len(dataset) != length:
        raise ValueError(
            f"Dataset must have length of {length}, "
            f"not: {len(dataset)}."
        )

def dataset_to_json(dataset: pd.DataFrame) -> list[str | dict[str, Any]]:
    """
    Converts the data of the dataset to json.

    :param dataset: The dataset to process.

    :return: The json representation of the data.
    """

    return list(json.loads(dataset.to_json(orient='index')).items())

def dataset_from_json(
        data: dict[str, dict[str, Any]] | list[str | dict[str, Any]]
) -> pd.DataFrame:
    """
    Converts the data from json format into a dataframe object.

    :param data: The json data to process.

    :return: The data frame object.
    """

    if isinstance(data, list):
        data = dict(data)

    return pd.read_json(json.dumps(data), orient="index")

CSV_EXTENSION = "csv"
JSON_EXTENSION = "json"
DEFAULT_EXTENSION = CSV_EXTENSION

EXTENSIONS = (CSV_EXTENSION, JSON_EXTENSION)

def validate_file_extension(path: str | Path, extension: str = None) -> str:
    """
    Validates the file formatting.

    :param path: The path to the file.
    :param extension: The data formatting.

    :return: The valid formatting.
    """

    path = str(path)

    if extension is None:
        if "." not in path:
            raise ValueError(
                f"Cannot infer file type and data "
                f"format from path: {path} and undefined formatting. "
                f"You may need to specify file extension in the path "
                f"or pass the 'formatting' parameter ({', '.join(EXTENSIONS)})."
            )

        extension = path[path.rfind(".") + 1:]

    if extension not in EXTENSIONS:
        raise ValueError(
            f"Invalid formatting value: {extension}. "
            f"value formatting options are: {', '.join(EXTENSIONS)}."
        )

    return extension

def is_valid_location(path: str | Path) -> bool:
    """
    Prepares the saving location.

    :param path: The path for the file to save.

    :return: The value of creating the location directory.
    """

    location = os.path.split(path)[0]

    return (
        ((not location) and path) or
        (location and os.path.exists(location))
    )

def validate_file_path(
        path: str | Path, create: bool = True, override: bool = True
) -> None:
    """
    Validates the file formatting.

    :param path: The path to the file.
    :param create: The value to create the path location.
    :param override: The value to override an existing file.

    :return: The valid formatting.
    """

    if create:
        prepare_saving_location(path=path)

    elif not is_valid_location(path=path):
        raise ValueError(
            f"Invalid file saving "
            f"location: {os.path.split(path)[0]} of {path}."
        )

    if os.path.exists(path) and not override:
        raise FileExistsError(
            f"Attempting to override an existing file: "
            f"{path} while 'override' is set to {override}."
        )

def prepare_saving_location(path: str | Path) -> bool:
    """
    Prepares the saving location.

    :param path: The path for the file to save.

    :return: The value of creating the location directory.
    """

    location = os.path.split(path)[0]

    if location:
        value = os.path.exists(location)

        os.makedirs(location, exist_ok=True)

        return value

    else:
        return False

def save_dataset(
        dataset: pd.DataFrame,
        path: str | Path,
        headers: bool = None,
        create: bool = True,
        override: bool = True,
        append: bool = False,
        extension: str = None
) -> None:
    """
    Saves the data.

    :param dataset: The dataset to save.
    :param create: The value to create the path location.
    :param headers: The value to include headers.
    :param override: The value to override an existing file.
    :param path: The saving path.
    :param append: The value to append data to the file.
    :param extension: The formatting of the data.
    """

    if extension is None:
        extension = DEFAULT_EXTENSION

    if headers is None:
        headers = not append

    path = str(path)

    extension = validate_file_extension(path=path, extension=extension)

    validate_file_path(path=path, create=create, override=override)

    if extension == CSV_EXTENSION:
        dataset.to_csv(path, mode='a' if append else "w", header=headers)

    elif extension == JSON_EXTENSION:
        with open(path, "w") as file:
            json.dump(dataset_to_json(dataset), file)

def load_dataset(
        path: str | Path,
        extension: str = None,
        index_column: int | bool = 0,
        time_index: bool = True
) -> pd.DataFrame:
    """
    Loads the dataset from the path.

    :param path: The saving path.
    :param extension: The formatting of the data.
    :param index_column: The value to set the index for the column.
    :param time_index: The value to se the index as datetime.

    :return: The loaded dataset.
    """

    if extension is None:
        extension = DEFAULT_EXTENSION

    path = str(path)

    extension = validate_file_extension(path=path, extension=extension)

    if extension == CSV_EXTENSION:
        dataset = pd.read_csv(path)

    elif extension == JSON_EXTENSION:
        with open(path, "r") as file:
            dataset = dataset_to_json(json.load(file))

    if index_column is True:
        index_column = 0

    if index_column is not None or index_column is False:
        index_column_name = list(dataset.columns)[index_column]
        dataset.index = (
            pd.DatetimeIndex(dataset[index_column_name])
            if time_index else dataset[index_column_name]
        )
        del dataset[index_column_name]
        dataset.index.name = DATETIME

    return dataset

def find_column(
        dataset: pd.DataFrame,
        columns: Iterable[Any],
        validation: Callable[[pd.Series], bool] = None
) -> pd.Series | None:
    """
    Finds the first valid column and returns it.

    :param dataset: The dataset to search.
    :param columns: The column names to search from, by order.
    :param validation: The validation function.

    :return: The valid column.
    """

    for column in columns:
        if column not in dataset:
            continue

        if (
            (validation is None) or
            (callable(validation) and validation(dataset[column]))
        ):
            return dataset[column]

def interval_adjuster(interval: str) -> str:
    """
    Creates the adjuster for the interval.

    :param interval: The interval to adjust data with.

    :return: The adjusted interval.
    """

    return f'{interval_total_time(interval).total_seconds()}S'

def adjust_series(data: pd.Series, interval: str) -> Resampler:
    """
    Converts the dataset into a dataset with an interval.

    :param data: The source data.
    :param interval: The interval for the new dataset.

    :return: The returned dataset.
    """

    return data.resample(interval_adjuster(interval))

def bid_ask_to_ohlcv(dataset: pd.DataFrame, interval: str) -> pd.DataFrame:
    """
    Converts the BID/ASK spread dataset into a OHLCV dataset.

    :param dataset: The source data.
    :param interval: The interval for the new dataset.

    :return: The returned dataset.
    """

    if not all(column in ORDERBOOK_COLUMNS for column in dataset.columns):
        raise ValueError(
            f"Dataset has to contain all columns: "
            f"{', '.join(ORDERBOOK_COLUMNS)}, "
            f"but found only: {', '.join(dataset.columns)}"
        )

    adjuster = interval_adjuster(interval)

    ohlcv_dataset = dataset[BID].resample(adjuster).ohlc()
    ohlcv_dataset.columns = list(OHLC_COLUMNS)
    ohlcv_dataset[VOLUME] = dataset[BID_VOLUME].resample(adjuster).mean()

    return ohlcv_dataset

def create_dataset(columns: Iterable[str] = None) -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :param columns: The dataset columns.

    :return: The dataframe.
    """

    market = pd.DataFrame(
        {column: [] for column in columns or []}, index=[]
    )
    market.index.name = DATETIME

    return market

def new_dataset_index(index: dt.datetime, dataset: pd.DataFrame) -> bool:
    """
    Checks if the index is new and valid to the dataset.

    :param index: The index to check.
    :param dataset: The dataset to validate the index for.

    :return: The validation of the index as new.
    """

    return (
        (len(dataset.index) == 0) or
        (
            isinstance(dataset.index[-1], dt.datetime) and
            (dataset.index[-1] < index)
        ) or
        (index not in dataset.index)
    )
