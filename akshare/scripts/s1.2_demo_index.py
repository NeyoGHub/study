#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 指数数据综合示例

功能：
1. 获取A股主要指数历史数据和实时行情
2. 计算技术指标（均线、MACD、RSI、布林带）
3. 金叉死叉信号识别
4. 指数走势对比分析
5. 行业指数分析
6. 数据可视化（正确处理中文字体）

运行：./venv/bin/python scripts/index_demo.py
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 中文字体设置（必须使用直接字体文件路径）
# ============================================================
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
if os.path.exists(FONT_PATH):
    chinese_font = fm.FontProperties(fname=FONT_PATH, size=12)
    chinese_font_title = fm.FontProperties(fname=FONT_PATH, size=14)
    chinese_font_small = fm.FontProperties(fname=FONT_PATH, size=10)
else:
    # 回退：查找系统可用中文字体
    font_candidates = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/noto/NotoSansCJK-Regular.ttc',
    ]
    FONT_PATH = None
    for fp in font_candidates:
        if os.path.exists(fp):
            FONT_PATH = fp
            break
    if FONT_PATH:
        chinese_font = fm.FontProperties(fname=FONT_PATH, size=12)
        chinese_font_title = fm.FontProperties(fname=FONT_PATH, size=14)
        chinese_font_small = fm.FontProperties(fname=FONT_PATH, size=10)
    else:
        # 最后回退到 sans-serif
        chinese_font = fm.FontProperties(size=12)
        chinese_font_title = fm.FontProperties(size=14)
        chinese_font_small = fm.FontProperties(size=10)

# ============================================================
# 输出目录
# ============================================================
OUTPUT_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(OUTPUT_DIR, 'data', 'index')
PLOT_DIR = os.path.join(OUTPUT_DIR, 'plots', 'index')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# 时间戳
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')


def print_header(title):
    """打印分隔标题"""
    print()
    print('=' * 70)
    print(f'  {title}')
    print('=' * 70)


def safe_api_call(api_func, *args, **kwargs):
    """安全调用API，带错误处理"""
    try:
        result = api_func(*args, **kwargs)
        return result
    except Exception as e:
        print(f'  ⚠ 调用失败: {type(e).__name__}: {str(e)[:60]}')
        return None


def calc_ma(df, windows=[5, 10, 20, 60]):
    """计算移动平均线"""
    for w in windows:
        col = f'MA{w}'
        close_col = '收盘' if '收盘' in df.columns else 'close'
        df[col] = df[close_col].rolling(window=w).mean()
    return df


