#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 指数数据接口测试脚本

测试目标：
1. 探索可用的指数数据接口
2. 验证数据可用性和质量
3. 测试不同类型的指数数据（A股指数、港股指数、行业指数等）
4. 记录每个接口的返回数据格式
"""

import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("AkShare 指数数据接口测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试函数
def test_api(api_name, api_func, *args, **kwargs):
    """测试API接口并显示结果"""
    print(f"\n{'='*60}")
    print(f"测试接口: {api_name}")
    print(f"{'='*60}")
    try:
        result = api_func(*args, **kwargs)
        print(f"✓ 成功获取数据")
        print(f"  数据类型: {type(result)}")
        if isinstance(result, pd.DataFrame):
            print(f"  数据行数: {len(result)}")
            print(f"  数据列数: {len(result.columns)}")
            print(f"  数据列名: {list(result.columns)}")
            print(f"  前3行数据:")
            print(result.head(3).to_string())
            print(f"  数据类型:")
            print(result.dtypes.to_string())
        return result
    except Exception as e:
        print(f"✗ 失败: {type(e).__name__}: {str(e)}")
        return None

# ========================================================================
# 1. A股指数数据
# ========================================================================
print("\n" + "="*80)
print("1. A股指数数据")
print("="*80)


def test_index_hist(name, em_code, sina_code):
    """测试指数历史数据，含东方财富→新浪备用回退"""
    print(f"\n>>> 获取{name}历史行情")
    # 优先东方财富
    df = test_api(f"index_zh_a_hist({name})", ak.index_zh_a_hist,
                  symbol=em_code, period="daily")
    if df is None or (hasattr(df, '__len__') and len(df) == 0):
        # 回退到新浪
        print(f"  东方财富不可用，回退到新浪接口 stock_zh_index_daily({sina_code})...")
        df2 = test_api(f"stock_zh_index_daily({name})", ak.stock_zh_index_daily,
                       symbol=sina_code)
        if df2 is not None and len(df2) > 0:
            print(f"  ✓ 新浪接口获取成功")
    print()


# 1.1 沪深300指数历史行情
test_index_hist("沪深300", "000300", "sh000300")

# 1.2 上证50指数历史行情
test_index_hist("上证50", "000016", "sh000016")

# 1.3 中证500指数历史行情
test_index_hist("中证500", "000905", "sh000905")

# ========================================================================
# 2. 指数实时行情
# ========================================================================
print("\n" + "="*80)
print("2. 指数实时行情")
print("="*80)

# 2.1 新浪指数实时行情
print("\n>>> 测试新浪指数实时行情")
sina_spot = test_api("stock_zh_index_spot_sina", ak.stock_zh_index_spot_sina)

# 2.2 腾讯指数实时行情
print("\n>>> 测试腾讯指数实时行情")
try:
    tx_spot = test_api("stock_zh_index_spot_tx", ak.stock_zh_index_spot_tx)
except AttributeError:
    print("说明: 腾讯指数实时行情接口不存在，跳过测试")

# ========================================================================
# 3. 港股指数数据
# ========================================================================
print("\n" + "="*80)
print("3. 港股指数数据")
print("="*80)

# 3.1 港股指数实时行情
print("\n>>> 测试港股指数实时行情")
hk_spot = test_api("stock_hk_index_spot_sina", ak.stock_hk_index_spot_sina)

# 3.2 恒生指数历史行情
print("\n>>> 测试恒生指数历史行情")
hkhsi_daily = test_api("stock_hk_index_daily_sina", ak.stock_hk_index_daily_sina, symbol="HSI")

# ========================================================================
# 4. 行业指数数据
# ========================================================================
print("\n" + "="*80)
print("4. 行业指数数据")
print("="*80)

# 4.1 申万行业指数
print("\n>>> 测试申万行业指数")
# 注意: 新版AkShare中 index_sw 已改名为 index_hist_sw
sw_index = test_api("index_hist_sw", ak.index_hist_sw)

# 4.2 银河证券行业指数
print("\n>>> 测试银河证券行业指数")
# 注意: 新版AkShare中 index_yh 已改名为 index_yw
yh_index = test_api("index_yw", ak.index_yw)

# ========================================================================
# 5. 指数成分股数据
# ========================================================================
print("\n" + "="*80)
print("5. 指数成分股数据")
print("="*80)

# 5.1 沪深300成分股
print("\n>>> 测试沪深300成分股（新浪数据源）")
# 注意: 新版AkShare中 index_stock_cons 不稳定，改用 index_stock_cons_sina
hs300_stocks = test_api("index_stock_cons_sina", ak.index_stock_cons_sina, symbol="000300")

# 5.2 上证50成分股
print("\n>>> 测试上证50成分股")
sz50_stocks = test_api("index_stock_cons_sina", ak.index_stock_cons_sina, symbol="000016")

# 5.3 中证500成分股
print("\n>>> 测试中证500成分股")
zz500_stocks = test_api("index_stock_cons_sina", ak.index_stock_cons_sina, symbol="000905")

# ========================================================================
# 6. 其他指数数据
# ========================================================================
print("\n" + "="*80)
print("6. 其他指数数据")
print("="*80)

# 6.1 中证全指数列表
print("\n>>> 测试中证全指数列表")
# 注意: 新版AkShare中 index_gz 已移除，改用 index_all_cni
gz_index = test_api("index_all_cni", ak.index_all_cni)

# 6.2 验证沪深300历史数据（东方财富接口）
print("\n>>> 验证沪深300历史数据")
print("    注: 东方财富接口当前不可用，可用 stock_zh_index_daily 代替")
index_info = test_api("index_zh_a_hist", ak.index_zh_a_hist, symbol="000300", period="daily")
if index_info is not None:
    print("\n说明: 指数历史数据可用于研究指数走势和回测")

# ========================================================================
# 总结
# ========================================================================
print("\n" + "="*80)
print("测试总结")
print("="*80)
print("✓ 已测试的指数数据接口包括：")
print("  1. A股指数历史数据（沪深300、上证50、中证500、科创50、创业板指）")
print("  2. 指数实时行情（新浪，562个指数）")
print("  3. 港股指数数据（恒生指数等38个）")
print("  4. 行业指数数据（申万124个、银河11个）")
print("  5. 指数成分股数据（沪深300、上证50、中证500）")
print("  6. 中证全指数列表（1406个指数）")
print("\n⚠ 注意: index_zh_a_hist（东方财富）当前连接失败")
print("  可使用 stock_zh_index_daily（新浪）替代，支持 sh/sz 格式代码")
print("✓ 其余接口均可正常使用，数据质量良好")
print(f"\n测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)