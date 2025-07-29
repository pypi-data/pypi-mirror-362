# -*- coding: utf-8 -*-
"""
---------------------------------------------
Copyright (c) 2025 ZhangYundi
Licensed under the MIT License. 
Created on 2025/7/9 15:03
Email: yundi.xxii@outlook.com
Description: 
---------------------------------------------
"""

import polars as pl
from .order import OrderConfig, create_order, summary_order_uc
import pandas as pd

def from_signal(signal_data: pl.LazyFrame,
                open_configs: list[OrderConfig],
                cover_configs: list[OrderConfig],
                cover: bool = True,
                limit: bool = True,
                fee: float = 5e-4,
                tax: float = 5e-4,
                show_notebook: bool = True):

    order_oss = create_order(signal_data, open_configs=open_configs, cover_configs=cover_configs, cover=cover)
    order_uc = summary_order_uc(order_oss, limit=limit, fee=fee, tax=tax, )
    account_value = (
        signal_data
        .select("date", "asset", "prev_close", "limit_qty")
        .unique(subset=["date", "asset"])
        .group_by("date")
        .agg(
            (pl.col("prev_close") * pl.col("limit_qty")).sum().alias("account_value")
        )
    )
    daily_asset_num = (
        signal_data
        .group_by("date")
        .agg(asset_num=pl.col("asset").n_unique())
    )

    # todo: summary - 交易胜率/日胜率/平均单笔/盈亏比/股票覆盖度/信号量/换手/ 预测胜率 / 交易胜率
    day_pnl_df = (
        order_uc
        .group_by("date")
        .agg(pl.col("pnl").sum())
        .join(account_value, on="date", how="left")
        .select("date", "pnl", 'account_value')
        .sort("date")
    )
    # 交易胜率
    win_ratio = order_uc.select((pl.col("pnl") > 0).mean())
    # 日胜率
    day_win_ratio = day_pnl_df.select((pl.col("pnl") > 0).mean())
    # 平均单笔
    bp = day_pnl_df.select((pl.col("pnl").sum() / pl.col("account_value").sum() * 1e4))
    # 盈亏比
    win_loss_ratio = (
            order_uc
            .filter(pl.col("pnl") > 0)
            .select("pnl")
            .sum() /
            order_uc
            .filter(pl.col("pnl") < 0)
            .select(pl.col("pnl").abs())
            .sum()
    )
    summary_df = pl.concat([win_ratio,
                            day_win_ratio,
                            bp,
                            win_loss_ratio],
                           how="vertical")
    summary_df = summary_df.to_pandas()
    summary_df.index = pd.Index(["Win Ratio/Trade", "Win Ratio/Day", "BP", "Profit/Loss"], name="metric")
    # summary_df = dc.to_pl(summary_df.reset_index()).select("metric", *[pl.col(period).round(2) for period in periods_cols])

    # print(summary_df)
    tb = finplot.table(summary_df.round(2).reset_index())
    if show_notebook:
        tb.show()
    # 股票覆盖度
    coverage = (
        order_uc
        .group_by("date")
        .agg(pl.col("asset").n_unique().alias("signal_asset_num"))
        .join(daily_asset_num, on="date", how="right", )
        .select("date", coverage=(pl.col("signal_asset_num") / pl.col("asset_num")).fill_null(0.0))
        .sort("date")
    )

    # 换手
    turnover = (
        order_uc
        .group_by("date")
        .agg(open_amt=(pl.col("order_qty") * pl.col("price")).sum())
        .join(account_value, on="date", how="right")
        .select("date", turnover=pl.col("open_amt") / pl.col("account_value"))
        .fill_null(0.0)
        .sort("date")
    )
    fig_coverage = finplot.bar_plot(coverage.to_pandas().set_index("date", drop=True),
                                    title=f"coverage (median: {(coverage["coverage"].median() * 100):.2f}%)")
    if show_notebook:
        fig_coverage.show()
    fig_turnover = finplot.bar_plot(turnover.to_pandas().set_index("date", drop=True),
                                    title=f"turnover (median: {(turnover["turnover"].median() * 100):.2f}%)")
    if show_notebook:
        fig_turnover.show()
    figs = [tb, fig_coverage, fig_turnover]
    nv_df = (
        day_pnl_df
        .with_columns(pl.col("pnl") / pl.col("account_value"))
        .fill_null(0.0)
        .with_columns((pl.col("pnl") + 1).cum_prod())
    )
    nv_pd = nv_df.to_pandas().set_index("date", drop=True)
    fig, metric = finplot.nv_plot(nv_pd["pnl"])

    summary = dc.to_pl(summary_df.reset_index()).select("metric", pl.col("pnl").round(2))
    summary_dict = summary.to_dicts()
    for item in summary_dict:
        metric[item["metric"]] = item["pnl"]
    if show_notebook:
        fig.show()
    figs.append(fig)

    return {
        "info": order_uc,
        "summary": summary,
        "pnl": day_pnl_df,
        "nv": nv_df,
        "figs": figs,
    }, metric
