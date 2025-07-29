# -*- coding: utf-8 -*-
"""
---------------------------------------------
Copyright (c) 2025 ZhangYundi
Licensed under the MIT License. 
Created on 2025/7/13 14:21
Email: yundi.xxii@outlook.com
Description: 性能指标
---------------------------------------------
"""
import time
from itertools import chain

import polars as pl
import numpy as np
from polars._utils.unstable import unstable

from . import utils


def factor_information_coefficient(factor_data: pl.DataFrame,
                                   factor_field: str = "factor",
                                   grouper: list[str] = ["date", ],
                                   group_adjust=False,
                                   method="spearman"):
    """
    计算因子值与 N 个周期的 forward returns 的 Spearman Rank 信息系数 (IC)。

    Parameters
    ----------
    factor_data : pl.DataFrame
        一个 Polars DataFrame，包含以下列：
        - 日期 (date)、时间 (time)、资产 (asset)、因子值 (factor)
        - N 个周期的 forward returns 列（如 1d, 5d, 5min, 30min 等）
        - 可选列：因子所属的分组 (group)、因子 quantile/bin 列等。

        如果需要清洗数据，请参考 utils.get_clean_factor_and_forward_returns。
    factor_field: str
        因子列名
    grouper: list[str]
        用于分组的字段名，默认 date。比如需要计算每个行业的 IC, 则 grouper = ["group", ]
    group_adjust : bool
        是否在计算 IC 前，对分组内的 forward returns 去均值化。默认值为 False
    method: str
    Returns
    -------
    ic : pl.DataFrame
        每个分组的 Spearman Rank 相关系数 (IC)，以及 `index` 中的分组键。
        返回的列：
        - `index`：用于分组的列（如 date, time, group 等）
        - forward returns 的 IC 值，每列对应一个周期的 forward returns。
    """
    return_cols = utils.get_timedelta_names(factor_data.columns)
    if group_adjust:
        factor_data = utils.demean_forward_returns(factor_data, grouper + ["time", "group"])

    factor_data = factor_data.drop_nulls(subset=grouper)
    # 在每个分组内计算因子和 forward returns 的相关性
    result = factor_data.group_by(grouper).agg([
        pl.corr(factor_field, col, method=method).alias(col) for col in return_cols
    ])
    return result.sort(by=grouper).fill_nan(None)


