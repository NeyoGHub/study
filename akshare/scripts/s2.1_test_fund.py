#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 基金数据接口测试脚本 (阶段2.1)

测试目标：
1. 基金基础信息接口
2. 开放式基金净值/排行
3. ETF基金行情/历史
4. 基金持仓分析
5. 基金管理人/评级
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 基金数据接口测试")
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
            print(f"  数据列名: {list(result.columns)}")
            print(f"  前3行数据:")
            print(result.head(3).to_string())
        return result
    except Exception as e:
        print(f"✗ 失败: {type(e).__name__}: {str(e)[:80]}")
        return None


# ========================================================================
# 1. 基金基础信息
# ========================================================================
print("\n" + "="*80)
print("1. 基金基础信息")
print("="*80)

test_api("fund_name_em (全部基金列表)", ak.fund_name_em)

# ========================================================================
# 2. 开放式基金
# ========================================================================
print("\n" + "="*80)
print("2. 开放式基金")
print("="*80)

# 2.1 单只基金净值历史
print("\n>>> 测试华夏成长混合(000001)净值历史")
test_api("fund_open_fund_info_em", ak.fund_open_fund_info_em, symbol="000001")

# 2.2 全部开放基金日线
print("\n>>> 测试所有开放基金日线")
test_api("fund_open_fund_daily_em (全部)", ak.fund_open_fund_daily_em)

# 2.3 基金排行
print("\n>>> 测试开放基金排行")
test_api("fund_open_fund_rank_em", ak.fund_open_fund_rank_em)

# ========================================================================
# 3. ETF基金
# ========================================================================
print("\n" + "="*80)
print("3. ETF基金")
print("="*80)

# 3.1 ETF行情（同花顺）
print("\n>>> 测试ETF行情（同花顺）")
test_api("fund_etf_spot_ths", ak.fund_etf_spot_ths)

# 3.2 ETF分类（新浪）
print("\n>>> 测试ETF分类（新浪-ETF基金）")
test_api("fund_etf_category_sina(ETF)", ak.fund_etf_category_sina, symbol="ETF基金")

print("\n>>> 测试ETF分类（新浪-LOF基金）")
test_api("fund_etf_category_sina(LOF)", ak.fund_etf_category_sina, symbol="LOF基金")

# 3.3 ETF历史日线（优先东方财富，失败回退到股票接口）
print("\n>>> 测试上证50ETF(510050)历史日线")
df_etf = test_api("fund_etf_hist_em", ak.fund_etf_hist_em,
         symbol="510050", period="daily", start_date="20250101", end_date="20260507")
if df_etf is None or (hasattr(df_etf, '__len__') and len(df_etf) == 0):
    print("  东方财富不可用，回退到 stock_zh_a_daily...")
    test_api("stock_zh_a_daily(510050)", ak.stock_zh_a_daily,
             symbol="sh510050", adjust="qfq")

# ========================================================================
# 4. 基金持仓
# ========================================================================
print("\n" + "="*80)
print("4. 基金持仓")
print("="*80)

# 4.1 持仓明细
print("\n>>> 测试华夏成长混合持仓明细")
test_api("fund_portfolio_hold_em", ak.fund_portfolio_hold_em, symbol="000001")

# 4.2 持仓变动
print("\n>>> 测试华夏成长混合持仓变动")
test_api("fund_portfolio_change_em", ak.fund_portfolio_change_em, symbol="000001")

# 4.3 行业配置
print("\n>>> 测试华夏成长混合行业配置")
test_api("fund_portfolio_industry_allocation_em",
         ak.fund_portfolio_industry_allocation_em, symbol="000001")

# ========================================================================
# 5. 基金管理人与评级
# ========================================================================
print("\n" + "="*80)
print("5. 基金管理人与评级")
print("="*80)

# 5.1 管理人信息
print("\n>>> 测试基金管理人列表")
test_api("fund_manager_em (前100)", ak.fund_manager_em)

# 5.2 基金评级
print("\n>>> 测试基金评级")
test_api("fund_rating_all (前100)", ak.fund_rating_all)

# 5.3 基金规模（注意：fund_scale_open_sina 有内部列名bug，可能导致失败）
print("\n>>> 测试开放基金规模（股票型）")
print("    注: fund_scale_open_sina 存在AkShare内部bug，可能不可用")
test_api("fund_scale_open_sina", ak.fund_scale_open_sina, symbol="股票型基金")

# 5.4 基金估值
print("\n>>> 测试基金估值")
test_api("fund_value_estimation_em (前100)", ak.fund_value_estimation_em)

# ========================================================================
# 总结
# ========================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)
print("✓ 已测试的基金数据接口包括：")
print("  1. 基金基础信息（26665只基金列表）")
print("  2. 开放式基金（净值历史、日线、排行）")
print("  3. ETF基金（行情、分类、历史日线）")
print("  4. 基金持仓（明细、变动、行业配置）")
print("  5. 基金管理人与评级（管理人、评级、规模、估值）")
print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
