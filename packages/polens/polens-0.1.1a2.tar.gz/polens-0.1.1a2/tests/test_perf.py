# -*- coding: utf-8 -*-
"""
---------------------------------------------
Copyright (c) 2025 ZhangYundi
Licensed under the MIT License. 
Created on 2025/7/14 10:51
Email: yundi.xxii@outlook.com
Description: 
---------------------------------------------
"""

import quda
import xcals
from quda.ml import transformer
from quda.data import zoo
import polars as pl
from quda.factor import INDEX, FIELD_ASSET, FIELD_DATE
from sklearn.pipeline import make_pipeline
from polens.tears import performance, utils

def read_data(date, freq="10s"):
    time_ = "09:31:00"
    tick_cleaned = quda.sql(f"select * from mc/stock_ytick where date='{date}' and freq='{freq}';").drop("freq")
    filter_val = zoo.fac_filter.get_value(date, time=time_).filter(pl.col("cond") < 1).lazy()
    return filter_val.select(FIELD_ASSET).join(tick_cleaned, on=FIELD_ASSET, how="left")

def prepare_data(date, freq="10s"):
    exprs = [
        "ask_p1", "bid_p1",
        "if(bid_p5 > 0, sum(bid_p1*bid_v1,bid_p2*bid_v2,bid_p3*bid_v3,bid_p4*bid_v4,bid_p5*bid_v5)/1e4, null) as bid_amt",
        "if(ask_p5 > 0, sum(ask_p1*ask_v1,ask_p2*ask_v2,ask_p3*ask_v3,ask_p4*ask_v4,ask_p5*ask_v5)/1e4, null) as ask_amt",
        "bid_amt/1e4/sum(bid_v1,bid_v2,bid_v3,bid_v4,bid_v5) as bid_vwap",
        "ask_amt/1e4/sum(ask_v1,ask_v2,ask_v3,ask_v4,ask_v5) as ask_vwap",
        "(ask_vwap-bid_vwap)/(ask_vwap+bid_vwap)/2 * 1e4 as vwap_spread",
        f"itd_mean(vwap_spread, 100) as vwap_spread_ma100",
    ]
    target_tf = transformer.Target(price_tag="if(ask_p1 > 0 and bid_p1 > 0, (ask_p1 + bid_p1)/2, null) as mid_p",
                                   frequency=freq, target="1d", gap=freq)
    dropnull_tf = transformer.FilterNotNull(subset=[f"vwap_spread_ma100", "1d"])
    pipe = make_pipeline(target_tf, dropnull_tf)
    data = read_data(date, freq=freq)
    data = quda.to_lazy(data).sql(*exprs)
    data = pipe.fit_transform(data)
    # data = utils.add_factor_quantile(data.collect(), f"vwap_spread_ma{length}", bins=10, by_group=False)
    return data


if __name__ == '__main__':
    test_date = "2025-04-30"
    length = 500
    data = prepare_data(test_date, )
    ref_beg = "2025-04-20"
    ref_end = "2025-04-29"
    ref_data = pl.concat([prepare_data(d) for d in xcals.get_tradingdays(ref_beg, ref_end)])
    # perf = performance.quantile_returns(data, factor_field=f"vwap_spread_ma{length}", stats_grouper=["asset"])
    # print(perf[0].group_by("vwap_spread_ma500_quantile").agg(pl.col("1d").mean()))
    perf = performance.ts_quantile_returns(data, ref_data, factor_field=f"vwap_spread_ma100", N=20)
    # perf = performance.ts_quantile_returns(data, ref_data, factor_field=f"ask_amt", N=10)
    print(perf)