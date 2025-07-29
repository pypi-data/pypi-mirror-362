# -*- coding: utf-8 -*-
"""
---------------------------------------------
Copyright (c) 2025 ZhangYundi
Licensed under the MIT License. 
Created on 2025/7/9 14:02
Email: yundi.xxii@outlook.com
Description: 
---------------------------------------------
"""

import polars as pl

class OrderConfig:

    def __init__(self, signal: str, order_unit: int = 100, amount_unit: float = -1):
        self.signal = signal
        self.order_unit = order_unit
        self.amount_unit = amount_unit

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(signal={self.signal}, order_unit={self.order_unit}, amount_unit={self.amount_unit})"

    def __repr__(self):
        return self.__str__()

def create_open_order(signal_data: pl.LazyFrame, open_config: OrderConfig) -> pl.LazyFrame:
    """
    创建开仓单
    Parameters
    ----------
    signal_data: polars.LazyFrame
        信号数据, 必须包含 `price` 列 以及 order_config.signal 列
    open_config: OrderConfig
        订单配置
    Returns
    -------
    polars.LazyFrame
    """
    assert open_config.signal in signal_data.collect_schema().names(), f"create_open_order.signal_data 缺少 `{open_config.signal}` 列"
    scalar = pl.lit(1) if open_config.amount_unit < 0 else (open_config.amount_unit / pl.col("price") / open_config.order_unit).ceil()
    return (
        signal_data
        .with_columns(
            (pl.col(open_config.signal) * scalar * open_config.order_unit).fill_null(0).cast(pl.Int32).alias(f"order_qty_{open_config.signal}")
        )
    )

def create_open_orders(signal_data: pl.LazyFrame, open_configs: list[OrderConfig]) -> pl.LazyFrame:
    """创建多个信号的开仓单"""
    open_orders = [create_open_order(signal_data, open_config) for open_config in open_configs]
    open_orders = pl.concat(open_orders, how="diagonal")
    open_orders = (
        open_orders
        .drop("^.*open_signal.*$", "^.*cover_signal.*$", strict=False)
        .with_columns(selected_signal=pl.sum_horizontal("^.*signal.*$"),
                      order_qty=pl.sum_horizontal("^.*order_qty.*$"),)
        .with_columns(open_signal=pl.col("order_qty").sign(),
                      direction=pl.col("order_qty").sign())
        .with_columns(order_qty=pl.col("order_qty").abs(),
                      is_open=pl.col("open_signal").abs())
    )
    date_window_spec = dict(partition_by=["date", "asset"], order_by="time")
    open_orders = (
        open_orders
        .filter(pl.col("is_open") > 0)
        .with_columns(last_direction=pl.col("direction").shift(1).over(**date_window_spec).fill_null(0))
        .with_columns(
            action_id=pl.when(pl.col("direction") != pl.col("last_direction")).then(1).otherwise(0).cum_sum().over(
                **date_window_spec))
        .drop("last_direction")
    )

    return open_orders

def cover_order_rs(open_order: pl.LazyFrame) -> pl.LazyFrame:
    """平仓单: 信号反转 reversed signal"""
    cols = open_order.columns
    check_fields = ["direction", "order_qty"]
    for field in check_fields:
        assert field in cols, f"cover_order_rs.open_order 缺少 `{field}` 列"
    date_window_spec = dict(partition_by=["date", "asset"], order_by="time")
    open_window_spec = dict(partition_by=["date", "asset", "action_id"], order_by="time")
    open_order = (
        open_order
        .with_columns(cum_open_qty=pl.col("order_qty").cum_sum().over(**open_window_spec).fill_null(0))
        .with_columns(last_cum_open_qty=pl.col("cum_open_qty").shift(1).over(**date_window_spec).fill_null(0),
                      last_direction=pl.col("direction").shift(1).over(**date_window_spec).fill_null(0))
    )
    cover_order = (
        open_order
        .with_columns(order_qty=pl.when(pl.col("last_direction") != 0,
                                        pl.col("direction") != pl.col("last_direction"))
                      .then(pl.col("last_cum_open_qty"))
                      .otherwise(None))
        .drop_nulls(subset=["order_qty"])
        .with_columns(is_open=pl.lit(0))
        .select(cols)
    )
    return cover_order

def cover_order_t0(order_data: pl.LazyFrame) -> pl.LazyFrame:
    """
    平仓单: t0收盘平掉所有敞口
    """
    cols = order_data.columns
    check_fields = ["price", "direction", "order_qty"]
    for field in check_fields:
        assert field in cols, f"`cover_order_t0.order_data` 缺少必要字段 {field}"
    # 当天的累计敞口
    total_qty = order_data.group_by("date", "asset").agg(total_qty=(pl.col("order_qty") * pl.col("direction")).sum())
    cover_order = (
        total_qty
        .with_columns(direction=-pl.col("total_qty").sign(),
                      order_qty=pl.col("total_qty").abs(), )
        .filter(pl.col("order_qty") > 0)
        .drop("total_qty")
    )
    return cover_order

