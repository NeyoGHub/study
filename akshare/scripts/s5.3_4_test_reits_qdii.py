#!/usr/bin/env python3
"""AkShare REITs/QDII 数据接口测试 (阶段5.3 & 5.4)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare REITs & QDII 数据接口测试")
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
        return d
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {str(e)[:60]}")
        return None

print("=" * 70)
print("1. REITs数据（东方财富，当前可能不可用）")
print("=" * 70)
test("reits_realtime_em", ak.reits_realtime_em)
test("reits_hist_em(508097)", ak.reits_hist_em, symbol='508097')

print("\n" + "=" * 70)
print("2. QDII数据（集思录）")
print("=" * 70)
test("qdii_a_index_jsl (QDII指数)", ak.qdii_a_index_jsl)
test("qdii_e_comm_jsl (QDII商品)", ak.qdii_e_comm_jsl)
test("qdii_e_index_jsl (QDII股票)", ak.qdii_e_index_jsl)

print("\n" + "=" * 70)
print("测试总结")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
