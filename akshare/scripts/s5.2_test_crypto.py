#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 虚拟货币数据接口测试
测试日期: 2026-04-27
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def test_crypto_spot():
    """测试虚拟货币实时行情数据"""
    print("=" * 80)
    print("测试1: 虚拟货币实时行情 (crypto_js_spot)")
    print("=" * 80)
    try:
        crypto_js_spot_df = ak.crypto_js_spot()
        print("\n数据获取成功！")
        print(f"数据行数: {len(crypto_js_spot_df)}")
        print(f"数据列数: {len(crypto_js_spot_df.columns)}")
        print(f"\n数据列: {list(crypto_js_spot_df.columns)}")
        print("\n前10条数据:")
        print(crypto_js_spot_df.head(10))
        print("\n数据类型:")
        print(crypto_js_spot_df.dtypes)
        return crypto_js_spot_df
    except Exception as e:
        print(f"错误: {e}")
        return None

def test_bitcoin_hold_report():
    """测试比特币持仓报告"""
    print("\n" + "=" * 80)
    print("测试2: 比特币持仓报告 (crypto_bitcoin_hold_report)")
    print("=" * 80)
    try:
        crypto_bitcoin_hold_report_df = ak.crypto_bitcoin_hold_report()
        print("\n数据获取成功！")
        print(f"数据行数: {len(crypto_bitcoin_hold_report_df)}")
        print(f"数据列数: {len(crypto_bitcoin_hold_report_df.columns)}")
        print(f"\n数据列: {list(crypto_bitcoin_hold_report_df.columns)}")
        print("\n前10条数据:")
        print(crypto_bitcoin_hold_report_df.head(10))
        print("\n数据类型:")
        print(crypto_bitcoin_hold_report_df.dtypes)
        return crypto_bitcoin_hold_report_df
    except Exception as e:
        print(f"错误: {e}")
        return None

def test_bitcoin_cme():
    """测试CME交易所数据"""
    print("\n" + "=" * 80)
    print("测试3: CME交易所比特币数据 (crypto_bitcoin_cme)")
    print("=" * 80)
    try:
        # 获取最近的工作日数据
        today = datetime.now()
        # 往前找到最近的一个工作日
        date = today
        while date.weekday() >= 5:  # 周六=5, 周日=6
            date -= timedelta(days=1)
        date_str = date.strftime("%Y%m%d")
        print(f"查询日期: {date_str}")
        
        crypto_bitcoin_cme_df = ak.crypto_bitcoin_cme(date=date_str)
        print("\n数据获取成功！")
        print(f"数据行数: {len(crypto_bitcoin_cme_df)}")
        print(f"数据列数: {len(crypto_bitcoin_cme_df.columns)}")
        print(f"\n数据列: {list(crypto_bitcoin_cme_df.columns)}")
        print("\n数据内容:")
        print(crypto_bitcoin_cme_df)
        print("\n数据类型:")
        print(crypto_bitcoin_cme_df.dtypes)
        return crypto_bitcoin_cme_df
    except Exception as e:
        print(f"错误: {e}")
        # 尝试使用固定日期
        print("\n尝试使用固定日期 20230830...")
        try:
            crypto_bitcoin_cme_df = ak.crypto_bitcoin_cme(date="20230830")
            print("\n数据获取成功！")
            print(crypto_bitcoin_cme_df)
            return crypto_bitcoin_cme_df
        except Exception as e2:
            print(f"固定日期也失败: {e2}")
            return None

def analyze_crypto_spot(df):
    """分析虚拟货币实时行情数据"""
    if df is None:
        return
    
    print("\n" + "=" * 80)
    print("数据分析: 虚拟货币实时行情")
    print("=" * 80)
    
    # 按涨跌幅排序
    if '涨跌幅' in df.columns:
        print("\n涨幅最大的5个币种:")
        top_gainers = df.nlargest(5, '涨跌幅')
        print(top_gainers[['交易品种', '最近报价', '涨跌幅', '24小时最高', '24小时最低', '24小时成交量']])
        
        print("\n跌幅最大的5个币种:")
        top_losers = df.nsmallest(5, '涨跌幅')
        print(top_losers[['交易品种', '最近报价', '涨跌幅', '24小时最高', '24小时最低', '24小时成交量']])
    
    # 统计交易所分布
    if '市场' in df.columns:
        print("\n各交易所数据数量:")
        exchange_counts = df['市场'].value_counts()
        print(exchange_counts)
    
    # 统计货币对分布
    if '交易品种' in df.columns:
        print("\n主要货币对:")
        # 提取基础货币
        df['基础货币'] = df['交易品种'].str.extract(r'([A-Z]+)')[0]
        base_currency_counts = df['基础货币'].value_counts().head(10)
        print(base_currency_counts)

def analyze_bitcoin_holdings(df):
    """分析比特币持仓数据"""
    if df is None:
        return
    
    print("\n" + "=" * 80)
    print("数据分析: 比特币持仓报告")
    print("=" * 80)
    
    # 按持仓数量排序
    if '持仓量' in df.columns:
        print("\n持有数量最多的10个实体:")
        top_holders = df.nlargest(10, '持仓量')
        print(top_holders[['公司名称-中文', '持仓量', '持仓占比', '分类']])
    
    # 按公司性质统计
    if '分类' in df.columns:
        print("\n按公司性质统计:")
        category_counts = df['分类'].value_counts()
        print(category_counts)
    
    # 计算总持仓
    if '持仓量' in df.columns:
        total_holdings = df['持仓量'].sum()
        print(f"\n总持仓数量: {total_holdings:.2f} BTC")

def main():
    """主函数"""
    print("\nAkShare 虚拟货币数据接口测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 测试1: 实时行情
    spot_df = test_crypto_spot()
    
    # 测试2: 比特币持仓报告
    holdings_df = test_bitcoin_hold_report()
    
    # 测试3: CME数据
    cme_df = test_bitcoin_cme()
    
    # 数据分析
    analyze_crypto_spot(spot_df)
    analyze_bitcoin_holdings(holdings_df)
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)
    
    # 保存数据
    if spot_df is not None:
        spot_file = f"output/crypto_spot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        spot_df.to_csv(spot_file, index=False, encoding='utf-8-sig')
        print(f"\n实时行情数据已保存到: {spot_file}")
    
    if holdings_df is not None:
        holdings_file = f"output/crypto_holdings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        holdings_df.to_csv(holdings_file, index=False, encoding='utf-8-sig')
        print(f"持仓报告数据已保存到: {holdings_file}")
    
    if cme_df is not None:
        cme_file = f"output/crypto_cme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        cme_df.to_csv(cme_file, index=False, encoding='utf-8-sig')
        print(f"CME数据已保存到: {cme_file}")

if __name__ == "__main__":
    import os
    # 创建output目录
    os.makedirs("output", exist_ok=True)
    main()