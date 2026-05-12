#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 期货数据接口测试 (阶段3.1)

测试目标：
1. 期货行情（主力合约日线/分钟/实时）
2. 外盘期货（美油/黄金等）
3. 期现价差与库存
4. 能源/碳/生猪数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 期货数据接口测试")
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
            print(f"  数据列名: {list(result.columns)[:8]}")
            print(f"  前2行数据:")
            print(result.head(2).to_string())
        return result
    except Exception as e:
        print(f"✗ 失败: {type(e).__name__}: {str(e)[:80]}")
        return None


# ========================================================================
# 1. 期货品种与主连日线
# ========================================================================
print("\n" + "="*80)
print("1. 期货品种与主力合约")
print("="*80)

test_api("futures_display_main_sina (品种列表)", ak.futures_display_main_sina)

print("\n>>> 螺纹钢主力(RB0)日线")
test_api("futures_main_sina", ak.futures_main_sina, symbol="RB0")

print("\n>>> 沪铜主力(CU0)日线")
test_api("futures_main_sina", ak.futures_main_sina, symbol="CU0")

# ========================================================================
# 2. 期货日线与分钟数据
# ========================================================================
print("\n" + "="*80)
print("2. 期货日线与分钟数据")
print("="*80)

test_api("futures_zh_daily_sina (RB0日线)", ak.futures_zh_daily_sina, symbol="RB0")
test_api("futures_zh_minute_sina (RB0 5分钟)", ak.futures_zh_minute_sina, symbol="RB0", period="5")

# ========================================================================
# 3. 外盘期货
# ========================================================================
print("\n" + "="*80)
print("3. 外盘期货")
print("="*80)

test_api("futures_foreign_commodity_realtime (原油CL)", ak.futures_foreign_commodity_realtime, symbol="CL")
test_api("futures_foreign_commodity_realtime (黄金GC)", ak.futures_foreign_commodity_realtime, symbol="GC")
test_api("futures_foreign_detail (美豆ZSD)", ak.futures_foreign_detail, symbol="ZSD")

# ========================================================================
# 4. 期现价差与库存
# ========================================================================
print("\n" + "="*80)
print("4. 期现价差与库存")
print("="*80)

test_api("futures_spot_price_daily (期现价差)", ak.futures_spot_price_daily)
test_api("futures_spot_stock (期现库存)", ak.futures_spot_stock)
test_api("futures_inventory_em (大豆库存)", ak.futures_inventory_em, symbol="a")
test_api("futures_comex_inventory (COMEX库存)", ak.futures_comex_inventory)

# ========================================================================
# 5. 手续费与生猪数据
# ========================================================================
print("\n" + "="*80)
print("5. 手续费与生猪数据")
print("="*80)

test_api("futures_comm_js (手续费)", ak.futures_comm_js)
test_api("futures_hog_core (生猪核心)", ak.futures_hog_core)
test_api("futures_hog_cost (生猪成本)", ak.futures_hog_cost)

# ========================================================================
# 6. 能源数据
# ========================================================================
print("\n" + "="*80)
print("6. 能源数据")
print("="*80)

test_api("energy_oil_detail (原油价格)", ak.energy_oil_detail)
test_api("energy_oil_hist (油价调整)", ak.energy_oil_hist)

# ========================================================================
# 总结
# ========================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)
print("✓ 已测试的期货数据接口包括：")
print("  1. 期货品种列表 + 主力合约日线（螺纹钢/沪铜）")
print("  2. 期货日线 + 分钟数据")
print("  3. 外盘期货（原油/黄金/美豆）")
print("  4. 期现价差 + 库存数据（大豆/COMEX）")
print("  5. 手续费 + 生猪数据")
print("  6. 能源数据（原油价格/调价历史）")
print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