def calc_macd(df, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    close_col = '收盘' if '收盘' in df.columns else 'close'
    ema_fast = df[close_col].ewm(span=fast).mean()
    ema_slow = df[close_col].ewm(span=slow).mean()
    df['DIF'] = ema_fast - ema_slow
    df['DEA'] = df['DIF'].ewm(span=signal).mean()
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    return df


def calc_rsi(df, period=14):
    """计算RSI指标"""
    close_col = '收盘' if '收盘' in df.columns else 'close'
    delta = df[close_col].diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def calc_bollinger(df, period=20, std_dev=2):
    """计算布林带"""
    close_col = '收盘' if '收盘' in df.columns else 'close'
    df['BOLL_MID'] = df[close_col].rolling(window=period).mean()
    std = df[close_col].rolling(window=period).std()
    df['BOLL_UP'] = df['BOLL_MID'] + std_dev * std
    df['BOLL_DN'] = df['BOLL_MID'] - std_dev * std
    return df


def find_golden_death_cross(df):
    """识别金叉死叉信号"""
    close_col = '收盘' if '收盘' in df.columns else 'close'
    date_col = '日期' if '日期' in df.columns else 'date'

    # 计算快慢均线
    df['MA_fast'] = df[close_col].rolling(window=5).mean()
    df['MA_slow'] = df[close_col].rolling(window=20).mean()

    signals = []
    for i in range(1, len(df)):
        prev_fast = df['MA_fast'].iloc[i-1]
        prev_slow = df['MA_slow'].iloc[i-1]
        curr_fast = df['MA_fast'].iloc[i]
        curr_slow = df['MA_slow'].iloc[i]

        # 金叉：快线上穿慢线
        if prev_fast <= prev_slow and curr_fast > curr_slow:
            signals.append({
                '日期': df[date_col].iloc[i],
                '类型': '金叉',
                'MA5': round(curr_fast, 2),
                'MA20': round(curr_slow, 2),
                '收盘价': round(df[close_col].iloc[i], 2)
            })
        # 死叉：快线下穿慢线
        elif prev_fast >= prev_slow and curr_fast < curr_slow:
            signals.append({
                '日期': df[date_col].iloc[i],
                '类型': '死叉',
                'MA5': round(curr_fast, 2),
                'MA20': round(curr_slow, 2),
                '收盘价': round(df[close_col].iloc[i], 2)
            })

    return pd.DataFrame(signals)


# ============================================================
# 第一步：获取A股主要指数数据
# ============================================================
print_header('第一步：获取A股主要指数数据')

indices = [
    ('000300', '沪深300指数'),
    ('000016', '上证50指数'),
    ('000905', '中证500指数'),
    ('000688', '科创50指数'),
    ('399006', '创业板指数'),
]

index_data = {}
for symbol, name in indices:
    # 新浪接口需要sh/sz前缀
    sina_symbol = f"sh{symbol}" if symbol.startswith('00') else f"sz{symbol}"

    print(f'\n正在获取 {name} ({symbol})...')

    # 优先尝试东方财富接口（但当前可能不可用）
    df = safe_api_call(
        ak.index_zh_a_hist,
        symbol=symbol,
        period='daily',
        start_date='20250101',
        end_date='20260507'
    )

    # 失败则回退到新浪接口
    if df is None or len(df) == 0:
        print(f'  东方财富不可用，尝试新浪接口...')
        df_sina = safe_api_call(ak.stock_zh_index_daily, symbol=sina_symbol)
        if df_sina is not None and len(df_sina) > 0:
            # 统一列名为中文格式
            df = df_sina.rename(columns={
                'date': '日期', 'open': '开盘', 'close': '收盘',
                'high': '最高', 'low': '最低', 'volume': '成交量'
            })
            # 新浪无成交额/振幅/涨跌幅/换手率，补空列
            for col in ['成交额', '振幅', '涨跌幅', '涨跌额', '换手率']:
                df[col] = 0.0
            df = df[['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']]

    if df is not None and len(df) > 0:
        df['指数代码'] = symbol
        df['指数名称'] = name
        index_data[name] = df
        print(f'  ✓ 获取成功: {len(df)} 条数据 ({df["日期"].iloc[0]} ~ {df["日期"].iloc[-1]})')
    else:
        print(f'  ✗ 获取失败')

print(f'\n成功获取 {len(index_data)}/{len(indices)} 个指数的数据')

# ============================================================
# 第二步：指数实时行情
# ============================================================
print_header('第二步：获取指数实时行情')

spot = safe_api_call(ak.stock_zh_index_spot_sina)
if spot is not None:
    print(f'  ✓ 成功获取 {len(spot)} 个指数实时行情')
    print(f'  列名: {list(spot.columns)}')
    print(f'\n  主要指数行情:')
    key_indices = ['上证指数', '深证成指', '创业板指', '科创50', '沪深300', '上证50', '中证500']
    for _, row in spot.iterrows():
        if row['名称'] in key_indices:
            print(f'    {row["名称"]}: {row["最新价"]} ({row["涨跌幅"]})')
    # 保存到CSV
    csv_path = os.path.join(DATA_DIR, f'指数实时行情_{TIMESTAMP}.csv')
    spot.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')

# ============================================================
# 第三步：技术指标计算（以沪深300为例）
# ============================================================
print_header('第三步：技术指标计算（沪深300指数）')

if '沪深300指数' in index_data:
    hs300 = index_data['沪深300指数'].copy()
    hs300 = hs300.sort_values('日期')

    # 计算各项技术指标
    hs300 = calc_ma(hs300)
    hs300 = calc_macd(hs300)
    hs300 = calc_rsi(hs300)
    hs300 = calc_bollinger(hs300)

    print(f'  均线: MA5/MA10/MA20/MA60')
    print(f'  MACD: DIF={hs300["DIF"].iloc[-1]:.2f}, DEA={hs300["DEA"].iloc[-1]:.2f}')
    print(f'  RSI(14): {hs300["RSI"].iloc[-1]:.2f}')
    print(f'  布林带上轨: {hs300["BOLL_UP"].iloc[-1]:.2f}')
    print(f'  布林带下轨: {hs300["BOLL_DN"].iloc[-1]:.2f}')
    print(f'  当前收盘价: {hs300["收盘"].iloc[-1]:.2f}')

    # 保存技术指标数据
    csv_path = os.path.join(DATA_DIR, f'沪深300技术指标_{TIMESTAMP}.csv')
    hs300.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')

# ============================================================
# 第四步：金叉死叉信号识别
# ============================================================
print_header('第四步：金叉死叉信号识别')

if '沪深300指数' in index_data:
    signals_df = find_golden_death_cross(hs300)
    if len(signals_df) > 0:
        print(f'  识别到 {len(signals_df)} 个信号:')
        print(f'    金叉: {len(signals_df[signals_df["类型"]=="金叉"])} 次')
        print(f'    死叉: {len(signals_df[signals_df["类型"]=="死叉"])} 次')
        print(f'\n  最近5个信号:')
        print(signals_df.tail(5).to_string(index=False))

        # 保存信号数据
        csv_path = os.path.join(DATA_DIR, f'沪深300金叉死叉信号_{TIMESTAMP}.csv')
        signals_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f'\n  ✓ 已保存: {csv_path}')
    else:
        print('  - 未识别到金叉死叉信号')

