#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 期权数据接口测试 (阶段3.2)

测试目标：
1. ETF期权（50ETF/300ETF）实时行情、希腊字母、日线
2. 股指期权（沪深300/上证50/中证1000）
3. 商品期权与波动率
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 期权数据接口测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()


def test_api(api_name, api_func, *args, **kwargs):
    print(f"\n{'-'*60}")
    print(f"测试接口: {api_name}")
    print(f"{'-'*60}")
    try:
        result = api_func(*args, **kwargs)
        print(f"✓ 成功获取数据")
        if isinstance(result, pd.DataFrame):
            print(f"  数据行数: {len(result)}")
            print(f"  数据列数: {len(result.columns)}")
            print(f"  数据列名: {list(result.columns)[:6]}")
            print(f"  前2行数据:")
            print(result.head(2).to_string())
        return result
    except Exception as e:
        print(f"✗ 失败: {type(e).__name__}: {str(e)[:80]}")
        return None


# ========================================================================
# 1. ETF期权
# ========================================================================
print("\n" + "="*80)
print("1. ETF期权（上交所）")
print("="*80)

# 1.1 期权代码列表
print("\n>>> 50ETF 2026年5月看涨期权列表")
test_api("option_sse_codes_sina(50ETF购5月)", ak.option_sse_codes_sina,
         symbol="看涨期权", trade_date="202605", underlying="510050")

print("\n>>> 50ETF 2026年5月认沽期权列表")
test_api("option_sse_codes_sina(50ETF沽5月)", ak.option_sse_codes_sina,
         symbol="认沽期权", trade_date="202605", underlying="510050")

# 1.2 期权实时行情（用已知代码）
print("\n>>> 50ETF购5月2700 实时行情")
test_api("option_sse_spot_price_sina", ak.option_sse_spot_price_sina, symbol="10011381")

# 1.3 期权希腊字母
print("\n>>> 50ETF购5月2700 希腊字母")
test_api("option_sse_greeks_sina", ak.option_sse_greeks_sina, symbol="10011381")

# 1.4 期权日线
print("\n>>> 50ETF购5月2700 日线")
test_api("option_sse_daily_sina", ak.option_sse_daily_sina, symbol="10011381")

# 1.5 标的行情
print("\n>>> 期权标的行情")
test_api("option_sse_underlying_spot_price_sina", ak.option_sse_underlying_spot_price_sina)

# ========================================================================
# 2. 股指期权（中金所）
# ========================================================================
print("\n" + "="*80)
print("2. 股指期权（中金所）")
print("="*80)

test_api("option_cffex_hs300_spot_sina (沪深300)", ak.option_cffex_hs300_spot_sina)
test_api("option_cffex_sz50_spot_sina (上证50)", ak.option_cffex_sz50_spot_sina)
test_api("option_cffex_zz1000_spot_sina (中证1000)", ak.option_cffex_zz1000_spot_sina)

# ========================================================================
# 3. 波动率数据
# ========================================================================
print("\n" + "="*80)
print("3. 波动率数据")
print("="*80)

test_api("option_vol_shfe (上期所波动率)", ak.option_vol_shfe)

# ========================================================================
# 总结
# ========================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)
print("✓ 已测试的期权数据接口包括：")
print("  1. ETF期权（50ETF）代码列表、实时行情、希腊字母、日线")
print("  2. 股指期权（沪深300/上证50/中证1000）")
print("  3. 波动率数据（上期所）")
print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
