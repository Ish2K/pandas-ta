# -*- coding: utf-8 -*-
from numpy import nan, roll
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def percent_return(
    close: Series, length: int = None, cumulative: bool = None,
    offset: int = None, **kwargs
) -> Series:
    """Percent Return

    Calculates the percent return of a Series.
    See also: help(df.ta.percent_return) for additional **kwargs a valid 'df'.

    Sources:
        https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 20
        cumulative (bool): If True, returns the cumulative returns. Default: False
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 1
    cumulative = bool(
        cumulative) if cumulative is not None and cumulative else False
    close = verify_series(close, length)
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    np_close = close.values
    if cumulative:
        pr = (np_close / np_close[0]) - 1
    else:
        pr = (np_close / roll(np_close, length)) - 1
        pr[:length] = nan
    pct_return = Series(pr, index=close.index)

    # Offset
    if offset != 0:
        pct_return = pct_return.shift(offset)

    # Fill
    if "fillna" in kwargs:
        pct_return.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pct_return.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    pct_return.name = f"{'CUM' if cumulative else ''}PCTRET_{length}"
    pct_return.category = "performance"

    return pct_return