# ============================================================
# 第五步：指数走势对比分析
# ============================================================
print_header('第五步：指数走势对比分析')

if len(index_data) >= 2:
    print('  计算各指数2025年至今涨跌幅...')
    comparison = []
    for name, df in index_data.items():
        df_sorted = df.sort_values('日期')
        if len(df_sorted) > 0:
            first_close = df_sorted['收盘'].iloc[0]
            last_close = df_sorted['收盘'].iloc[-1]
            pct_change = (last_close - first_close) / first_close * 100
            high = df_sorted['最高'].max()
            low = df_sorted['最低'].min()
            comparison.append({
                '指数名称': name,
                '起始日期': df_sorted['日期'].iloc[0],
                '结束日期': df_sorted['日期'].iloc[-1],
                '起始收盘': round(first_close, 2),
                '最新收盘': round(last_close, 2),
                '涨跌幅%': round(pct_change, 2),
                '最高': round(high, 2),
                '最低': round(low, 2)
            })

    comp_df = pd.DataFrame(comparison)
    print(f'\n{comp_df.to_string(index=False)}')

    csv_path = os.path.join(DATA_DIR, f'指数对比分析_{TIMESTAMP}.csv')
    comp_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')

# ============================================================
# 第六步：数据可视化
# ============================================================
print_header('第六步：数据可视化')

def save_fig(fig, filename):
    """保存图表"""
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓ 已保存: {path}')


