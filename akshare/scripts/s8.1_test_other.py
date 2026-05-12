#!/usr/bin/env python3
"""AkShare 电影+能源扩展+利率扩展 (阶段5.7)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare 阶段5.7 - 其他数据扩展")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

def test(name, fn, **kw):
    try:
        d = fn(**kw)
        if hasattr(d, '__len__') and len(d) > 0:
            cols = list(d.columns[:6]) if hasattr(d, 'columns') else []
            print(f"  ✓ {name}: {len(d)} rows, cols={cols[:4]}")
        elif d is not None:
            print(f"  ✓ {name}: {d}")
        return d
    except Exception as e:
        print(f"  ✗ {name}: {type(e).__name__}: {str(e)[:50]}")
        return None

print("1. 电影票房")
for api in ['movie_boxoffice_realtime', 'movie_boxoffice_daily', 'movie_boxoffice_yearly']:
    fn = getattr(ak, api, None)
    if fn:
        test(api, fn)

print("\n2. 能源扩展")
test("energy_carbon_bj", ak.energy_carbon_bj)
test("energy_carbon_eu", ak.energy_carbon_eu)
test("energy_oil_detail", ak.energy_oil_detail)

print("\n3. 利率扩展")
test("repo_rate_query", ak.repo_rate_query)
test("macro_bank_japan_interest_rate", ak.macro_bank_japan_interest_rate)
test("macro_bank_uk_interest_rate", ak.macro_bank_uk_interest_rate)

print(f"\n{'='*70}")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
