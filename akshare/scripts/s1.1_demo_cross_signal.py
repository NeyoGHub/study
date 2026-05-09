#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AkShare 金叉死叉信号识别演示脚本
展示如何使用AkShare数据识别金叉死叉信号
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime

# 设置中文字体支持
def setup_chinese_font():
    """设置matplotlib中文字体"""
    try:
        # 使用系统中的Noto Sans CJK字体文件
        font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
        font_prop = fm.FontProperties(fname=font_path, size=12)
        return font_prop
    except Exception as e:
        print(f"中文字体设置失败: {e}")
        return None

# 设置中文字体
chinese_font = setup_chinese_font()

def get_stock_data(symbol="sh600000", adjust="qfq"):
    """获取股票历史数据"""
    print(f"正在获取 {symbol} 的历史数据...")
    df = ak.stock_zh_a_daily(symbol=symbol, adjust=adjust)
    print(f"数据获取成功，共 {len(df)} 条记录")
    return df

def calculate_ma(df):
    """计算移动平均线"""
    print("\n计算移动平均线...")
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    print("MA5, MA10, MA20 计算完成")
    return df

def identify_cross_signals(df):
    """识别金叉死叉信号"""
    print("\n识别金叉死叉信号...")

    # 识别MA5和MA10的金叉死叉
    df['MA5_MA10_金叉'] = ((df['MA5'] > df['MA10']) & (df['MA5'].shift(1) < df['MA10'].shift(1)))
    df['MA5_MA10_死叉'] = ((df['MA5'] < df['MA10']) & (df['MA5'].shift(1) > df['MA10'].shift(1)))

    # 识别MA5和MA20的金叉死叉
    df['MA5_MA20_金叉'] = ((df['MA5'] > df['MA20']) & (df['MA5'].shift(1) < df['MA20'].shift(1)))
    df['MA5_MA20_死叉'] = ((df['MA5'] < df['MA20']) & (df['MA5'].shift(1) > df['MA20'].shift(1)))

    print("信号识别完成")
    return df

def analyze_signals(df, days=252):
    """分析信号"""
    recent_data = df.tail(days)

    print("\n" + "="*50)
    print("金叉死叉信号分析报告")
    print("="*50)

    # 统计信号数量
    ma5_10_golden_count = recent_data['MA5_MA10_金叉'].sum()
    ma5_10_death_count = recent_data['MA5_MA10_死叉'].sum()
    ma5_20_golden_count = recent_data['MA5_MA20_金叉'].sum()
    ma5_20_death_count = recent_data['MA5_MA20_死叉'].sum()

    print(f"\n【MA5与MA10交叉信号】(近{days}天)")
    print(f"  金叉次数: {ma5_10_golden_count}")
    print(f"  死叉次数: {ma5_10_death_count}")

    if ma5_10_golden_count > 0:
        print("\n  最近的MA5-MA10金叉:")
        golden_signals = recent_data[recent_data['MA5_MA10_金叉']].tail(3)
        for idx, row in golden_signals.iterrows():
            print(f"    {row['date']}: 收盘价={row['close']:.2f}, MA5={row['MA5']:.2f}, MA10={row['MA10']:.2f}")

    if ma5_10_death_count > 0:
        print("\n  最近的MA5-MA10死叉:")
        death_signals = recent_data[recent_data['MA5_MA10_死叉']].tail(3)
        for idx, row in death_signals.iterrows():
            print(f"    {row['date']}: 收盘价={row['close']:.2f}, MA5={row['MA5']:.2f}, MA10={row['MA10']:.2f}")

    print(f"\n【MA5与MA20交叉信号】(近{days}天)")
    print(f"  金叉次数: {ma5_20_golden_count}")
    print(f"  死叉次数: {ma5_20_death_count}")

    if ma5_20_golden_count > 0:
        print("\n  最近的MA5-MA20金叉:")
        golden_signals = recent_data[recent_data['MA5_MA20_金叉']].tail(3)
        for idx, row in golden_signals.iterrows():
            print(f"    {row['date']}: 收盘价={row['close']:.2f}, MA5={row['MA5']:.2f}, MA20={row['MA20']:.2f}")

    if ma5_20_death_count > 0:
        print("\n  最近的MA5-MA20死叉:")
        death_signals = recent_data[recent_data['MA5_MA20_死叉']].tail(3)
        for idx, row in death_signals.iterrows():
            print(f"    {row['date']}: 收盘价={row['close']:.2f}, MA5={row['MA5']:.2f}, MA20={row['MA20']:.2f}")

    return recent_data

def simple_ma_strategy(df):
    """简单的金叉死叉交易策略"""
    print("\n执行简单的均线交叉策略...")

    df['position'] = 0  # 持仓状态：1持有，0空仓
    df['signal'] = 0    # 交易信号：1买入，-1卖出

    # 金叉买入
    buy_signals = df['MA5_MA10_金叉']
    df.loc[buy_signals, 'signal'] = 1

    # 死叉卖出
    sell_signals = df['MA5_MA10_死叉']
    df.loc[sell_signals, 'signal'] = -1

    # 更新持仓状态
    for i in range(1, len(df)):
        if df.iloc[i]['signal'] == 1:  # 买入
            df.iloc[i, df.columns.get_loc('position')] = 1
        elif df.iloc[i]['signal'] == -1:  # 卖出
            df.iloc[i, df.columns.get_loc('position')] = 0
        else:  # 保持之前的状态
            df.iloc[i, df.columns.get_loc('position')] = df.iloc[i-1]['position']

    # 计算收益率
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['returns'] * df['position'].shift(1)

    print("策略执行完成")
    return df

