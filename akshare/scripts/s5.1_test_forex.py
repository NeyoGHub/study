#!/usr/bin/env python3
"""AkShare 外汇数据接口测试 (阶段5.1)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare 外汇数据接口测试")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

def test(name, fn, **kw):
    print(f"{'-'*50}")
    print(f"测试: {name}")
    try:
        d = fn(**kw)
        if hasattr(d, '__len__') and len(d) > 0:
            print(f"  ✓ {len(d)} rows, cols={list(d.columns)[:6]}")
            print(d.head(2).to_string())
        elif d is not None:
            print(f"  ✓ {d}")
        return d
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {str(e)[:60]}")
        return None

print("=" * 70)
print("1. 外汇牌价")
print("=" * 70)
test("currency_boc_sina (中行外汇牌价)", ak.currency_boc_sina)

print("\n2. 货币对报价")
test("fx_pair_quote (货币对报价)", ak.fx_pair_quote)
test("fx_spot_quote (即期报价)", ak.fx_spot_quote)
test("fx_swap_quote (掉期报价)", ak.fx_swap_quote)

print("\n" + "=" * 70)
print("测试总结")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
