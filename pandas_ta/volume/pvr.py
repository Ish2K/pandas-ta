# -*- coding: utf-8 -*-
from numpy import nan
from pandas import Series
from pandas_ta.utils import get_drift, verify_series


def pvr(
    close: Series, volume: Series, drift: int = None,
) -> Series:
    """Price Volume Rank

    The Price Volume Rank was developed by Anthony J. Macek and is described in his
    article in the June, 1994 issue of Technical Analysis of Stocks & Commodities
    Magazine. It was developed as a simple indicator that could be calculated even
    without a computer. The basic interpretation is to buy when the PV Rank is below
    2.5 and sell when it is above 2.5.

    Sources:
        https://www.fmlabs.com/reference/default.htm?url=PVrank.htm

    Args:
        close (pd.Series): Series of 'close's
        volume (pd.Series): Series of 'volume's
        drift (int): The difference period. Default: 1

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    drift = get_drift(drift)
    close = verify_series(close, drift)
    volume = verify_series(volume, drift)

    # Calculate
    close_diff = close.diff(drift).fillna(0)
    volume_diff = volume.diff(drift).fillna(0)

    pvr = Series(nan, index=close.index)

    pvr.loc[(close_diff >= 0) & (volume_diff >= 0)] = 1
    pvr.loc[(close_diff >= 0) & (volume_diff < 0)] = 2
    pvr.loc[(close_diff < 0) & (volume_diff >= 0)] = 3
    pvr.loc[(close_diff < 0) & (volume_diff < 0)] = 4

    # Name and Category
    pvr.name = f"PVR"
    pvr.category = "volume"

    return pvr