# 6.1 沪深300走势图（含均线）
print('\n  6.1 绘制沪深300走势图（含均线）...')
if '沪深300指数' in index_data:
    df = hs300.sort_values('日期').tail(120)  # 最近120个交易日
    dates = pd.to_datetime(df['日期'])

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1, 1]})
    fig.suptitle('沪深300指数技术分析', fontproperties=chinese_font_title, fontsize=16)

    # 上：K线+均线
    ax1 = axes[0]
    ax1.plot(dates, df['收盘'], label='收盘价', color='#333333', linewidth=1.5)
    ax1.plot(dates, df['MA5'], label='MA5', color='#FF6B6B', linestyle='--', linewidth=1)
    ax1.plot(dates, df['MA10'], label='MA10', color='#4ECDC4', linestyle='--', linewidth=1)
    ax1.plot(dates, df['MA20'], label='MA20', color='#45B7D1', linestyle='--', linewidth=1)
    ax1.plot(dates, df['MA60'], label='MA60', color='#96CEB4', linestyle='--', linewidth=1)

    # 布林带
    ax1.fill_between(dates, df['BOLL_UP'], df['BOLL_DN'], alpha=0.15, color='gray', label='布林带')
    ax1.plot(dates, df['BOLL_UP'], color='gray', linewidth=0.5, alpha=0.5)
    ax1.plot(dates, df['BOLL_DN'], color='gray', linewidth=0.5, alpha=0.5)

    ax1.set_ylabel('点位', fontproperties=chinese_font)
    ax1.legend(prop=chinese_font_small, loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    # 中：MACD
    ax2 = axes[1]
    colors_macd = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in df['MACD']]
    ax2.bar(dates, df['MACD'], color=colors_macd, width=1.5, alpha=0.7, label='MACD柱')
    ax2.plot(dates, df['DIF'], label='DIF', color='#333333', linewidth=1)
    ax2.plot(dates, df['DEA'], label='DEA', color='#FF6B6B', linewidth=1)
    ax2.set_ylabel('MACD', fontproperties=chinese_font)
    ax2.legend(prop=chinese_font_small, loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    # 下：RSI
    ax3 = axes[2]
    ax3.plot(dates, df['RSI'], label='RSI(14)', color='#6C5CE7', linewidth=1.5)
    ax3.axhline(y=70, color='#FF6B6B', linestyle='--', alpha=0.5, label='超买(70)')
    ax3.axhline(y=30, color='#4ECDC4', linestyle='--', alpha=0.5, label='超卖(30)')
    ax3.axhline(y=50, color='gray', linestyle=':', alpha=0.3)
    ax3.fill_between(dates, 70, 30, alpha=0.05, color='gray')
    ax3.set_ylabel('RSI', fontproperties=chinese_font)
    ax3.set_xlabel('日期', fontproperties=chinese_font)
    ax3.legend(prop=chinese_font_small, loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 100)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    plt.tight_layout()
    save_fig(fig, f'沪深300技术分析_{TIMESTAMP}.png')


# 6.2 主要指数走势对比（归一化）
print('\n  6.2 绘制主要指数走势对比图...')
if len(index_data) >= 2:
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('A股主要指数走势对比（归一化）', fontproperties=chinese_font_title, fontsize=16)

    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#6C5CE7', '#F9CA24', '#FF9FF3']
    color_idx = 0

    for name, df in index_data.items():
        df_sorted = df.sort_values('日期')
        if len(df_sorted) > 20:
            dates = pd.to_datetime(df_sorted['日期'])
            # 归一化到100
            normalized = df_sorted['收盘'] / df_sorted['收盘'].iloc[0] * 100
            ax.plot(dates, normalized, label=name, color=colors[color_idx % len(colors)], linewidth=1.5)
            color_idx += 1

    ax.set_ylabel('归一化点位（基期=100）', fontproperties=chinese_font)
    ax.set_xlabel('日期', fontproperties=chinese_font)
    ax.legend(prop=chinese_font_small, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.tight_layout()
    save_fig(fig, f'指数走势对比_{TIMESTAMP}.png')


# 6.3 金叉死叉信号标记图
print('\n  6.3 绘制金叉死叉信号图...')
if '沪深300指数' in index_data and len(signals_df) > 0:
    df = hs300.sort_values('日期').tail(250)
    dates = pd.to_datetime(df['日期'])

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('沪深300指数 - 金叉死叉信号', fontproperties=chinese_font_title, fontsize=16)

    ax.plot(dates, df['收盘'], label='收盘价', color='#333333', linewidth=1.5)
    ax.plot(dates, df['MA_fast'], label='MA5', color='#FF6B6B', linestyle='--', linewidth=1)
    ax.plot(dates, df['MA_slow'], label='MA20', color='#45B7D1', linestyle='--', linewidth=1)

    # 标记信号
    signals_in_range = signals_df[
        pd.to_datetime(signals_df['日期']).isin(dates)
    ]
    for _, sig in signals_in_range.iterrows():
        sig_date = pd.to_datetime(sig['日期'])
        sig_type = sig['类型']
        if sig_type == '金叉':
            ax.scatter(sig_date, sig['收盘价'], color='red', s=100, marker='^', zorder=5)
            ax.annotate('金叉', (sig_date, sig['收盘价']),
                       textcoords='offset points', xytext=(0, 15),
                       ha='center', fontproperties=chinese_font_small,
                       color='red', fontweight='bold')
        else:
            ax.scatter(sig_date, sig['收盘价'], color='green', s=100, marker='v', zorder=5)
            ax.annotate('死叉', (sig_date, sig['收盘价']),
                       textcoords='offset points', xytext=(0, -20),
                       ha='center', fontproperties=chinese_font_small,
                       color='green', fontweight='bold')

    ax.set_ylabel('点位', fontproperties=chinese_font)
    ax.set_xlabel('日期', fontproperties=chinese_font)
    ax.legend(prop=chinese_font_small, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.tight_layout()
    save_fig(fig, f'沪深300金叉死叉_{TIMESTAMP}.png')


# 6.4 申万行业指数热力图
print('\n  6.4 获取并绘制申万行业指数...')
realtime_sw = safe_api_call(ak.index_realtime_sw)
if realtime_sw is not None and len(realtime_sw) > 0:
    csv_path = os.path.join(DATA_DIR, f'申万行业行情_{TIMESTAMP}.csv')
    realtime_sw.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')

    # 绘制行业涨跌幅柱状图
    top_industries = realtime_sw.head(20)
    # 申万行业实时行情没有涨跌幅列，需要手动计算
    realtime_sw['涨跌幅'] = round((realtime_sw['最新价'] - realtime_sw['昨收盘']) / realtime_sw['昨收盘'] * 100, 2)
    top_industries = realtime_sw.sort_values('涨跌幅', ascending=False).head(20)
    names = top_industries['指数名称'].tolist()
    changes = top_industries['涨跌幅'].tolist()
    colors_bar = ['#FF6B6B' if c < 0 else '#4ECDC4' for c in changes]

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('申万行业指数涨跌幅（前20）', fontproperties=chinese_font_title, fontsize=16)

    bars = ax.barh(range(len(names)), changes, color=colors_bar, alpha=0.8)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontproperties=chinese_font_small)
    ax.set_xlabel('涨跌幅（%）', fontproperties=chinese_font)
    ax.axvline(x=0, color='gray', linewidth=0.5)
    ax.grid(True, alpha=0.3, axis='x')

    for bar, val in zip(bars, changes):
        if val >= 0:
            ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                   f'{val:.2f}%', va='center', fontproperties=chinese_font_small)
        else:
            ax.text(val - 0.5, bar.get_y() + bar.get_height()/2,
                   f'{val:.2f}%', va='center', fontproperties=chinese_font_small)

    plt.tight_layout()
    save_fig(fig, f'申万行业涨跌幅_{TIMESTAMP}.png')


# ============================================================
# 汇总报告
# ============================================================
print_header('指数数据研究完成')

print(f'  研究时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'  数据文件目录: {DATA_DIR}')
print(f'  图表文件目录: {PLOT_DIR}')
print()

# 列出生成的CSV文件
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and TIMESTAMP in f]
print(f'  生成的CSV文件 ({len(csv_files)}个):')
for f in sorted(csv_files):
    fpath = os.path.join(DATA_DIR, f)
    size = os.path.getsize(fpath)
    print(f'    - {f} ({size/1024:.1f} KB)')

# 列出生成的PNG文件
png_files = [f for f in os.listdir(PLOT_DIR) if f.endswith('.png') and TIMESTAMP in f]
print(f'\n  生成的PNG图表 ({len(png_files)}个):')
for f in sorted(png_files):
    fpath = os.path.join(PLOT_DIR, f)
    size = os.path.getsize(fpath)
    print(f'    - {f} ({size/1024:.1f} KB)')

print()
print('=' * 70)
print('  研究完成！')
print('=' * 70)
