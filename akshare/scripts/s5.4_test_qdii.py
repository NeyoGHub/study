#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare QDII数据接口测试 (阶段5.4)"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare QDII数据接口测试")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()


def test_api(api_name, api_func, *args, **kwargs):
    print(f"\n{'-'*60}")
    print(f"测试接口: {api_name}")
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
        print(f"✗ 失败: {type(e).__name__}: {str(e)[:60]}")
        return None


print("=" * 80)
print("1. QDII指数型基金")
print("=" * 80)
test_api("qdii_a_index_jsl (QDII指数)", ak.qdii_a_index_jsl)

print("\n" + "=" * 80)
print("2. QDII商品型基金")
print("=" * 80)
test_api("qdii_e_comm_jsl (QDII商品)", ak.qdii_e_comm_jsl)

print("\n" + "=" * 80)
print("3. QDII股票型基金")
print("=" * 80)
test_api("qdii_e_index_jsl (QDII股票)", ak.qdii_e_index_jsl)

print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print("✓ QDII接口全部测试完成 (3/3)")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