def mean_information_coefficient(factor_data: pl.DataFrame,
                                 factor_field: str = "factor",
                                 grouper: list[str] = ["date", ],
                                 group_adjust=False,
                                 every: str = None) -> pl.DataFrame:
    """
    计算指定条件下的平均信息系数（IC，Information Coefficient）。

    信息系数（IC）用于衡量因子值与未来收益之间的相关性，通常以 **Spearman 等级相关系数** 表示。
    本函数支持按时间窗口、资产分组或两者结合来分别计算平均 IC。

    功能示例：
    - 计算每个月的平均 IC。
    - 计算整个时间范围内，每个分组的平均 IC。
    - 计算每周、每个分组的平均 IC。

    Parameters
    ----------
    factor_data : pl.DataFrame
        一个 Polars DataFrame，包含以下列：
        - 日期列 (`date`)：用于时间索引；
        - 因子值列：包含单因子的值；
        - 前瞻收益列（forward returns columns）：用于计算因子与未来收益的相关性；
        - （可选）分组列（`group`）：按资产类别或自定义分组标识资产所属类别。
        数据格式需参考 `utils.get_clean_factor_and_forward_returns` 处理后的输出。

    factor_field: str
        因子列名
    grouper: list[str]
        用于分组的字段名，默认 date。比如需要计算每个行业的 IC, 则 grouper = ["group", ]
    group_adjust : bool
        是否在计算 IC 前，对分组内的 forward returns 去均值化。默认值为 False

    every : str, 可选，默认值为 None
        按指定时间频率动态分组，例如 "1d"（按日）、"1w"（按周）、"1mo"（按月）、"1q"（按季度）、"1y" (按年)。
        若指定此参数，则使用 Polars 的 `group_by_dynamic` 按时间窗口分组。

    Returns
    -------
    pl.DataFrame
        一个 Polars DataFrame，包含平均 IC 值，具体结构取决于参数组合：
        - 如果仅指定 `by_group=True`：返回按分组计算的平均 IC；
        - 如果仅指定 `by_time=True`：返回按时间窗口计算的平均 IC；
        - 如果同时指定 `by_group=True` 和 `by_time=True`：返回按分组和时间窗口的平均 IC；
        - 如果未指定分组参数：返回整个数据集的平均 IC。

    Notes
    -----
    - 信息系数（IC）的计算基于因子值与前瞻收益的 **Spearman 等级相关系数**。
    - 可以通过参数组合自定义分组方式，例如按时间窗口和分组同时分组。

    Examples
    --------
    按时间窗口分组计算 IC：

    >>> mean_information_coefficient(factor_data=df, every="1m")

    按分组计算 IC：

    >>> mean_information_coefficient(factor_data=df, grouper=["group", ])

    按时间窗口和分组同时计算 IC：

    >>> mean_information_coefficient(factor_data=df, every="1w", grouper=["time", "group"])

    计算全局平均 IC：

    >>> mean_information_coefficient(factor_data=df)
    """

    ic = factor_information_coefficient(factor_data,
                                        factor_field=factor_field,
                                        grouper=grouper,
                                        group_adjust=group_adjust, ).fill_nan(None)
    cols = utils.get_timedelta_names(factor_data.columns)

    ic = ic.drop_nulls(subset=grouper)
    if every is not None:
        # 使用 groupby_dynamic 按时间频率分组
        ic = ic.group_by_dynamic("date", every=every).agg(
            pl.col(*cols, *grouper)).explode(*cols, *grouper)
    if len(grouper) == 0:
        return ic.select(pl.col(*cols)).mean()
    ic_result = ic.group_by(grouper).agg(
        pl.col(*cols).mean()
    )

    return ic_result


def factor_weights(factor_data: pl.DataFrame,
                   factor_field: str = "factor",
                   grouper: list[str] = ["date", "time"],
                   demeaned=True,
                   group_adjust=True,
                   equal_weight=False) -> pl.DataFrame:
    """
    使用 Polars 实现资产权重计算，基于因子值按分组进行归一化处理。

    Parameters
    ----------
    factor_data : pl.DataFrame
        一个 Polars DataFrame，包含以下列：
        - `date`：日期；
        - `time`：时间；
        - `asset`：资产标识；
        - `factor`：因子值；
        - `group`：资产所属分组（可选）。
    factor_field: str
        因子列
    grouper: list[str]
    demeaned : bool, 默认值为 True
        是否对因子值进行去均值处理以构建多空组合。
    group_adjust : bool, 默认值为 False
        是否按分组进行中性化处理，使每组权重的绝对值总和相等。
    equal_weight : bool, 默认值为 True
        是否对资产进行等权分配。

    Returns
    -------
    pl.DataFrame
        包含计算出的资产权重的 DataFrame，列包括：
        - `date`：日期；
        - `time`：时间；
        - `asset`：资产标识；
        - `weight`：计算出的权重。
    """

    index = list({"date", "time"}.intersection(factor_data.columns))
    if group_adjust:
        grouper.append("group")
    factor_data = factor_data.fill_nan(None).drop_nulls(subset=grouper)
    if demeaned:
        factor_data = factor_data.with_columns(pl.col(factor_field) - pl.col(factor_field).median().over(grouper))
    if equal_weight:
        negative_mask = pl.col("factor") < 0
        positive_mask = pl.col("factor") > 0
        factor_data = factor_data.with_columns(
            pl.when(negative_mask).then(-1.0).when(positive_mask).then(1.0).otherwise(0.0).alias(factor_field))
    factor_data = factor_data.select(*index, "asset",
                                     pl.col(factor_field) / pl.col(factor_field).abs().sum().over(grouper)).fill_nan(
        None)
    if group_adjust:
        # 归一化
        factor_data = factor_data.select(*index, "asset",
                                         pl.col(factor_field) / pl.col(factor_field).abs().sum().over(index))
    return factor_data.sort(by=[*index, "asset"])


