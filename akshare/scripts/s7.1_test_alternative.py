#!/usr/bin/env python3
"""AkShare 空气质量+汽车+财富榜单 (阶段5.6)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare 阶段5.6 - 另类数据")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

def test(name, fn, **kw):
    try:
        d = fn(**kw)
        if hasattr(d, '__len__') and len(d) > 0:
            cols = list(d.columns[:6]) if hasattr(d, 'columns') else []
            print(f"  ✓ {name}: {len(d)} rows, cols={cols[:4]}")
        return d
    except Exception as e:
        print(f"  ✗ {name}: {type(e).__name__}: {str(e)[:50]}")
        return None

print("1. 空气质量")
test("air_quality_rank", ak.air_quality_rank)
test("air_quality_hist", ak.air_quality_hist)
test("air_city_table", ak.air_city_table)

print("\n2. 汽车市场")
test("car_sale_rank_gasgoo", ak.car_sale_rank_gasgoo)
test("car_market_total_cpca", ak.car_market_total_cpca)
test("car_market_cate_cpca", ak.car_market_cate_cpca)

print("\n3. 财富榜单")
test("forbes_rank", ak.forbes_rank)
test("hurun_rank", ak.hurun_rank)
test("xincaifu_rank", ak.xincaifu_rank)

print(f"\n{'='*70}")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
