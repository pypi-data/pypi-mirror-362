from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
import pyarrow as pa
from kumoapi.typing import Dtype, Stype
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_list_like,
    is_object_dtype,
)

from kumoai.experimental.rfm.infer import (
    contains_categorical,
    contains_id,
    contains_multicategorical,
    contains_timestamp,
)

# Maximum number of rows to check for dtype inference in object columns
_MAX_NUM_ROWS_FOR_DTYPE_INFERENCE = 100

# Mapping from pandas/numpy dtypes to Kumo Dtypes
PANDAS_TO_DTYPE: Dict[Any, Dtype] = {
    np.dtype('bool'): Dtype.bool,
    pd.BooleanDtype(): Dtype.bool,
    pa.bool_(): Dtype.bool,
    np.dtype('byte'): Dtype.int,
    pd.UInt8Dtype(): Dtype.int,
    np.dtype('int16'): Dtype.int,
    pd.Int16Dtype(): Dtype.int,
    np.dtype('int32'): Dtype.int,
    pd.Int32Dtype(): Dtype.int,
    np.dtype('int64'): Dtype.int,
    pd.Int64Dtype(): Dtype.int,
    np.dtype('float32'): Dtype.float,
    pd.Float32Dtype(): Dtype.float,
    np.dtype('float64'): Dtype.float,
    pd.Float64Dtype(): Dtype.float,
    np.dtype('object'): Dtype.string,
    pd.StringDtype(storage='python'): Dtype.string,
    pd.StringDtype(storage='pyarrow'): Dtype.string,
    pa.string(): Dtype.string,
    pa.binary(): Dtype.binary,
    np.dtype('datetime64[ns]'): Dtype.date,
    np.dtype('timedelta64[ns]'): Dtype.timedelta,
    pa.list_(pa.float32()): Dtype.floatlist,
    pa.list_(pa.int64()): Dtype.intlist,
    pa.list_(pa.string()): Dtype.stringlist,
}


def to_dtype(dtype: Any, ser: Optional[pd.Series] = None) -> Dtype:
    """Convert a pandas/numpy/pyarrow dtype to Kumo Dtype.

    Args:
        dtype: The dtype to convert
        ser: Optional pandas Series for additional type inference

    Returns:
        The corresponding Kumo Dtype
    """
    if is_datetime64_any_dtype(dtype):
        return Dtype.date
    if isinstance(dtype, pd.CategoricalDtype):
        return Dtype.string
    if is_object_dtype(dtype) and ser is not None and len(ser) > 0:
        if is_list_like(ser.iloc[0]):
            # the 0-th element might be an empty list or a list of N/A so
            # iterate over the first _MAX_NUM_ROWS_FOR_DTYPE_INFERENCE elements
            # to infer the dtype:
            for i in range(min(len(ser), _MAX_NUM_ROWS_FOR_DTYPE_INFERENCE)):
                # pd.isna can't be called on a list
                if (not isinstance(ser.iloc[i], list)
                        and not isinstance(ser.iloc[i], np.ndarray)
                        and pd.isna(ser.iloc[i])) or len(ser.iloc[i]) == 0:
                    continue
                elif isinstance(ser.iloc[i][0], float):
                    return Dtype.floatlist
                elif np.issubdtype(type(ser.iloc[i][0]), int):
                    return Dtype.intlist
                elif isinstance(ser.iloc[i][0], str):
                    return Dtype.stringlist
    return PANDAS_TO_DTYPE[dtype]


def infer_stype(ser: pd.Series, column_name: str, dtype: Dtype) -> Stype:
    r"""Infers the semantic type of a column.

    Args:
        ser: A :class:`pandas.Series` to analyze.
        column_name: The name of the column (used for pattern matching).
        dtype: The data type.

    Returns:
        The semantic type.
    """
    if contains_id(ser, column_name, dtype):
        return Stype.ID

    if contains_timestamp(ser, column_name, dtype):
        return Stype.timestamp

    if contains_multicategorical(ser, column_name, dtype):
        return Stype.multicategorical

    if contains_categorical(ser, column_name, dtype):
        return Stype.categorical

    return dtype.default_stype


def detect_primary_key(
    table_name: str,
    df: pd.DataFrame,
    candidates: list[str],
) -> Optional[str]:
    r"""Auto-detect potential primary key column.

    Args:
        table_name: The table name.
        df: The pandas DataFrame to analyze
        candidates: A list of potential candidates.

    Returns:
        The name of the detected primary key, or ``None`` if not found.
    """
    table_name = table_name.lower()

    scores: list[tuple[str, int]] = []
    for col_name in candidates:
        col_name_lower = col_name.lower()

        score = 0
        if col_name_lower == 'id':
            score += 5
        elif col_name_lower == f'{table_name}_id':
            score += 5  # USER -> USER_ID
        elif col_name_lower == f'{table_name}id':
            score += 5  # User -> UserId
        elif (table_name.endswith('s')
              and col_name_lower == f'{table_name[:-1]}_id'):
            score += 5  # USERS -> USER_ID
        elif (table_name.endswith('s')
              and col_name_lower == f'{table_name[:-1]}id'):
            score += 5  # Users -> UserId
        elif col_name_lower == table_name:
            score += 4  # USER -> USER
        elif table_name.endswith('s') and col_name_lower == table_name[:-1]:
            score += 4  # USERS -> USER
        elif col_name_lower.endswith('_id'):
            score += 2

        if df[col_name].nunique() / len(df) >= 0.95:
            score += 4

        scores.append((col_name, score))

    scores = [x for x in scores if x[-1] >= 4]
    scores.sort(key=lambda x: x[-1], reverse=True)

    if len(scores) == 1:
        return scores[0][0]

    # In case of multiple candidates, only return one if its score is unique:
    if len(scores) > 1 and scores[0][1] != scores[1][1]:
        return scores[0][0]

    return None


def detect_time_column(
    df: pd.DataFrame,
    candidates: list[str],
) -> Optional[str]:
    r"""Auto-detect potential time column.

    Args:
        df: The pandas DataFrame to analyze
        candidates: A list of potential candidates.

    Returns:
        The name of the detected time column, or ``None`` if not found.
    """
    if len(candidates) == 0:
        return None

    if len(candidates) == 1:
        return candidates[0]

    # Find the most optimal time column. Usually, it is the one pointing to
    # the oldest timestamps:
    min_timestamp_dict = {
        key: pd.to_datetime(df[key], 'coerce').min().tz_localize(None)
        for key in candidates
    }
    min_timestamp_dict = {
        key: min_timestamp
        for key, min_timestamp in min_timestamp_dict.items()
        if not pd.isna(min_timestamp)
    }

    if len(min_timestamp_dict) == 0:
        return None

    return min(min_timestamp_dict, key=min_timestamp_dict.get)  # type: ignore