def calculate_performance(df):
    """计算策略表现"""
    print("\n" + "="*50)
    print("策略回测结果")
    print("="*50)

    total_return = (1 + df['strategy_returns'].fillna(0)).prod() - 1
    buy_hold_return = (df['close'].iloc[-1] / df['close'].iloc[0]) - 1

    print(f"\n  策略总收益率: {total_return:.2%}")
    print(f"  买入持有收益率: {buy_hold_return:.2%}")
    print(f"  超额收益: {(total_return - buy_hold_return):.2%}")

    # 交易次数统计
    trade_count = df['signal'].abs().sum()
    print(f"\n  交易次数: {trade_count}")

    return {
        'total_return': total_return,
        'buy_hold_return': buy_hold_return,
        'excess_return': total_return - buy_hold_return,
        'trade_count': trade_count
    }

def plot_signals(df, recent_days=60):
    """绘制信号图表"""
    print(f"\n绘制最近{recent_days}天的信号图表...")

    recent_data = df.tail(recent_days).copy()
    recent_data = recent_data.reset_index(drop=True)

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # 第一个图：价格和均线
    ax1 = axes[0]
    ax1.plot(recent_data.index, recent_data['close'], label='收盘价', linewidth=1.5, color='black')
    ax1.plot(recent_data.index, recent_data['MA5'], label='MA5', linewidth=1, alpha=0.7)
    ax1.plot(recent_data.index, recent_data['MA10'], label='MA10', linewidth=1, alpha=0.7)
    ax1.plot(recent_data.index, recent_data['MA20'], label='MA20', linewidth=1, alpha=0.7)

    # 标记金叉
    golden_points = recent_data[recent_data['MA5_MA10_金叉']]
    if len(golden_points) > 0:
        ax1.scatter(golden_points.index, golden_points['MA10'],
                   marker='^', color='red', s=100, label='金叉', zorder=5)

    # 标记死叉
    death_points = recent_data[recent_data['MA5_MA10_死叉']]
    if len(death_points) > 0:
        ax1.scatter(death_points.index, death_points['MA10'],
                   marker='v', color='green', s=100, label='死叉', zorder=5)

    ax1.set_title('股价走势与金叉死叉信号', fontsize=14, fontweight='bold', fontproperties=chinese_font)
    ax1.set_xlabel('交易日', fontsize=12, fontproperties=chinese_font)
    ax1.set_ylabel('价格', fontsize=12, fontproperties=chinese_font)
    ax1.legend(loc='best', prop=chinese_font)
    ax1.grid(True, alpha=0.3)

    # 第二个图：策略收益
    ax2 = axes[1]
    cumulative_returns = (1 + recent_data['strategy_returns'].fillna(0)).cumprod()
    buy_hold_cumulative = recent_data['close'] / recent_data['close'].iloc[0]

    ax2.plot(recent_data.index, cumulative_returns, label='策略收益', linewidth=2, color='blue')
    ax2.plot(recent_data.index, buy_hold_cumulative, label='买入持有', linewidth=2, color='gray', linestyle='--')

    ax2.set_title('策略收益对比', fontsize=14, fontweight='bold', fontproperties=chinese_font)
    ax2.set_xlabel('交易日', fontsize=12, fontproperties=chinese_font)
    ax2.set_ylabel('累计收益', fontsize=12, fontproperties=chinese_font)
    ax2.legend(loc='best', prop=chinese_font)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # 保存图表
    output_path = f'/home/neyo/workspace/code/study/akshare/output/金叉死叉信号分析_{datetime.now().strftime("%Y%m%d")}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"图表已保存: {output_path}")

    plt.close()

def export_signals(df, output_path):
    """导出信号数据到CSV"""
    # 只导出有信号的日期
    signals_df = df[(df['MA5_MA10_金叉']) | (df['MA5_MA10_死叉']) |
                   (df['MA5_MA20_金叉']) | (df['MA5_MA20_死叉'])].copy()

    if len(signals_df) > 0:
        # 选择相关列
        export_columns = ['date', 'close', 'MA5', 'MA10', 'MA20',
                          'MA5_MA10_金叉', 'MA5_MA10_死叉',
                          'MA5_MA20_金叉', 'MA5_MA20_死叉', 'signal', 'position']

        # 确保列存在
        available_columns = [col for col in export_columns if col in signals_df.columns]
        signals_df = signals_df[available_columns]

        signals_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n信号数据已导出: {output_path}")
        print(f"共 {len(signals_df)} 条信号记录")
    else:
        print("\n未发现信号记录")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("AkShare 金叉死叉信号识别演示")
    print("="*60)

    # 1. 获取数据
    df = get_stock_data("sh600000", "qfq")

    # 2. 计算移动平均线
    df = calculate_ma(df)

    # 3. 识别金叉死叉信号
    df = identify_cross_signals(df)

    # 4. 分析信号
    recent_data = analyze_signals(df, days=252)

    # 5. 执行策略
    df = simple_ma_strategy(df)

    # 6. 计算策略表现
    performance = calculate_performance(df)

    # 7. 绘制图表
    plot_signals(df, recent_days=60)

    # 8. 导出信号数据
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f'/home/neyo/workspace/code/study/akshare/output/金叉死叉信号数据_{timestamp}.csv'
    export_signals(df, output_path)

    # 9. 保存完整数据
    data_output_path = f'/home/neyo/workspace/code/study/akshare/output/金叉死叉分析完整数据_{timestamp}.csv'
    df.to_csv(data_output_path, index=False, encoding='utf-8-sig')
    print(f"\n完整分析数据已保存: {data_output_path}")

    print("\n" + "="*60)
    print("金叉死叉信号识别演示完成!")
    print("="*60)

    return performance

if __name__ == "__main__":
    performance = main()