def factor_returns(factor_data: pl.DataFrame,
                   factor_field: str = "factor",
                   grouper: list[str] = ["date", "time"],
                   demeaned=True,
                   group_adjust=True,
                   equal_weight=False,
                   by_asset=False) -> pl.DataFrame:
    """
    计算按因子值加权的投资组合在每个周期的收益。

    Parameters
    ----------
    factor_data : pl.DataFrame
        一个 Polars DataFrame，包含以下列：
        - `date`：日期；
        - `time`：时间（可选，若存在则使用）；
        - `asset`：资产标识；
        - `factor`：因子值；
        - 若存在未来收益列（例如 `1D`, `5D` 等），则用于计算收益；
        - 可选的 `group` 列用于分组。
        因子数据被预处理以确保数据完整和符合要求。
    factor_field: str
    grouper: list[str]
    demeaned : bool, 默认值为 True
        是否去均值以构建多空组合。
        - 如果为 True，权重将按去均值后的因子值计算。
    group_adjust : bool, 默认值为 False
        是否按分组进行中性化处理。
        - 如果为 True，每组权重的绝对值总和将相等。
    equal_weight : bool, 默认值为 False
        是否对资产进行等权分配。
        - 如果为 True，所有资产的权重将相等。
    by_asset : bool, 默认值为 False
        是否按资产单独返回收益。
        - 如果为 True，将按资产分别报告收益；
        - 如果为 False，将返回整体组合的收益。

    Returns
    -------
    returns : pl.DataFrame
        每个周期的因子收益。
        - 如果 `by_asset=True`，返回按资产分组的收益；
        - 如果 `by_asset=False`，返回整体因子组合的周期收益。
        返回的 DataFrame 列包括：
        - 时间索引列（如 `date` 和 `time`）；
        - 每个周期的收益列（例如 `1D`, `5D` 等）。
    """

    # index = pd.Index(["date", "time", "asset"]).intersection(factor_data.columns).tolist()
    index = list({"date", "time", "asset"}.intersection(factor_data.columns))

    weights = factor_weights(factor_data=factor_data, factor_field=factor_data, grouper=grouper, demeaned=demeaned,
                             group_adjust=group_adjust, equal_weight=equal_weight)

    factor_data = factor_data.join(weights.rename({factor_field: "w"}), on=index, how="left")
    cols = utils.get_timedelta_names(factor_data.columns)
    weighted_returns = factor_data.select(*index, pl.col(cols) * pl.col("w"))

    if by_asset:
        returns = weighted_returns
    else:
        index = list({"date", "time"}.intersection(factor_data.columns))
        returns = weighted_returns.fill_nan(None).group_by(index).agg(pl.col(cols).sum())

    return returns.sort(by=index)


