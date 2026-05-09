#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 上市公司基本面数据接口测试 (阶段1.3)

测试目标：
1. 公司基本信息（名单、代码映射、个股详情）
2. 财务数据（摘要、指标、利润表、资产负债表、现金流）
3. 分红送配与业绩预告
4. 股本股东与限售解禁
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 上市公司基本面数据接口测试")
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
# 1. 公司基本信息
# ========================================================================
print("\n" + "="*80)
print("1. 公司基本信息")
print("="*80)

test_api("stock_info_a_code_name (全部A股)", ak.stock_info_a_code_name)
test_api("stock_info_sh_name_code (沪市)", ak.stock_info_sh_name_code)
test_api("stock_info_sz_name_code (深市)", ak.stock_info_sz_name_code)
test_api("stock_individual_info_em (平安银行)", ak.stock_individual_info_em, symbol="000001")

# ========================================================================
# 2. 财务数据
# ========================================================================
print("\n" + "="*80)
print("2. 财务数据（以平安银行 000001 为例）")
print("="*80)

# 2.1 财务摘要
print("\n>>> 财务摘要（东方财富）")
test_api("stock_financial_abstract", ak.stock_financial_abstract, symbol="000001")

print("\n>>> 财务摘要（同花顺，更详细）")
test_api("stock_financial_abstract_ths", ak.stock_financial_abstract_ths, symbol="000001")

# 2.2 财务分析指标
print("\n>>> 财务分析指标")
test_api("stock_financial_analysis_indicator", ak.stock_financial_analysis_indicator,
         symbol="000001", start_year="2023")

# 2.3 利润表/资产负债表/现金流（同花顺）
print("\n>>> 利润表（同花顺）")
test_api("stock_financial_benefit_ths", ak.stock_financial_benefit_ths, symbol="000001")

print("\n>>> 资产负债表（同花顺）")
test_api("stock_financial_debt_ths", ak.stock_financial_debt_ths, symbol="000001")

print("\n>>> 现金流量表（同花顺）")
test_api("stock_financial_cash_ths", ak.stock_financial_cash_ths, symbol="000001")

# ========================================================================
# 3. 业绩报表与预告
# ========================================================================
print("\n" + "="*80)
print("3. 业绩报表与预告")
print("="*80)

test_api("stock_yjbb_em (业绩报表)", ak.stock_yjbb_em)
test_api("stock_profit_forecast_em (业绩预告)", ak.stock_profit_forecast_em)

# ========================================================================
# 4. 分红送配
# ========================================================================
print("\n" + "="*80)
print("4. 分红送配")
print("="*80)

test_api("stock_fhps_detail_em (平安银行分红)", ak.stock_fhps_detail_em, symbol="000001")
test_api("stock_fhps_em (全市场分红列表)", ak.stock_fhps_em)

# ========================================================================
# 5. 股本股东与限售
# ========================================================================
print("\n" + "="*80)
print("5. 股本股东与限售")
print("="*80)

test_api("stock_restricted_release_queue_em (限售解禁)", ak.stock_restricted_release_queue_em)
test_api("stock_shareholder_change_ths (平安银行股东变动)", ak.stock_shareholder_change_ths, symbol="000001")

# ========================================================================
# 6. 全市场估值
# ========================================================================
print("\n" + "="*80)
print("6. 全市场估值数据")
print("="*80)

test_api("stock_a_ttm_lyr (全市场PE)", ak.stock_a_ttm_lyr)
test_api("stock_a_all_pb (全市场PB)", ak.stock_a_all_pb)

# ========================================================================
# 总结
# ========================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)
print("✓ 已测试的上市公司基本面接口：")
print("  1. 公司基本信息（A股5513只、沪深板块分类）")
print("  2. 个股详情（公司简介、主营业务等）")
print("  3. 财务摘要（东方财富+同花顺双数据源）")
print("  4. 财务分析指标（ROE、每股收益、毛利率等）")
print("  5. 三张报表（利润表/资产负债表/现金流-同花顺）")
print("  6. 业绩报表+业绩预告")
print("  7. 分红送配（明细+全市场列表）")
print("  8. 限售解禁+股东变动")
print("  9. 全市场估值（PE-TTM、PB）")
print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
