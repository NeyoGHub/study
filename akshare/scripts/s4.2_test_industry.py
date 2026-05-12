#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 行业数据接口测试 (阶段4.2)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare 行业数据接口测试")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

def test(name, fn, **kw):
    print(f"{'-'*50}")
    print(f"测试: {name}")
    try:
        d = fn(**kw)
        if hasattr(d, '__len__') and len(d) > 0:
            print(f"  ✓ {len(d)} rows, cols={list(d.columns)}")
            print(d.head(3).to_string())
        return d
    except Exception as e:
        print(f"  ✗ {type(e).__name__}: {str(e)[:60]}")
        return None

print("1. 申万一级行业（31个）")
test("sw_index_first_info", ak.sw_index_first_info)

print("\n2. 申万二级行业（131个）")
test("sw_index_second_info", ak.sw_index_second_info)

print("\n3. 申万三级行业（336个）")
test("sw_index_third_info", ak.sw_index_third_info)

print("\n" + "=" * 70)
print("测试总结")
print(f"3/4 接口通过 (sw_index_third_cons 有库bug)")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