def quantile_returns(factor_data: pl.DataFrame,
                     factor_field: str = "factor",
                     demeaned_grouper: list[str] = ["date", "time"],
                     stats_grouper: list[str] = ["date",],
                     by_date=False, ) -> (pl.DataFrame, pl.DataFrame, pl.DataFrame):
    """
    计算因子分位数（quantile）对应的平均收益和 t 统计量。

    此函数基于给定的因子数据，按照因子分位数（quantile）计算前瞻收益的平均值和标准误差，
    并进一步计算 t 统计量。

    Parameters
    ----------
    factor_data : pl.DataFrame
        包含因子值、分位数、前瞻收益数据的 DataFrame。通常由 `utils.get_clean_factor_and_forward_returns` 函数生成。
        需要包含以下列：
            - `date`：日期；
            - `time`：时间；
            - `asset`：资产标识；
            - `factor`：因子值；
            - `factor_quantile`：因子值对应的分位数或区间。
            - 前向收益列：每个周期的收益，例如 `1D`、`5D` 等。
            - （可选）`group`：资产所属的行业。
    factor_field: str
        因子列名
    demeaned_grouper: list[str]
        用于demeand的分组,比如高频alpha我们需要将每一个截面的return都剔除市场均值的影响 则该grouper可以设置为["date", "time"]
    stats_grouper: list[str]
        用于计算统计量的grouper,统计量分两步计算：首先是每日的统计量，接着是计算全局统计量
    by_date : bool, 默认为 False
        如果为 True，则按日期分别计算每个分位数的收益。

    Returns
    -------
    (polars.DataFrame, polars.DataFrame, polars.DataFrame)

    mean_ret : pl.DataFrame
        每个分位数的平均收益，按指定的分组维度（如日期、时间、分组）计算。
        列出每个前瞻收益周期的分位数平均收益。
    std_err_ret: pl.DataFrame
        每个分位数收益的标准误差，表示精确度。
        列出每个前瞻收益周期的分位数平均收益。
    t_stat_ret : pl.DataFrame
        每个分位数的 t 统计量，表示收益显著性。
        列出每个前瞻收益周期的分位数 t 统计量。

    Examples
    --------
    >>> mean_ret, std_err_ret, t_stat_ret = mean_return_by_quantile(
    ...     factor_data=factor_data,
    ...     by_date=True,
    ...     by_time=True,
    ...     by_group=True,
    ...     demeaned=True
    ... )
    >>> print(mean_ret)
    >>> print(t_stat_ret)
    """

    if demeaned_grouper:
        factor_data = utils.demean_forward_returns(factor_data, grouper=demeaned_grouper)
    if f"{factor_field}_quantile" not in stats_grouper:
        stats_grouper = [f"{factor_field}_quantile", *stats_grouper]
    cols = utils.get_timedelta_names(factor_data.columns)
    group_stats = factor_data.group_by(stats_grouper).agg(
        *chain.from_iterable(
            [
                [
                    pl.col(col).mean().alias(f"mean_{col}"),
                    pl.col(col).std().alias(f"std_{col}"),
                    pl.col(col).count().alias(f"n_{col}"),
                ]
                for col in cols
            ]
        )
    )
    mean_ret = group_stats.select(
        *stats_grouper,
        *[pl.col(f"mean_{col}").alias(col) for col in cols]
    )
    if not by_date:
        stats_grouper = [field for field in stats_grouper if field != "date"]
        group_stats = mean_ret.group_by(stats_grouper).agg(
            *chain.from_iterable(
                [
                    [
                        pl.col(col).mean().alias(f"mean_{col}"),
                        pl.col(col).std().alias(f"std_{col}"),
                        pl.col(col).count().alias(f"n_{col}"),
                    ]
                    for col in cols
                ]
            )
        )
        mean_ret = group_stats.select(
            *stats_grouper,
            *[pl.col(f"mean_{col}").alias(col) for col in cols]
        )

    # 计算标准误
    std_err_ret = group_stats.select(
        *stats_grouper,
        *[(pl.col(f"std_{col}") / pl.col(f"n_{col}").sqrt()).alias(col) for col in cols],
    )

    # 计算t统计量
    t_stat_ret = group_stats.select(
        *stats_grouper,
        *[(pl.col(f"mean_{col}") / (pl.col(f"std_{col}") / pl.col(f"n_{col}").sqrt())).alias(col) for col in cols],
    )

    return (mean_ret
            .drop_nulls(stats_grouper)
            .sort(by=stats_grouper),
            std_err_ret
            .drop_nulls(stats_grouper)
            .sort(by=stats_grouper),
            t_stat_ret
            .drop_nulls(stats_grouper)
            .sort(by=stats_grouper)
            )


