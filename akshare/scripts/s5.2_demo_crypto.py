#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AkShare 加密货币数据接口演示脚本
展示如何使用AkShare获取和分析加密货币数据
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime

# 设置中文字体支持
def setup_chinese_font():
    """设置matplotlib中文字体"""
    try:
        # 使用系统中的Noto Sans CJK字体文件
        font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
        chinese_font = fm.FontProperties(fname=font_path, size=12)
        return chinese_font
    except Exception as e:
        print(f"中文字体设置失败: {e}")
        return None

# 设置中文字体
chinese_font = setup_chinese_font()

def get_crypto_spot_data():
    """获取虚拟货币实时行情数据"""
    print("正在获取虚拟货币实时行情数据...")
    df = ak.crypto_js_spot()
    print(f"数据获取成功，共 {len(df)} 条记录")
    return df

def get_bitcoin_holdings_data():
    """获取比特币持仓报告数据"""
    print("\n正在获取比特币持仓报告数据...")
    df = ak.crypto_bitcoin_hold_report()
    print(f"数据获取成功，共 {len(df)} 条记录")
    return df

def analyze_crypto_spot(df):
    """分析虚拟货币实时行情数据"""
    if df is None or len(df) == 0:
        print("\n没有可用的实时行情数据")
        return

    print("\n" + "="*60)
    print("虚拟货币实时行情数据分析")
    print("="*60)

    # 按涨跌幅排序
    if '涨跌幅' in df.columns:
        print("\n涨幅最大的5个币种:")
        top_gainers = df.nlargest(5, '涨跌幅')
        for idx, row in top_gainers.iterrows():
            print(f"  {row['交易品种']}: {row['最近报价']:,.2f} ({row['涨跌幅']:+.2f}%)")

        print("\n跌幅最大的5个币种:")
        top_losers = df.nsmallest(5, '涨跌幅')
        for idx, row in top_losers.iterrows():
            print(f"  {row['交易品种']}: {row['最近报价']:,.2f} ({row['涨跌幅']:+.2f}%)")

    # 统计交易所分布
    if '市场' in df.columns:
        print("\n各交易所数据数量:")
        exchange_counts = df['市场'].value_counts()
        for market, count in exchange_counts.items():
            print(f"  {market}: {count}个")

    # 统计货币对分布
    if '交易品种' in df.columns:
        print("\n主要货币对:")
        df['基础货币'] = df['交易品种'].str.extract(r'([A-Z]+)')[0]
        base_currency_counts = df['基础货币'].value_counts().head(10)
        for currency, count in base_currency_counts.items():
            print(f"  {currency}: {count}个")

def analyze_bitcoin_holdings(df):
    """分析比特币持仓数据"""
    if df is None or len(df) == 0:
        print("\n没有可用的持仓数据")
        return

    print("\n" + "="*60)
    print("比特币持仓数据分析")
    print("="*60)

    # 按持仓数量排序
    if '持仓量' in df.columns:
        print("\n持仓量TOP 10:")
        top_holders = df.nlargest(10, '持仓量')
        for idx, row in top_holders.iterrows():
            print(f"  {row['公司名称-中文']}: {row['持仓量']:,.0f} BTC ({row['持仓占比']:.3f}%)")

    # 按公司性质统计
    if '分类' in df.columns:
        print("\n按公司性质统计:")
        category_counts = df['分类'].value_counts()
        for category, count in category_counts.items():
            print(f"  {category}: {count}个")

    # 计算总持仓
    if '持仓量' in df.columns:
        total_holdings = df['持仓量'].sum()
        print(f"\n总持仓数量: {total_holdings:,.2f} BTC")

        # 机构持仓分析
        institutional = df[df['分类'].isin(['上市公司', 'ETF', '政府机构'])]
        inst_holdings = institutional['持仓量'].sum()
        inst_ratio = inst_holdings / total_holdings * 100
        print(f"机构持仓比例: {inst_ratio:.2f}%")

        # 大额持仓分析（>10000 BTC）
        large_holders = df[df['持仓量'] > 10000]
        print(f"大额持仓者(>10K BTC): {len(large_holders)}个")

