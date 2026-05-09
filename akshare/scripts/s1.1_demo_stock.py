#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 股票数据接口演示脚本（修正版）

本脚本演示AkShare股票数据接口的核心功能，包括：
1. 获取单只股票历史数据
2. 获取全市场实时行情
3. 获取分钟级数据
4. 获取指数实时数据
5. 数据分析和可视化

运行方式：
    python s1.1_demo_stock.py

作者：Adams
日期：2026-04-27
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建输出目录
os.makedirs('output', exist_ok=True)


def demo_1_single_stock():
    """演示1：获取单只股票历史数据"""
    print("\n" + "=" * 80)
    print("演示1：获取单只股票历史数据")
    print("=" * 80)
    
    try:
        # 获取浦发银行历史数据（前复权）
        print("\n正在获取浦发银行（sh600000）的历史数据...")
        df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")
        
        print(f"\n✓ 数据获取成功！")
        print(f"数据量：{len(df)} 条")
        print(f"时间范围：{df['date'].min()} 至 {df['date'].max()}")
        print(f"数据字段：{list(df.columns)}")
        
        # 显示最近5天数据
        print("\n最近5天数据：")
        print(df.tail(5)[['date', 'close', 'volume', 'amount']].to_string())
        
        # 保存数据
        output_file = 'output/浦发银行历史数据.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到：{output_file}")
        
        return df
    except Exception as e:
        print(f"✗ 错误：{e}")
        return None


def demo_2_realtime_market():
    """演示2：获取全市场实时行情"""
    print("\n" + "=" * 80)
    print("演示2：获取全市场实时行情")
    print("=" * 80)
    
    try:
        # 获取全市场实时行情
        print("\n正在获取全市场实时行情...")
        df = ak.stock_zh_a_spot()
        
        print(f"\n✓ 数据获取成功！")
        print(f"股票总数：{len(df)} 只")
        print(f"数据字段：{list(df.columns)}")
        
        # 统计涨跌情况
        up_count = len(df[df['涨跌幅'] > 0])
        down_count = len(df[df['涨跌幅'] < 0])
        flat_count = len(df[df['涨跌幅'] == 0])
        
        print(f"\n市场概况：")
        print(f"  上涨股票：{up_count} 只（{up_count/len(df)*100:.1f}%）")
        print(f"  下跌股票：{down_count} 只（{down_count/len(df)*100:.1f}%）")
        print(f"  平盘股票：{flat_count} 只（{flat_count/len(df)*100:.1f}%）")
        
        # 涨幅榜TOP10
        print("\n涨幅榜TOP10：")
        top_gainers = df.nlargest(10, '涨跌幅')
        print(top_gainers[['代码', '名称', '最新价', '涨跌幅', '成交额']].to_string(index=False))
        
        # 跌幅榜TOP10
        print("\n跌幅榜TOP10：")
        top_losers = df.nsmallest(10, '涨跌幅')
        print(top_losers[['代码', '名称', '最新价', '涨跌幅', '成交额']].to_string(index=False))
        
        # 成交额TOP10
        print("\n成交额TOP10：")
        top_by_amount = df.nlargest(10, '成交额')
        print(top_by_amount[['代码', '名称', '最新价', '涨跌幅', '成交额']].to_string(index=False))
        
        # 保存数据
        output_file = 'output/全市场实时行情.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到：{output_file}")
        
        return df
    except Exception as e:
        print(f"✗ 错误：{e}")
        return None


def demo_3_minute_data():
    """演示3：获取分钟级数据"""
    print("\n" + "=" * 80)
    print("演示3：获取分钟级数据")
    print("=" * 80)
    
    try:
        # 获取5分钟K线
        print("\n正在获取浦发银行（sh600000）的5分钟K线...")
        df = ak.stock_zh_a_minute(symbol="sh600000", period="5", adjust="")
        
        print(f"\n✓ 数据获取成功！")
        print(f"数据量：{len(df)} 条")
        print(f"数据字段：{list(df.columns)}")
        
        # 显示最近10条数据
        print("\n最近10条5分钟数据：")
        print(df.tail(10).to_string())
        
        # 保存数据
        output_file = 'output/浦发银行5分钟数据.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到：{output_file}")
        
        return df
    except Exception as e:
        print(f"✗ 错误：{e}")
        return None


def demo_4_index_data():
    """演示4：获取指数实时数据"""
    print("\n" + "=" * 80)
    print("演示4：获取指数实时数据")
    print("=" * 80)
    
    try:
        # 获取指数实时行情
        print("\n正在获取指数实时行情...")
        df = ak.stock_zh_index_spot_sina()
        
        print(f"\n✓ 数据获取成功！")
        print(f"指数总数：{len(df)} 个")
        print(f"数据字段：{list(df.columns)}")
        
        # 筛选主要指数（使用正确的字段名'名称'）
        if '名称' in df.columns:
            major_indices = df[df['名称'].str.contains('上证|深证|创业板', na=False)]
            print(f"\n主要指数：")
            print(major_indices[['代码', '名称', '最新价', '涨跌幅', '涨跌额']].to_string(index=False))
        else:
            print("\n注意：索引数据字段可能已更新，请查看实际字段名")
            print(df.head())
        
        # 保存数据
        output_file = 'output/指数实时行情.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n数据已保存到：{output_file}")
        
        return df
    except Exception as e:
        print(f"✗ 错误：{e}")
        return None