def compute_mean_returns_spread(mean_returns: pl.DataFrame,
                                long_quant: int,
                                short_quant: int,
                                factor_field: str = "factor",
                                std_err=None):
    """
    计算两个分位数之间的平均收益差异（Spread），并可选地计算该差异的标准误差和 t 统计量。

    该函数通过 Polars DataFrame 实现，按 `factor_quantile` 分组计算两个指定分位数的平均收益差异。
    如果提供了标准误差数据，还会计算收益差异的联合标准误差和 t 统计量。

    Parameters
    ----------
    mean_returns : pl.DataFrame
        包含按分位数计算的各期平均收益的 Polars DataFrame。
        必须包含 `factor_quantile` 列，以及与日期（如 "date"、"time"）或分组（如 "group"）相关的索引列。
        通常由 `mean_return_by_quantile` 方法生成。
    long_quant : int
        多头组
    short_quant : int
        空头组
    factor_field: str
    std_err : pl.DataFrame, optional
        （可选）包含按分位数计算的每期平均收益标准误差的 Polars DataFrame。
        格式必须与 `mean_returns` 相同，具有相同的列和索引。

    Returns
    -------
    mean_return_difference : pl.DataFrame
        每期分位数收益差异的 DataFrame，按列返回所有收益差异。
        包含索引（如 "date"、"time"、"group"）以及各期收益差异值。
    joint_std_err : pl.DataFrame or None
        每期收益差异的联合标准误差。如果未提供 `std_err` 参数，则返回 None。
        否则，返回包含联合标准误差的 DataFrame。
    t_stat_difference : pl.DataFrame or None
        每期收益差异的 t 统计量（差异值除以联合标准误差）。
        如果 `std_err` 为 None，则返回 None。
        否则，返回包含 t 统计量的 DataFrame。

    Notes
    -----
    1. `mean_returns` 和 `std_err` 必须具有相同的结构，且包含相同的索引列（如 "date"、"time" 等）。
    2. 计算收益差异时，使用 `upper_quant` 和 `lower_quant` 对 `factor_quantile` 进行筛选。
    3. 如果 `std_err` 可用，则联合标准误差按公式计算：
       `sqrt(std_err_upper_quant^2 + std_err_lower_quant^2)`。
    4. t 统计量的计算公式为：
       `t_stat = mean_return_difference / joint_std_err`。
    """

    cols = utils.get_timedelta_names(mean_returns.columns)
    index = [col for col in mean_returns.columns if col not in cols]
    quant_field = f"{factor_field}_quantile"
    if index:
        mean_return_difference = (
            mean_returns
            .filter(pl.col(quant_field) == long_quant)
            .join(
                mean_returns
                .filter(pl.col(quant_field) == short_quant),
                on=index, how="left", suffix="_right")
            .select(
                *index,
                *[pl.col(col) - pl.col(f"{col}_right") for col in cols]
            )
        )
    else:
        top_ret = mean_returns.filter(pl.col(quant_field) == long_quant).select(cols)
        bottom_ret = mean_returns.filter(pl.col(quant_field) == short_quant).select(cols)
        mean_return_difference = top_ret - bottom_ret

    if std_err is None:
        joint_std_err = None
    else:
        if index:
            joint_std_err = (
                std_err
                .filter(pl.col(quant_field) == long_quant)
                .join(
                    std_err
                    .filter(pl.col(quant_field) == short_quant),
                    on=index, how="left")
                .select(
                    *index,
                    *[(pl.col(col) ** 2 + pl.col(f"{col}_right") ** 2).sqrt() for col in cols]
                )
            )
        else:
            top_err = std_err.filter(pl.col(quant_field) == long_quant)
            bottom_err = std_err.filter(pl.col(quant_field) == short_quant)
            joint_std_err = top_err.select(
                (pl.col(col) ** 2 + bottom_err[col] ** 2).sqrt() for col in cols
            )
    if joint_std_err is None:
        t_stat_difference = None
    else:
        if index:
            t_stat_difference = (
                mean_return_difference.join(
                    joint_std_err,
                    on=index, how="left"
                ).select(
                    *index,
                    *[(pl.col(col) / pl.col(f"{col}_right")) for col in cols]
                )
            )
        else:
            t_stat_difference = mean_return_difference / joint_std_err
    return mean_return_difference, joint_std_err, t_stat_difference