def create_order(signal_data: pl.DataFrame | pl.LazyFrame,
                 open_configs: list[OrderConfig],
                 cover_configs: list[OrderConfig],
                 cover=True) -> pl.LazyFrame:
    """
    根据信号进行开平仓

    Parameters
    ----------
    signal_data: polars.DataFrame | polars.LazyFrame
    open_configs: list[OrderConfig]
    cover_configs: list[OrderConfig]
    cover: bool

    Returns
    -------
    polars.DataFrame | polars.LazyFrame
    """

    signal_data = signal_data.lazy()
    assert "price" in signal_data.collect_schema().names(), f"create_order.signal_data 缺少 `price` 列"
    open_orders = create_open_orders(signal_data, open_configs)
    open_orders_shadow = create_open_orders(signal_data, cover_configs)
    cover_orders = cover_order_rs(open_orders_shadow)
    cover_orders = (
        cover_orders
        .with_columns(is_close=pl.lit(1),
                      cover_signal=pl.col("selected_signal"))
    )
    orders = pl.concat([open_orders, cover_orders], how="diagonal").sort("date", "time", "asset", "is_open")
    date_window_spec = dict(partition_by=["date", "asset"], order_by="time")
    action_window_spec = dict(partition_by=["date", "asset", "action_id"], order_by="time")
    orders = (
        orders
        .drop("selected_signal")
        .with_columns(last_open_signal=pl.col("open_signal").shift(1).over(**date_window_spec))
        .filter(~pl.all_horizontal(pl.col("open_signal").is_null(),
                                   pl.col(
                                       "last_open_signal").is_null(), ))  # open_signal 为 Null，则必是平仓单，如果last_open_direction 为Null, 说明这是无效平仓单，剔除
        .with_columns(pl.col("open_signal").fill_null(0),
                      pl.col("cover_signal").fill_null(0),
                      pl.col("last_open_signal").fill_null(0))
        .filter(pl.col("last_open_signal") != pl.col("cover_signal"), pl.col("open_signal") != pl.col("cover_signal"))
        .with_columns(last_cover_signal=pl.col("cover_signal").shift(1).over(**date_window_spec))
        .with_columns(action_id=pl.when(pl.col("last_cover_signal").abs() > 0,
                                        pl.col("open_signal") != pl.col("last_open_signal"))
                      .then(1)
                      .otherwise(0)
                      .cum_sum()
                      .over(**date_window_spec))
    )
    # 修复平仓单量
    orders = (
        orders
        .with_columns(open_qty=pl.when(pl.col("is_close") == 1).then(None).otherwise(pl.col("order_qty")))
        .with_columns(cover_qty=pl.col("open_qty").cum_sum().forward_fill().over(**action_window_spec))
        .with_columns(order_qty=pl.when(pl.col("is_open") == 1).then(pl.col("open_qty")).otherwise(pl.col("cover_qty")))
        .drop("open_qty", "cover_qty")
    )
    if cover:
        latest_signal_data = signal_data.group_by("date", "asset").agg(pl.all().last())
        cover_orders = cover_order_t0(orders)
        cover_orders = (
            cover_orders
            .select("date", "asset", "direction", "order_qty")
            .join(latest_signal_data.select("date", "time", "asset", "price"),
                  on=["date", "asset"],
                  how="left")
            .with_columns(
                is_open=pl.lit(0),
                is_close=pl.lit(1),
            )
        )
        orders = pl.concat([orders, cover_orders], how="diagonal").sort("date", "time", "asset", "is_open")
        orders = orders.with_columns(action_id=pl.col("action_id").forward_fill().over(**date_window_spec))
    return orders

def summary_order_uc(order_data: pl.LazyFrame, limit: bool = True, fee: float = 5e-4, tax: float = 5e-4) -> pl.LazyFrame:
    """订单数据统计: 添加`pnl`列以及过滤只留下开仓信号"""
    action_window_spec = dict(partition_by=["date", "asset", "action_id"], order_by="time")
    window_spec = dict(partition_by=["date", "asset"], order_by="time")

    order_data = (
        order_data
        .with_columns(
            cover_price=pl.when(pl.col("is_open") == 0).then(pl.col("price")).otherwise(None).backward_fill().over(
                **action_window_spec),
            cover_time=pl.when(pl.col("is_open") == 0).then(pl.col("time")).otherwise(None).backward_fill().over(
                **action_window_spec))
    )
    if limit:
        assert "limit_qty" in order_data.columns, f"创建订单数据源必须包含 `limit_qty` 列"
        # 根据 limit_qty 修改订单数量
        order_data = (order_data
                      .filter(pl.col("is_open") == 1)
                      .sort("date", "time", "asset")
                      .with_columns(order_qty=pl.col("order_qty").clip(upper_bound=pl.col("limit_qty")))
                      .with_columns(cum_qty=pl.col("order_qty").cum_sum().over("date", "asset", order_by="time"))
                      .with_columns(cum_qty=pl.col("cum_qty").clip(upper_bound=pl.col("limit_qty")))
                      .with_columns(order_qty=pl.col("cum_qty").diff().over(**window_spec).fill_null(pl.col("order_qty")))
                      .filter(pl.col("order_qty") > 0)
                      )

    order_data = (
        order_data
        .with_columns(pnl=pl.when(pl.col("direction") > 0)
                      .then(pl.col("cover_price") * (1 - fee - tax) - pl.col("price") * (1 + fee))
                      .otherwise(pl.col("price") * (1 - fee - tax) - pl.col("cover_price") * (1 + fee)))
        .with_columns(pnl=pl.col("pnl") * pl.col("order_qty"))
        .filter(pl.col("is_open") == 1)
    )
    return order_data



