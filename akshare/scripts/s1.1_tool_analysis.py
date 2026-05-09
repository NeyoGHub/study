#!/usr/bin/env python3
"""
综合股票分析工具
集成数据获取、技术指标计算、可视化分析
"""

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans']
plt.rcParams['axes.unicode_minus'] = False

print("="*70)
print("综合股票分析工具")
print("="*70)

# 设置输出目录
DATA_OUTPUT_DIR = "output/data/stock"
PLOT_OUTPUT_DIR = "output/plots/technical"
os.makedirs(DATA_OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOT_OUTPUT_DIR, exist_ok=True)

# 输入股票代码
symbol = input("请输入股票代码（例如：sz002624）: ").strip() or "sz002624"

# 输入日期范围
start_date = input("请输入开始日期（默认20240101）: ").strip() or "20240101"
end_date = input("请输入结束日期（默认20260430）: ").strip() or "20260430"

print(f"\n正在获取 {symbol} 的数据...")

try:
    # 获取历史数据
    hist_data = ak.stock_zh_a_daily(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"
    )

    if len(hist_data) < 20:
        print(f"\n✗ 数据不足（{len(hist_data)} 条），需要至少20条数据")
        exit(1)

    print(f"✓ 成功获取 {len(hist_data)} 条数据")

    # 1. 基本统计
    print("\n" + "="*70)
    print("1. 基本统计")
    print("="*70)

    latest = hist_data.iloc[-1]
    print(f"最新收盘价: {latest['close']:.2f} 元")
    print(f"期间最高价: {hist_data['high'].max():.2f} 元")
    print(f"期间最低价: {hist_data['low'].min():.2f} 元")
    print(f"平均收盘价: {hist_data['close'].mean():.2f} 元")

    # 期间涨跌
    first_close = hist_data['close'].iloc[0]
    last_close = hist_data['close'].iloc[-1]
    total_change = (last_close - first_close) / first_close * 100
    print(f"期间总涨跌: {total_change:.2f}%")

    # 2. 计算技术指标
    print("\n" + "="*70)
    print("2. 技术指标")
    print("="*70)

    # 移动平均线
    hist_data['MA5'] = hist_data['close'].rolling(window=5).mean()
    hist_data['MA10'] = hist_data['close'].rolling(window=10).mean()
    hist_data['MA20'] = hist_data['close'].rolling(window=20).mean()
    hist_data['MA60'] = hist_data['close'].rolling(window=60).mean()

    # RSI
    def calculate_rsi(data, period=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    hist_data['RSI6'] = calculate_rsi(hist_data['close'], period=6)
    hist_data['RSI12'] = calculate_rsi(hist_data['close'], period=12)
    hist_data['RSI24'] = calculate_rsi(hist_data['close'], period=24)

    # MACD
    ema12 = hist_data['close'].ewm(span=12, adjust=False).mean()
    ema26 = hist_data['close'].ewm(span=26, adjust=False).mean()
    hist_data['MACD_DIF'] = ema12 - ema26
    hist_data['MACD_DEA'] = hist_data['MACD_DIF'].ewm(span=9, adjust=False).mean()
    hist_data['MACD_BAR'] = (hist_data['MACD_DIF'] - hist_data['MACD_DEA']) * 2

    # 布林带
    hist_data['BOLL_MID'] = hist_data['close'].rolling(window=20).mean()
    hist_data['BOLL_STD'] = hist_data['close'].rolling(window=20).std()
    hist_data['BOLL_UPPER'] = hist_data['BOLL_MID'] + 2 * hist_data['BOLL_STD']
    hist_data['BOLL_LOWER'] = hist_data['BOLL_MID'] - 2 * hist_data['BOLL_STD']

    # 成交量移动平均
    hist_data['VOL_MA5'] = hist_data['volume'].rolling(window=5).mean()
    hist_data['VOL_MA10'] = hist_data['volume'].rolling(window=10).mean()

    print("✓ 已计算技术指标:")
    print("  - MA5/MA10/MA20/MA60")
    print("  - RSI(6/12/24)")
    print("  - MACD(DIF/DEA/BAR)")
    print("  - BOLL(上轨/中轨/下轨)")
    print("  - VOL_MA5/VOL_MA10")

    # 重新获取最新数据（在技术指标计算之后）
    latest = hist_data.iloc[-1]

    # 3. 技术指标解读
    print("\n" + "="*70)
    print("3. 技术指标解读")
    print("="*70)

    # MA趋势
    if pd.notna(latest['MA5']) and pd.notna(latest['MA10']) and pd.notna(latest['MA20']):
        if latest['close'] > latest['MA5'] > latest['MA10'] > latest['MA20']:
            ma_signal = "🟢 多头排列，短期看涨"
        elif latest['close'] < latest['MA5'] < latest['MA10'] < latest['MA20']:
            ma_signal = "🔴 空头排列，短期看跌"
        else:
            ma_signal = "🟡 盘整状态"
    else:
        ma_signal = "⚪ 数据不足，无法判断"
    print(f"MA趋势: {ma_signal}")

    # RSI判断
    if pd.notna(latest['RSI12']):
        if latest['RSI12'] > 70:
            rsi_signal = "🟠 超买区域，可能回调"
        elif latest['RSI12'] < 30:
            rsi_signal = "🟠 超卖区域，可能反弹"
        else:
            rsi_signal = "✅ 正常范围"
    else:
        rsi_signal = "⚪ 数据不足，无法判断"
    print(f"RSI(12): {rsi_signal}")

    # MACD判断
    if pd.notna(latest['MACD_DIF']) and pd.notna(latest['MACD_DEA']):
        if latest['MACD_DIF'] > latest['MACD_DEA'] and latest['MACD_BAR'] > 0:
            macd_signal = "🟢 金叉，看涨信号"
        elif latest['MACD_DIF'] < latest['MACD_DEA'] and latest['MACD_BAR'] < 0:
            macd_signal = "🔴 死叉，看跌信号"
        else:
            macd_signal = "🟡 无明确信号"
    else:
        macd_signal = "⚪ 数据不足，无法判断"
    print(f"MACD:    {macd_signal}")

    # 布林带判断
    if pd.notna(latest['BOLL_UPPER']) and pd.notna(latest['BOLL_LOWER']):
        if latest['close'] > latest['BOLL_UPPER']:
            boll_signal = "🟠 价格突破上轨，可能超买"
        elif latest['close'] < latest['BOLL_LOWER']:
            boll_signal = "🟠 价格跌破下轨，可能超卖"
        else:
            boll_signal = "✅ 价格在正常区间"
    else:
        boll_signal = "⚪ 数据不足，无法判断"
    print(f"BOLL:    {boll_signal}")

    # 4. 综合评估
    print("\n" + "="*70)
    print("4. 综合评估")
    print("="*70)

    buy_signals = 0
    sell_signals = 0

    # MA信号
    if pd.notna(latest['MA5']) and pd.notna(latest['MA10']):
        if latest['close'] > latest['MA5'] > latest['MA10']:
            buy_signals += 1
        elif latest['close'] < latest['MA5'] < latest['MA10']:
            sell_signals += 1

    # RSI信号
    if pd.notna(latest['RSI12']):
        if latest['RSI12'] < 30:
            buy_signals += 1
        elif latest['RSI12'] > 70:
            sell_signals += 1

    # MACD信号
    if pd.notna(latest['MACD_DIF']) and pd.notna(latest['MACD_DEA']) and pd.notna(latest['MACD_BAR']):
        if latest['MACD_DIF'] > latest['MACD_DEA'] and latest['MACD_BAR'] > 0:
            buy_signals += 1
        elif latest['MACD_DIF'] < latest['MACD_DEA'] and latest['MACD_BAR'] < 0:
            sell_signals += 1

    # BOLL信号
    if pd.notna(latest['BOLL_UPPER']) and pd.notna(latest['BOLL_LOWER']):
        if latest['close'] < latest['BOLL_LOWER']:
            buy_signals += 1
        elif latest['close'] > latest['BOLL_UPPER']:
            sell_signals += 1

    total_signals = buy_signals + sell_signals

    if total_signals == 0:
        overall = "⚪ 数据不足，无法评估"
    elif buy_signals >= 3:
        overall = "🟢 强烈买入信号"
    elif buy_signals >= 2:
        overall = "🟡 谨慎买入"
    elif sell_signals >= 3:
        overall = "🔴 强烈卖出信号"
    elif sell_signals >= 2:
        overall = "🟡 谨慎卖出"
    else:
        overall = "⚪ 持有观望"

    print(f"买入信号: {buy_signals} 个")
    print(f"卖出信号: {sell_signals} 个")
    print(f"\n综合建议: {overall}")

    # 5. 可视化
    print("\n" + "="*70)
    print("5. 生成可视化图表")
    print("="*70)

    # 创建图表
    fig, axes = plt.subplots(4, 1, figsize=(14, 16))

    # 图1：价格和均线
    axes[0].plot(hist_data['date'], hist_data['close'], label='Close Price', linewidth=2, color='black')
    axes[0].plot(hist_data['date'], hist_data['MA5'], label='MA5', linewidth=1.5, alpha=0.8)
    axes[0].plot(hist_data['date'], hist_data['MA10'], label='MA10', linewidth=1.5, alpha=0.8)
    axes[0].plot(hist_data['date'], hist_data['MA20'], label='MA20', linewidth=1.5, alpha=0.8)
    axes[0].plot(hist_data['date'], hist_data['MA60'], label='MA60', linewidth=1.5, alpha=0.8)
    axes[0].set_title(f'{symbol} - Price & Moving Averages', fontsize=14)
    axes[0].set_ylabel('Price (CNY)', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # 图2：RSI
    axes[1].plot(hist_data['date'], hist_data['RSI6'], label='RSI(6)', linewidth=1.5, alpha=0.8)
    axes[1].plot(hist_data['date'], hist_data['RSI12'], label='RSI(12)', linewidth=2)
    axes[1].plot(hist_data['date'], hist_data['RSI24'], label='RSI(24)', linewidth=1.5, alpha=0.8)
    axes[1].axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Overbought (70)')
    axes[1].axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Oversold (30)')
    axes[1].set_title('RSI Indicators', fontsize=14)
    axes[1].set_ylabel('RSI', fontsize=12)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    # 图3：MACD
    axes[2].plot(hist_data['date'], hist_data['MACD_DIF'], label='DIF', linewidth=2)
    axes[2].plot(hist_data['date'], hist_data['MACD_DEA'], label='DEA', linewidth=2)
    axes[2].bar(hist_data['date'], hist_data['MACD_BAR'], label='BAR', alpha=0.3)
    axes[2].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[2].set_title('MACD', fontsize=14)
    axes[2].set_ylabel('MACD', fontsize=12)
    axes[2].legend(fontsize=10)
    axes[2].grid(True, alpha=0.3)

    # 图4：布林带
    axes[3].plot(hist_data['date'], hist_data['close'], label='Close Price', linewidth=2, color='black')
    axes[3].plot(hist_data['date'], hist_data['BOLL_UPPER'], label='Upper', linewidth=1.5, alpha=0.7)
    axes[3].plot(hist_data['date'], hist_data['BOLL_MID'], label='Middle', linewidth=1.5, alpha=0.7)
    axes[3].plot(hist_data['date'], hist_data['BOLL_LOWER'], label='Lower', linewidth=1.5, alpha=0.7)
    axes[3].fill_between(hist_data['date'], hist_data['BOLL_UPPER'], hist_data['BOLL_LOWER'], alpha=0.1)
    axes[3].set_title('Bollinger Bands', fontsize=14)
    axes[3].set_ylabel('Price (CNY)', fontsize=12)
    axes[3].legend(fontsize=10)
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()

    # 保存图表到outputs目录
    plot_filename = f"{symbol}_analysis_{start_date}_{end_date}.png"
    plot_filepath = os.path.join(PLOT_OUTPUT_DIR, plot_filename)
    plt.savefig(plot_filepath, dpi=300, bbox_inches='tight')
    print(f"✓ 图表已保存到: {plot_filepath}")

    # 保存数据到outputs目录
    data_filename = f"{symbol}_analysis_{start_date}_{end_date}.csv"
    data_filepath = os.path.join(DATA_OUTPUT_DIR, data_filename)
    hist_data.to_csv(data_filepath, index=False, encoding='utf-8')
    print(f"✓ 数据已保存到: {data_filepath}")

    # 显示最新数据
    print("\n" + "="*70)
    print("6. 最新数据")
    print("="*70)
    print(hist_data[['date', 'close', 'MA5', 'MA10', 'MA20', 'RSI12', 'MACD_BAR', 'BOLL_UPPER', 'BOLL_LOWER']].tail(10).to_string(index=False))

    print("\n" + "="*70)
    print("分析完成！")
    print("="*70)
    print(f"\n文件清单:")
    print(f"  - 数据文件: {data_filepath}")
    print(f"  - 图表文件: {plot_filepath}")

except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()