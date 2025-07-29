# -*- coding: utf-8 -*-
"""
---------------------------------------------
Created on 2025/6/8 14:29
@author: ZhangYundi
@email: yundi.xxii@outlook.com
@description: 
---------------------------------------------
"""
import time

import polars as pl
from quda.data.zoo import base
import ylog
import ygo

from quda.data.zoo.base import fac_components



def test_components():
    test_date = "2025-05-06"
    w = fac_components(index_code="000852").get_value(test_date)
    ylog.info(w)

def test_base_quote():
    test_date1 = "2025-05-06"
    test_date2 = "2025-07-04"
    data1 = base.fac_base_quote.get_value(test_date1)
    data2 = base.fac_base_quote(env="rt").get_value(test_date2)
    ylog.info(data1.head())
    ylog.info(data2.head())

def test_filter():
    test_date = "2025-05-06"
    data = base.fac_filter.get_value(test_date)
    ylog.info(data.filter(pl.col("cond") > 0))

def test_filter_notindex():
    test_date = "2025-05-06"
    data = base.fac_filter_notindex(index_codes=["000016", ]).get_value(test_date)
    ylog.info(data.filter(pl.col("cond").is_null()))

def test_get_value():
    test_date = "2025-05-06"
    data = base.fac_kline_minute.get_value(date=test_date, time="09:31:00")
    # data = base.fac_filter.get_value(date=test_date, time="09:00:00")
    ylog.info(data)

def test_get_history():
    test_date = "2025-05-06"
    data = base.fac_filter.get_history(date=test_date, period="-1000d",)
    ylog.info(data)

def test_ipo():
    test_date = "2025-05-30"
    data = base.fac_ipo(days=90).get_value(date=test_date)
    ylog.info(data)

def test_st():
    test_date = "2025-05-30"
    data = base.fac_st.get_value(date=test_date)
    ylog.info(data)



if __name__ == '__main__':
    import quda
    # print(FactorContext.__dataclass_fields__.keys())
    # print(ygo.fn_info(ygo.delay(base.fac_prev_close.fn)(env="rt")))
    # test_base_quote()
    # test_filter()
    # test_components()
    # test_filter_notindex()
    # test_get_value()
    test_get_history()
    # test_ipo()
    # data = quda.sql("select * from mc/stock_kline_minute where date='2025-05-30';")
    # ylog.info(data.collect())