def plot_crypto_spot(df):
    """绘制虚拟货币实时行情图表"""
    if df is None or len(df) == 0:
        print("\n没有可用的实时行情数据用于绘图")
        return

    print("\n绘制虚拟货币实时行情图表...")

    # 创建图表
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # 第一个图：价格和涨跌幅
    ax1 = axes[0]
    x_pos = range(len(df))

    bars = ax1.bar(x_pos, df['最近报价'], color='skyblue', alpha=0.7)

    # 标注涨跌幅
    for i, (bar, change) in enumerate(zip(bars, df['涨跌幅'])):
        color = 'red' if change > 0 else 'green'
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{change:+.1f}%', ha='center', va='bottom',
                fontsize=8, color=color, fontproperties=chinese_font)

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(df['交易品种'], rotation=45, ha='right', fontproperties=chinese_font)
    ax1.set_ylabel('价格 (USD)', fontproperties=chinese_font)
    ax1.set_title('虚拟货币实时价格', fontproperties=chinese_font, fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # 第二个图：成交量
    ax2 = axes[1]
    if '24小时成交量' in df.columns:
        volume_bars = ax2.bar(x_pos, df['24小时成交量'], color='lightcoral', alpha=0.7)
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(df['交易品种'], rotation=45, ha='right', fontproperties=chinese_font)
        ax2.set_ylabel('24小时成交量', fontproperties=chinese_font)
        ax2.set_title('虚拟货币成交量对比', fontproperties=chinese_font, fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # 保存图表
    output_path = f'/home/neyo/workspace/code/study/akshare/output/加密货币实时行情分析_{datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"图表已保存: {output_path}")

    plt.close()

def plot_bitcoin_holdings(df):
    """绘制比特币持仓分布图表"""
    if df is None or len(df) == 0:
        print("\n没有可用的持仓数据用于绘图")
        return

    print("\n绘制比特币持仓分布图表...")

    # 创建图表
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # 第一个图：TOP 10 持仓者
    ax1 = axes[0]
    top_10 = df.nlargest(10, '持仓量')
    y_pos = range(len(top_10))

    bars = ax1.barh(y_pos, top_10['持仓量'], color='lightblue', alpha=0.7)

    # 添加数值标签
    for i, (bar, value) in enumerate(zip(bars, top_10['持仓量'])):
        ax1.text(value, i, f' {value:,.0f}', va='center',
                fontproperties=chinese_font, fontsize=9)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(top_10['公司名称-中文'], fontproperties=chinese_font)
    ax1.set_xlabel('持仓量 (BTC)', fontproperties=chinese_font)
    ax1.set_title('比特币持仓量TOP 10', fontproperties=chinese_font, fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # 第二个图：持仓类型分布
    ax2 = axes[1]
    category_counts = df['分类'].value_counts()
    categories = category_counts.index.tolist()
    counts = category_counts.values.tolist()

    colors = ['skyblue', 'lightcoral', 'lightgreen', 'lightyellow', 'plum', 'orange', 'pink', 'gray', 'brown', 'olive']
    colors = colors[:len(categories)]

    bars = ax2.bar(categories, counts, color=colors, alpha=0.7)

    # 添加数值标签
    for bar, count in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f'{count}', ha='center', va='bottom',
                fontproperties=chinese_font)

    ax2.set_ylabel('数量', fontproperties=chinese_font)
    ax2.set_title('持仓者类型分布', fontproperties=chinese_font, fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45, labelsize=10)

    plt.tight_layout()

    # 保存图表
    output_path = f'/home/neyo/workspace/code/study/akshare/output/比特币持仓分布分析_{datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"图表已保存: {output_path}")

    plt.close()

def export_data(df, filename_prefix, description):
    """导出数据到CSV文件"""
    if df is None or len(df) == 0:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f'/home/neyo/workspace/code/study/akshare/output/{filename_prefix}_{timestamp}.csv'

    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"{description}已保存: {output_path}")

    return output_path

def main():
    """主函数"""
    print("\n" + "="*60)
    print("AkShare 加密货币数据接口演示")
    print("="*60)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 获取数据
    spot_df = get_crypto_spot_data()
    holdings_df = get_bitcoin_holdings_data()

    # 2. 数据分析
    analyze_crypto_spot(spot_df)
    analyze_bitcoin_holdings(holdings_df)

    # 3. 绘制图表
    plot_crypto_spot(spot_df)
    plot_bitcoin_holdings(holdings_df)

    # 4. 导出数据
    if spot_df is not None:
        export_data(spot_df, "加密货币实时行情", "实时行情数据")

    if holdings_df is not None:
        export_data(holdings_df, "比特币持仓报告", "持仓报告数据")

    print("\n" + "="*60)
    print("加密货币数据接口演示完成!")
    print("="*60)

if __name__ == "__main__":
    import os
    # 创建output目录
    os.makedirs("output", exist_ok=True)
    main()