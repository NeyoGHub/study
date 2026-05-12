#!/usr/bin/env python3
"""AkShare 龙虎榜+融资融券+沪深港通 (阶段5.5)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare 阶段5.5 - 市场微观数据")
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

print("1. 龙虎榜")
test("stock_lhb_detail_em", ak.stock_lhb_detail_em)
test("stock_lhb_hyyyb_em", ak.stock_lhb_hyyyb_em)
test("stock_lhb_jgstatistic_em", ak.stock_lhb_jgstatistic_em)
test("stock_lhb_ggtj_sina", ak.stock_lhb_ggtj_sina)

print("\n2. 融资融券")
test("stock_margin_sse", ak.stock_margin_sse)
test("stock_margin_szse", ak.stock_margin_szse)
test("stock_margin_detail_sse", ak.stock_margin_detail_sse)
test("stock_margin_detail_szse", ak.stock_margin_detail_szse)

print("\n3. 沪深港通")
test("stock_hsgt_hist_em", ak.stock_hsgt_hist_em)
test("stock_hsgt_sh_hk_spot_em", ak.stock_hsgt_sh_hk_spot_em)
test("stock_hsgt_hold_stock_em", ak.stock_hsgt_hold_stock_em)
test("stock_hsgt_individual_em", ak.stock_hsgt_individual_em)

print(f"\n{'='*70}")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