def quantile_turnover(factor_data: pl.DataFrame,
                      factor_field: str = "factor",
                      by_time=False,
                      lag=1):
    """
    计算因子分位数（quantile）的换手率（Turnover），即当前期分位数资产集合
    与上一期分位数资产集合的差异比例。

    Parameters
    ----------
    factor_data : pl.DataFrame
        包含因子数据的 Polars DataFrame，必须包括以下列：
        - 'factor_quantile': 因子分位数。
        - 'date': 日期。
        - 'time': 时间（如果按时间分组分析，则此列必需）。
        - 'asset': 资产名称或标识。
    factor_field: str
    by_time : bool, optional
        是否按时间（`time` 列）进一步分组进行换手率计算。
        默认为 False，即仅按 `factor_quantile` 和 `date` 计算。
        - True: 时间对齐后计算换手，比如09:31:00的换手是相对于上一天的09:31:00
    lag : int, optional
        时间偏移间隔，用于计算换手率的时间跨度。
        默认为 1，即计算相邻时间段的换手率。

    Returns
    -------
    turnover_data : pl.DataFrame
        包含换手率的 Polars DataFrame，结果包括以下列：
        - 'factor_quantile': 因子分位数。
        - 'date': 日期。
        - 'time': 时间
        - 'turnover': 换手率，表示当前分位数中新增资产的比例。

    Notes
    -----
    - 换手率公式：
       `turnover = len(差集资产集合) / len(当前资产集合)`，
       差集资产集合为当前期资产集合中不属于上一期的资产。
    - 如果 `by_time=True`，则按 `factor_quantile` 和 `time` 进一步分组计算。
    - 如果某期资产集合为空或上一期资产集合缺失，则该期换手率无法计算。
    """
    quant_field = f"{factor_field}_quantile"
    factor_data = factor_data.drop_nulls(subset=quant_field)
    index = list({"date", "time"}.intersection(factor_data.columns))
    grouper = [quant_field, *index]
    cur_asset_set = factor_data.group_by(grouper).agg(
        pl.col("asset").unique()
    ).sort(by=grouper)
    shift_grouper = [quant_field, ]
    if by_time:
        shift_grouper.append("time")
    prev_asset_set = cur_asset_set.select(
        *grouper,
        pl.col("asset").shift(lag).over(shift_grouper)
    )
    return cur_asset_set.join(
        prev_asset_set, on=grouper, how="left", suffix="_prev"
    ).with_columns(
        pl.col("asset").list.set_difference("asset_prev").alias("asset_diff").list.len().alias("diff_count"),
        pl.col("asset").list.len().alias("cur_count"),
    ).select(
        quant_field, *index,
        (pl.col("diff_count") / pl.col("cur_count")).alias("turnover")
    )

