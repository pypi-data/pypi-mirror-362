"""Extensions to pandas."""
from math import inf

import pandas as pd
from pandas.core.generic import NDFrame

from ._collect import convert_nested_dict_to_nested_list


def _extend_index(old_index, new_index, mode="extend"):
    from ._set import union

    if mode == "extend":
        return union(list(old_index), list(new_index))
    if mode == "prioritize":
        return union(list(new_index), list(old_index))
    raise ValueError("mode must be 'extend' or 'prioritize'")


def _extend(frame, labels=None, index=None, columns=None, axis=None, mode="extend", **kwargs):
    if labels is not None:
        if axis in [0, "index"]:
            index = labels
        elif axis in [1, "columns"]:
            columns = labels
        else:
            raise ValueError("axis must be 0 or 1")
    if index is not None:
        kwargs["index"] = _extend_index(frame.index, index, mode=mode)
    if columns is not None:
        kwargs["columns"] = _extend_index(frame.columns, columns, mode=mode)
    result = frame.reindex(**kwargs)
    return result


def extend(frame, /, labels=None, *, index=None, columns=None, axis=None, **kwargs):
    """Add index values if the index values are not present.

    This API is simliar to ``pd.DataFrame.reindex()``.

    Parameters:
        frame (pd.Series | pd.DataFrame): Input data.
        labels (list | tuple, optional): New labels / index to conform the axis specified by.
        index (list | tuple, optional): index names.
        columns (list | tuple, optional): column names.
            only work for DataFrame.
        axis (int | str, optional): axis to extend.
            0: index, 1: columns.
            only work for DataFrame.
        kwargs: keyword arguments to be passed to ``pd.DataFrame.reindex()``,
            including ``copy``, ``level``, ``fill_value``, ``limit``, and ``tolerance``.

    Returns:
        pd.Series | pd.DataFrame:

    Example:
        >>> import pandas as pd
        >>> s = pd.Series(1, index=[0, 1])
        >>> extend(s, index=[1, 2])
        0    1.0
        1    1.0
        2    NaN
        dtype: float64
        >>> df = pd.DataFrame({"A": 1, "B": 2}, index=[0, 1])
        >>> extend(df, index=[1, 2], columns=["A", "C"])
              A    B    C
        0   1.0  2.0  NaN
        1   1.0  2.0  NaN
        2   NaN  NaN  NaN
    """
    result = _extend(frame, labels=labels, index=index, columns=columns, axis=axis, mode="extend", **kwargs)
    return result


def prioritize(frame, /, labels=None, *, index=None, columns=None, axis=None, **kwargs):
    """Put some index values at the begining of the index.

    If the index is already in the index, the index will be moved to the begining.
    If the index is not in the index, the index will be added to the index.

    This API is simliar to ``pd.Series.reindex()`` and ``pd.DataFrame.reindex()``.

    Parameters:
        frame (pd.Series | pd.DataFrame): Input data.
        labels (list | tuple, optional): New labels / index to conform the axis specified by
        index (list | tuple, optional): index names
        columns (list | tuple, optional): column names.
            only work for DataFrame.
        axis (int | str, optional): axis to extend.
            0: index, 1: columns.
            only work for DataFrame.
        kwargs: keyword arguments to be passed to ``pd.DataFrame.reindex()``,
            including ``copy``, ``level``, ``fill_value``, ``limit``, and ``tolerance``.

    Returns:
        pd.Series | pd.DataFrame:

    Example:
        >>> import pandas as pd
        >>> s = pd.Series(1, index=[0, 1])
        >>> prioritize(s, index=[1, 2])
        1    1.0
        2    NaN
        0    1.0
        dtype: float64
        >>> df = pd.DataFrame({"A": 1, "B": 2}, index=[0, 1])
        >>> prioritize(df, index=[1, 2], columns=["A", "C"])
             A   C    B
        1  1.0 NaN  2.0
        2  NaN NaN  NaN
        0  1.0 NaN  2.0
    """
    result = _extend(frame, labels=labels, index=index, columns=columns, axis=axis, mode="prioritize", **kwargs)
    return result


def stack(frame, /, **kwargs):
    """Stack a ``pd.Series`` or ``pd.DataFrame`` with ``future_stack`` behavior.

    Stack and silence the ``FutureWarning`` "The prevoius implementation of stack is deprecated".

    Parameters:
        frame (pd.DataFrame):
        **kwargs: Keyword arguments to be passed to ``pd.DataFrame.stack()``.

    Returns:
        pd.Series | pd.DataFrame:

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"A": 1, "B": 2}, index=[0])
        >>> stack(df)
        0 A  1
          B  2
        dtype: int64
    """
    dropna = kwargs.pop("dropna", False)
    try:
        result = frame.stack(future_stack=True, **kwargs)
    except Exception:
        result = frame.stack(dropna=False, **kwargs)
    if dropna:
        result = result.dropna()
    return result


def convert_nested_dict_to_dataframe(data, /, *, index_cols=None, columns=None):
    """Convert a nested dictionary to a ``pd.DataFrame``.

    Parameters:
        data (dict): Nested dict.
        index_cols (int | str | (list | tuple)[str], optional): Index names.
        columns (int | (list | tuple)[str]], optional): Column names.

    Returns:
        pd.DataFrame:

    Example:
        >>> data = {"A": {"H": 1, "J": 2}, "E": {"D": 3, "T": 4}}
        >>> convert_nested_dict_to_dataframe(data)
           0  1  2
        0  A  H  1
        1  A  J  2
        2  E  D  3
        3  E  T  4
        >>> convert_nested_dict_to_dataframe(data, index_cols=["v", "c"], columns=["x"])
             x
        v c
        A H  1
          J  2
        E D  3
          T  4
    """
    if index_cols is None:
        index_count = 0
        index_cols = []
    elif isinstance(index_cols, int):
        index_count = index_cols
        index_cols = list(range(index_cols))
    elif isinstance(index_cols, (list, tuple)):
        index_count = len(index_cols)
    else:
        raise ValueError()

    if columns is None:
        if index_count == 0:
            column_count = inf
        else:
            column_count = 1
    elif isinstance(columns, int):
        column_count = columns
    elif isinstance(columns, (list, tuple)):
        column_count = len(columns)
    else:
        raise ValueError()
    maxdepth = index_count + column_count - 1
    lst = convert_nested_dict_to_nested_list(data, maxdepth=maxdepth)
    df = pd.DataFrame(lst)
    if index_count > 0:
        df = df.set_index(list(range(index_count)))
        df.index.names = index_cols
    if isinstance(columns, (list, tuple)):
        df.columns = columns
    else:
        df.columns = list(range(df.shape[1]))
    return df


def convert_series_to_nested_dict(series, /):
    """Convert a ``pd.Series`` to a nested dictionary.

    Parameters:
        series (pd.Series):

    Returns:
        dict:

    Example:
        >>> import pandas as pd
        >>> s = pd.DataFrame({"A": 1, "B": [2, 3], "C": [4, 5]}).set_index(["A", "B"])["C"]
        >>> convert_series_to_nested_dict(s)
        {1: {2: 4, 3: 5}}
    """
    if not isinstance(series, NDFrame):  # recursive end, in this case the input is not series
        return series
    keys = sorted(set(series.index.get_level_values(0)))
    results = {}
    for key in keys:
        arg0 = series.loc[key]
        results[key] = convert_series_to_nested_dict(arg0)
    return results
