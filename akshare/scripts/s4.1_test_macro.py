#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 宏观经济数据接口测试 (阶段4.1)"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 宏观经济数据接口测试")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()


def test(api_name, fn, *args, **kwargs):
    print(f"\n{'-'*50}")
    print(f"测试: {api_name}")
    try:
        d = fn(*args, **kwargs)
        if isinstance(d, pd.DataFrame) and len(d) > 0:
            print(f"  ✓ {len(d)} rows, cols={list(d.columns)[:6]}")
        else:
            print(f"  ✓ {type(d).__name__}")
        return d
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {str(e)[:60]}")
        return None


print("=" * 80)
print("1. 中国主要经济指标")
print("=" * 80)
test("GDP年率", ak.macro_china_gdp_yearly)
test("CPI", ak.macro_china_cpi)
test("PPI", ak.macro_china_ppi)
test("PMI", ak.macro_china_pmi)
test("LPR利率", ak.macro_china_lpr)
test("M2货币供应", ak.macro_china_m2_yearly)
test("贸易顺差", ak.macro_china_trade_balance)
test("SHIBOR", ak.macro_china_shibor_all)
test("固投", ak.macro_china_gdzctz)
test("海关进出口", ak.macro_china_hgjck)
test("存款准备金率", ak.macro_china_reserve_requirement_ratio)

print("\n" + "=" * 80)
print("2. 美国主要经济指标")
print("=" * 80)
test("CPI月度", ak.macro_usa_cpi_monthly)
test("非农就业", ak.macro_usa_non_farm)
test("失业率", ak.macro_usa_unemployment_rate)
test("ISM制造业PMI", ak.macro_usa_ism_pmi)

print("\n" + "=" * 80)
print("3. 利率对比")
print("=" * 80)
test("美联储利率", ak.macro_bank_usa_interest_rate)
test("中国基准利率", ak.macro_bank_china_interest_rate)
test("欧央行利率", ak.macro_bank_euro_interest_rate)

print("\n" + "=" * 80)
print("4. 航运指数")
print("=" * 80)
test("BDI", ak.macro_shipping_bdi)

print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print("✓ 宏观经济接口测试完成")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