@unstable()
def ts_quantile_returns(factor_data: pl.LazyFrame,
                        ref_data: pl.LazyFrame,
                        factor_field: str = "factor",
                        N: int = 10,
                        by_date: bool = True) -> pl.DataFrame:
    """
    时序分组收益，根据ref_data(过去一段时间的因子值) 进行分组

    .. warning::
            This functionality is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.
    """
    factor_data = factor_data.lazy()
    ref_data = ref_data.lazy()
    assert "asset" in ref_data.collect_schema().names(), "ref_data must contain 'asset' column"
    index = ["date", "asset"]
    for field in index:
        assert field in factor_data.collect_schema().names(), f"factor_data must contain '{field}' column"
    ret_cols = utils.get_timedelta_names(factor_data.collect_schema().names())
    if not ret_cols:
        raise ValueError("factor_data must contain return columns")
    factor_data = factor_data.select(*index, factor_field, *ret_cols)
    ref_data = ref_data.select("asset", factor_field)
    quantiles = np.linspace(0, 1, N+1)
    quantile_df = ref_data.group_by("asset").agg(pl.quantile(factor_field, q).alias(f"{factor_field}_G{i}") for i, q in enumerate(quantiles))
    factor_data = (
        quantile_df
        .join(factor_data, on="asset", how="left")
        .collect()
    )
    rets = list()
    for lower in range(N):
        upper = lower + 1
        ret = (factor_data
               .filter(pl.col(f"{factor_field}_G{lower}") <= pl.col(factor_field), pl.col(f"{factor_field}_G{upper}") >= pl.col(factor_field),)
               .select("date", *ret_cols)
               .group_by("date")
               .mean()
               .with_columns(quantile=pl.lit(upper))
               )
        rets.append(ret)
    result = pl.concat(rets).select("date", "quantile", *ret_cols)
    if by_date:
        return result.sort("date", "quantile")
    return result.drop("date").group_by("quantile").mean().sort("quantile")

def ts_spread(factor_data: pl.LazyFrame,
              ref_data: pl.LazyFrame,
              factor_field: str = "factor",
              N: int = 10,
              reverse: bool = False,
              by_date: bool = True):
    factor_data = factor_data.lazy()
    ref_data = ref_data.lazy()
    assert "asset" in ref_data.collect_schema().names(), "ref_data must contain 'asset' column"
    index = ["date", "asset"]
    for field in index:
        assert field in factor_data.collect_schema().names(), f"factor_data must contain '{field}' column"
    ret_cols = utils.get_timedelta_names(factor_data.collect_schema().names())
    if not ret_cols:
        raise ValueError("factor_data must contain return columns")
    factor_data = factor_data.select(*index, factor_field, *ret_cols)
    ref_data = ref_data.select("asset", factor_field)
    quantiles = np.linspace(0, 1, N+1)
    long = quantiles[-2:] if not reverse else quantiles[:2]
    short = quantiles[:2] if not reverse else quantiles[-2:]
    ref_gdf = ref_data.group_by("asset")
    long_lower, long_upper = ref_gdf.quantile(long[0]).rename({factor_field: "long_lower"}), ref_gdf.quantile(long[-1]).rename({factor_field: "long_upper"})
    short_lower, short_upper = ref_gdf.quantile(short[0]).rename({factor_field: "short_lower"}), ref_gdf.quantile(short[-1]).rename({factor_field: "short_upper"})
    factor_data = pl.concat([factor_data, long_lower, long_upper, short_lower, short_upper], how="align").collect()
    long_data = (
        factor_data
        .filter(pl.col(factor_field) >= pl.col("long_lower"), pl.col(factor_field) <= pl.col("long_upper"))
        .select("date", *ret_cols)
        .group_by("date")
        .mean()
        .rename({col: f"{col}_long" for col in ret_cols})
    )

    short_data = (
        factor_data
        .filter(pl.col(factor_field) >= pl.col("short_lower"), pl.col(factor_field) <= pl.col("short_upper"))
        .select("date", *ret_cols)
        .group_by("date")
        .mean()
        .rename({col: f"{col}_short" for col in ret_cols})
    )
    result = (long_data
              .join(short_data, on="date", how="left")
              .with_columns((pl.col(f"{col}_long") - pl.col(f"{col}_short")).alias(f"{col}_spread") for col in ret_cols)
              )
    if by_date:
        return result.sort("date")
    return result.drop("date").mean()