def demo_5_technical_analysis(df):
    """演示5：技术分析和可视化"""
    if df is None or len(df) == 0:
        print("\n" + "=" * 80)
        print("演示5：技术分析和可视化")
        print("=" * 80)
        print("\n✗ 无数据，跳过技术分析")
        return
    
    print("\n" + "=" * 80)
    print("演示5：技术分析和可视化")
    print("=" * 80)
    
    try:
        # 计算移动平均线（使用正确的字段名'close'）
        df['MA5'] = df['close'].rolling(window=5).mean()
        df['MA10'] = df['close'].rolling(window=10).mean()
        df['MA20'] = df['close'].rolling(window=20).mean()
        
        print("\n计算技术指标：")
        print("✓ MA5（5日移动平均线）")
        print("✓ MA10（10日移动平均线）")
        print("✓ MA20（20日移动平均线）")
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 图1：价格走势和移动平均线
        ax1 = axes[0, 0]
        ax1.plot(range(len(df)), df['close'], label='收盘价', linewidth=1)
        ax1.plot(range(len(df)), df['MA5'], label='MA5', linewidth=1)
        ax1.plot(range(len(df)), df['MA10'], label='MA10', linewidth=1)
        ax1.plot(range(len(df)), df['MA20'], label='MA20', linewidth=1)
        ax1.set_title('价格走势与移动平均线', fontsize=12)
        ax1.set_xlabel('日期')
        ax1.set_ylabel('价格')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 图2：成交量
        ax2 = axes[0, 1]
        ax2.bar(range(len(df)), df['volume'], alpha=0.7)
        ax2.set_title('成交量', fontsize=12)
        ax2.set_xlabel('日期')
        ax2.set_ylabel('成交量')
        ax2.grid(True, alpha=0.3)
        
        # 图3：换手率（如果有）
        ax3 = axes[1, 0]
        if 'turnover' in df.columns:
            colors = ['red' if x > 0 else 'green' for x in df['turnover'].diff()]
            ax3.bar(range(len(df)), df['turnover'], color=colors, alpha=0.7)
            ax3.set_title('换手率', fontsize=12)
            ax3.set_xlabel('日期')
            ax3.set_ylabel('换手率(%)')
        else:
            ax3.text(0.5, 0.5, '数据中无换手率字段', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('换手率（无数据）', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # 图4：成交额
        ax4 = axes[1, 1]
        ax4.plot(range(len(df)), df['amount']/1e8, label='成交额', linewidth=1, color='orange')
        ax4.set_title('成交额', fontsize=12)
        ax4.set_xlabel('日期')
        ax4.set_ylabel('成交额(亿元)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 保存图表
        output_file = 'output/技术分析图表.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n✓ 技术分析图表已保存到：{output_file}")
        plt.close()
        
        print("\n✓ 技术分析完成！")
        
    except Exception as e:
        print(f"\n✗ 技术分析错误：{e}")


def demo_6_data_analysis(realtime_df):
    """演示6：数据分析"""
    if realtime_df is None or len(realtime_df) == 0:
        print("\n" + "=" * 80)
        print("演示6：数据分析")
        print("=" * 80)
        print("\n✗ 无数据，跳过数据分析")
        return
    
    print("\n" + "=" * 80)
    print("演示6：数据分析")
    print("=" * 80)
    
    try:
        # 统计分析
        print("\n统计分析：")
        print(f"平均涨跌幅：{realtime_df['涨跌幅'].mean():.2f}%")
        print(f"涨跌幅中位数：{realtime_df['涨跌幅'].median():.2f}%")
        print(f"涨跌幅标准差：{realtime_df['涨跌幅'].std():.2f}%")
        
        # 价格区间分析
        print(f"\n价格区间分析：")
        print(f"最低价：{realtime_df['最新价'].min():.2f} 元")
        print(f"最高价：{realtime_df['最新价'].max():.2f} 元")
        print(f"平均价：{realtime_df['最新价'].mean():.2f} 元")
        
        # 成交量分析
        print(f"\n成交量分析：")
        print(f"总成交额：{realtime_df['成交额'].sum()/1e8:.2f} 亿元")
        print(f"平均成交额：{realtime_df['成交额'].mean()/1e8:.2f} 亿元")
        
        print("\n✓ 数据分析完成！")
        
    except Exception as e:
        print(f"\n✗ 数据分析错误：{e}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("AkShare 股票数据接口演示（修正版）")
    print("=" * 80)
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 演示1：获取单只股票历史数据
    stock_df = demo_1_single_stock()
    
    # 演示2：获取全市场实时行情
    realtime_df = demo_2_realtime_market()
    
    # 演示3：获取分钟级数据
    demo_3_minute_data()
    
    # 演示4：获取指数实时数据
    demo_4_index_data()
    
    # 演示5：技术分析和可视化
    demo_5_technical_analysis(stock_df)
    
    # 演示6：数据分析
    demo_6_data_analysis(realtime_df)
    
    # 总结
    print("\n" + "=" * 80)
    print("演示完成！")
    print("=" * 80)
    print("\n生成的文件：")
    print("  1. output/浦发银行历史数据.csv")
    print("  2. output/全市场实时行情.csv")
    print("  3. output/浦发银行5分钟数据.csv")
    print("  4. output/指数实时行情.csv")
    print("  5. output/技术分析图表.png")
    print("\n所有文件已保存到 output 目录")
    print("=" * 80)


if __name__ == "__main__":
    main()