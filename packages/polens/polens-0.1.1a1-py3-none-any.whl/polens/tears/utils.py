# -*- coding: utf-8 -*-
"""
---------------------------------------------
Copyright (c) 2025 ZhangYundi
Licensed under the MIT License. 
Created on 2025/7/13 14:02
Email: yundi.xxii@outlook.com
Description: 
---------------------------------------------
"""
from typing import Sequence

import polars as pl
from pandas import Timedelta

def get_timedelta_names(columns: Sequence[str], ) -> list[str]:
    """
    Return a list of column names that can be successfully parsed into <pandas>.Timedelta object.

    Parameters
    ----------
    columns: Sequence[str]
        A Sequence of strings representing column names to be evaluated for Timedelta

    Returns
    -------
    list[str]

    Examples
    --------
    >>> get_timedelta_names(['1s', '2min', 'invalid', '3H'])
    ['1s', '2min', '3H']

    """
    from pandas import Timedelta
    def _is_valid_timedelta(s: str) -> bool:
        try:
            Timedelta(s)
            return True
        except ValueError:
            return False

    return [col for col in columns if _is_valid_timedelta(col)]


def extract_feature_names(columns: Sequence[str], ) -> list[str]:
    """
    Extract a list of valid feature column names by excluding index-like(date/time/asset)、price-like(price)、time-like columns.
    Parameters
    ----------
    columns: Sequence[str]
        A sequence of strings representing all available column names.

    Returns
    -------
    list[str]

    Examples
    --------
    >>> extract_feature_names(['date', 'time', 'asset', 'open', 'high', '1s', 'volume', 'price'])
    ['open', 'high', 'volume']

    """
    return_cols = get_timedelta_names(columns)
    exclude = {"date", "time", "asset", 'price', *return_cols}
    return [col for col in columns if col not in exclude]


def demean_forward_returns(factor_data: pl.DataFrame, grouper=None):
    if grouper is None:
        grouper = list({"date", "time"}.intersection(factor_data.columns))
    # 提取需要计算的列
    cols = get_timedelta_names(factor_data.columns)

    # 按 grouper 分组，对 cols 列进行中心化 (x - x.mean())
    result = factor_data.with_columns([
        (pl.col(col) - pl.col(col).mean().over(grouper)).alias(col)
        for col in cols
    ])

    return result


def freq_adjust(period, trading_hours=4, target_period="252d"):
    """调整周期: 按照1天交易时间4h"""
    scaler = (Timedelta(target_period).days * trading_hours * 60 * 60 + Timedelta(target_period).seconds) / (
                Timedelta(period).days * trading_hours * 60 * 60 + Timedelta(period).seconds)
    return scaler


def add_factor_quantile(factor_data: pl.DataFrame,
                        factor_field: str = "factor",
                        bins: int = 10,
                        by_group: bool = False) -> pl.DataFrame:
    """添加分组列"""
    grouper = list({"date", "time"}.intersection(factor_data.columns))
    if by_group:
        grouper.append("group")
    return (
        factor_data
        .with_columns(pl.col(factor_field)
                      .qcut(bins, labels=[str(i) for i in range(1, bins + 1)], allow_duplicates=True)
                      .over(grouper)
                      .alias(f"{factor_field}_quantile")
                      )
        .cast({pl.Categorical: pl.Int32})
    )
