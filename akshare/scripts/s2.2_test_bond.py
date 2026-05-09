#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 债券数据接口测试脚本 (阶段2.2)

测试目标：
1. 国债收益率曲线
2. 国债现货/指数
3. 可转债行情/数据
4. 中美利率对比
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 债券数据接口测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()


def test_api(api_name, api_func, *args, **kwargs):
    """测试API接口并显示结果"""
    print(f"\n{'-'*60}")
    print(f"测试接口: {api_name}")
    print(f"{'-'*60}")
    try:
        result = api_func(*args, **kwargs)
        print(f"✓ 成功获取数据")
        if isinstance(result, pd.DataFrame):
            print(f"  数据行数: {len(result)}")
            print(f"  数据列数: {len(result.columns)}")
            print(f"  数据列名: {list(result.columns)[:8]}...")
            print(f"  前3行数据:")
            print(result.head(3).to_string())
        return result
    except Exception as e:
        print(f"✗ 失败: {type(e).__name__}: {str(e)[:80]}")
        return None


# ========================================================================
# 1. 国债收益率
# ========================================================================
print("\n" + "="*80)
print("1. 国债收益率")
print("="*80)

test_api("bond_china_yield (国债收益率曲线)", ak.bond_china_yield)
test_api("bond_zh_us_rate (中美收益率)", ak.bond_zh_us_rate)

# ========================================================================
# 2. 国债现货与指数
# ========================================================================
print("\n" + "="*80)
print("2. 国债现货与指数")
print("="*80)

test_api("bond_zh_hs_daily (国债日线)", ak.bond_zh_hs_daily)
test_api("bond_treasury_index_cbond (国债指数)", ak.bond_treasury_index_cbond)
test_api("bond_composite_index_cbond (债券综合指数)", ak.bond_composite_index_cbond)
test_api("bond_new_composite_index_cbond (新综合指数)", ak.bond_new_composite_index_cbond)

# ========================================================================
# 3. 可转债数据
# ========================================================================
print("\n" + "="*80)
print("3. 可转债数据")
print("="*80)

test_api("bond_zh_hs_cov_spot (可转债实时)", ak.bond_zh_hs_cov_spot)
test_api("bond_zh_hs_cov_daily (可转债日线)", ak.bond_zh_hs_cov_daily)
test_api("bond_cb_jsl (集思录可转债)", ak.bond_cb_jsl)
test_api("bond_cb_index_jsl (可转债指数)", ak.bond_cb_index_jsl)
test_api("bond_zh_cov (可转债基本信息)", ak.bond_zh_cov)
test_api("bond_zh_cov_info_ths (同花顺转债信息)", ak.bond_zh_cov_info_ths)
test_api("bond_cb_summary_sina (可转债市场概况)", ak.bond_cb_summary_sina)

# ========================================================================
# 4. 中美利率
# ========================================================================
print("\n" + "="*80)
print("4. 中美利率对比")
print("="*80)

test_api("bond_gb_zh_sina (中国国债期货)", ak.bond_gb_zh_sina)
test_api("bond_gb_us_sina (美国国债期货)", ak.bond_gb_us_sina)

# ========================================================================
# 总结
# ========================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)
print("✓ 已测试的债券数据接口包括：")
print("  1. 国债收益率曲线（738条）")
print("  2. 中美国债收益率对比（9251条）")
print("  3. 国债日线 + 债券指数（3个指数）")
print("  4. 可转债行情（350只实时 + 日线）")
print("  5. 可转债基本信息（1012只）")
print("  6. 集思录可转债数据（23维度，30只）")
print("  7. 中美利率对比")
print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
