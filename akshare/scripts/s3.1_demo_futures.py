#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 期货数据综合示例 (阶段3.1)

功能：
1. 期货品种总览
2. 主力合约走势对比（螺纹钢 vs 沪铜）
3. 技术指标计算（均线、MACD、RSI）
4. 外盘期货行情（原油、黄金）
5. 期现价差分析
6. 库存数据可视化
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
# 中文字体设置
# ============================================================
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
if os.path.exists(FONT_PATH):
    chinese_font = fm.FontProperties(fname=FONT_PATH, size=12)
    chinese_font_title = fm.FontProperties(fname=FONT_PATH, size=14)
    chinese_font_small = fm.FontProperties(fname=FONT_PATH, size=10)
else:
    chinese_font = fm.FontProperties(size=12)
    chinese_font_title = fm.FontProperties(size=14)
    chinese_font_small = fm.FontProperties(size=10)

# ============================================================
# 输出目录
# ============================================================
BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'futures')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'futures')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  AkShare 期货数据综合示例')
print('=' * 70)
print(f'  运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)


def safe_api(api, **kwargs):
    try:
        return api(**kwargs)
    except Exception as e:
        print(f'  ⚠ 调用失败: {type(e).__name__}')
        return None


def calc_ma(df, col='收盘价', windows=[5, 10, 20, 60]):
    for w in windows:
        df[f'MA{w}'] = df[col].rolling(w).mean()
    return df


def calc_macd(df, col='收盘价'):
    e12 = df[col].ewm(span=12).mean()
    e26 = df[col].ewm(span=26).mean()
    df['DIF'] = e12 - e26
    df['DEA'] = df['DIF'].ewm(span=9).mean()
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    return df


def calc_rsi(df, col='收盘价', n=14):
    delta = df[col].diff()
    gain = delta.where(delta > 0, 0).rolling(n).mean()
    loss = (-delta).where(delta < 0, 0).rolling(n).mean()
    rs = gain / loss
    df['RSI'] = 100 - 100 / (1 + rs)
    return df


def save_fig(fig, name):
    path = os.path.join(PLOT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓ 已保存: {path}')


# ============================================================
# 1. 主力合约走势（螺纹钢）
# ============================================================
print('\n1. 螺纹钢主力合约走势')
df_rb = safe_api(ak.futures_main_sina, symbol='RB0')
if df_rb is not None and len(df_rb) > 0:
    df_rb = df_rb.sort_values('日期')
    df_rb = calc_ma(df_rb)
    df_rb = calc_macd(df_rb)
    df_rb = calc_rsi(df_rb)
    print(f'  获取 {len(df_rb)} 条数据 (2009-03 ~ 至今)')
    print(f'  最新收盘: {df_rb["收盘价"].iloc[-1]:.0f}')
    print(f'  RSI(14): {df_rb["RSI"].iloc[-1]:.1f}')

    csv_path = os.path.join(DATA_DIR, f'螺纹钢主力_{TIMESTAMP}.csv')
    df_rb.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')

    # 绘制技术分析图（最近200个交易日）
    recent = df_rb.tail(200)
    dates = pd.to_datetime(recent['日期'])

    fig, axes = plt.subplots(3, 1, figsize=(14, 10),
                             gridspec_kw={'height_ratios': [3, 1, 1]})
    fig.suptitle('螺纹钢主力合约 - 技术分析', fontproperties=chinese_font_title, size=16)

    ax1 = axes[0]
    ax1.plot(dates, recent['收盘价'], label='收盘价', color='#333', lw=1.5)
    ax1.plot(dates, recent['MA5'], label='MA5', ls='--', lw=1)
    ax1.plot(dates, recent['MA20'], label='MA20', ls='--', lw=1)
    ax1.plot(dates, recent['MA60'], label='MA60', ls='--', lw=1)
    ax1.set_ylabel('价格 (元/吨)', fontproperties=chinese_font)
    ax1.legend(prop=chinese_font_small, loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    ax2 = axes[1]
    colors = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in recent['MACD']]
    ax2.bar(dates, recent['MACD'], color=colors, width=1.5, alpha=0.7)
    ax2.plot(dates, recent['DIF'], color='#333', lw=1, label='DIF')
    ax2.plot(dates, recent['DEA'], color='#FF6B6B', lw=1, label='DEA')
    ax2.axhline(0, color='gray', lw=0.5)
    ax2.legend(prop=chinese_font_small, loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    ax3 = axes[2]
    ax3.plot(dates, recent['RSI'], color='#6C5CE7', lw=1.5)
    ax3.axhline(70, color='#FF6B6B', ls='--', alpha=0.5)
    ax3.axhline(30, color='#4ECDC4', ls='--', alpha=0.5)
    ax3.fill_between(dates, 70, 30, alpha=0.05, color='gray')
    ax3.set_ylim(0, 100)
    ax3.set_ylabel('RSI', fontproperties=chinese_font)
    ax3.set_xlabel('日期', fontproperties=chinese_font)
    ax3.grid(True, alpha=0.3)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    plt.tight_layout()
    save_fig(fig, f'螺纹钢技术分析_{TIMESTAMP}.png')

# ============================================================
# 2. 多品种走势对比（归一化）
# ============================================================
print('\n2. 多品种走势对比')
df_cu = safe_api(ak.futures_main_sina, symbol='CU0')
if df_rb is not None and df_cu is not None:
    df_rb_sorted = df_rb.sort_values('日期')
    df_cu_sorted = df_cu.sort_values('日期')

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('期货主力合约走势对比（归一化）', fontproperties=chinese_font_title, size=16)

    for name, data in [('螺纹钢(RB)', df_rb_sorted), ('沪铜(CU)', df_cu_sorted)]:
        d = data.tail(500)
        prices = d['收盘价'].values
        norm = prices / prices[0] * 100
        ax.plot(pd.to_datetime(d['日期']), norm, label=name, lw=1.5)

    ax.set_ylabel('归一化价格（基期=100）', fontproperties=chinese_font)
    ax.legend(prop=chinese_font, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    save_fig(fig, f'期货走势对比_{TIMESTAMP}.png')

# ============================================================
# 3. 外盘期货行情
# ============================================================
print('\n3. 外盘期货行情')
foreign = []
for sym, name in [('CL', 'NYMEX原油'), ('GC', 'COMEX黄金'), ('SI', 'COMEX白银')]:
    d = safe_api(ak.futures_foreign_commodity_realtime, symbol=sym)
    if d is not None and len(d) > 0:
        row = d.iloc[0]
        foreign.append({'品种': name, '最新价': row['最新价'],
                        '涨跌幅': row['涨跌幅'], '人民币报价': row['人民币报价']})
        print(f'  {name}: {row["最新价"]} ({row["涨跌幅"]}%)')

if foreign:
    df_foreign = pd.DataFrame(foreign)
    csv_path = os.path.join(DATA_DIR, f'外盘期货_{TIMESTAMP}.csv')
    df_foreign.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')

# ============================================================
# 4. 期现价差
# ============================================================
print('\n4. 期现价差分析')
df_basis = safe_api(ak.futures_spot_price_daily)
if df_basis is not None and len(df_basis) > 0:
    csv_path = os.path.join(DATA_DIR, f'期现价差_{TIMESTAMP}.csv')
    df_basis.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}（{len(df_basis)} 条记录）')

    # 选取几个常见品种绘制基差
    symbols = ['C', 'A', 'M', 'RB', 'CU']
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('主要品种期现价差（基差率）', fontproperties=chinese_font_title, size=16)
    for sym in symbols:
        sub = df_basis[df_basis['symbol'] == sym].tail(100)
        if len(sub) > 5:
            dates = pd.to_datetime(sub['date'])
            ax.plot(dates, sub['dom_basis_rate'] * 100, label=sym, lw=1.5)
    ax.set_ylabel('基差率 (%)', fontproperties=chinese_font)
    ax.axhline(0, color='gray', lw=0.5)
    ax.legend(prop=chinese_font, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    save_fig(fig, f'期现价差_{TIMESTAMP}.png')

# ============================================================
# 5. 库存数据
# ============================================================
print('\n5. 库存数据分析')
df_inv = safe_api(ak.futures_inventory_em, symbol='a')
if df_inv is not None and len(df_inv) > 0:
    csv_path = os.path.join(DATA_DIR, f'大豆库存_{TIMESTAMP}.csv')
    df_inv.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}（{len(df_inv)} 条记录）')

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle('大豆库存变化', fontproperties=chinese_font_title, size=16)
    dates = pd.to_datetime(df_inv['日期'])
    ax.fill_between(dates, df_inv['库存'], alpha=0.3, color='#45B7D1')
    ax.plot(dates, df_inv['库存'], color='#2C3E50', lw=1.5)
    ax.set_ylabel('库存', fontproperties=chinese_font)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    save_fig(fig, f'大豆库存_{TIMESTAMP}.png')

# ============================================================
# 汇总
# ============================================================
print('\n' + '=' * 70)
print('  研究完成！')
print('=' * 70)
print(f'\n  数据文件: {DATA_DIR}/')
for f in sorted(os.listdir(DATA_DIR)):
    if TIMESTAMP in f:
        fpath = os.path.join(DATA_DIR, f)
        print(f'    {f} ({os.path.getsize(fpath)/1024:.1f} KB)')

print(f'\n  图表文件: {PLOT_DIR}/')
for f in sorted(os.listdir(PLOT_DIR)):
    if TIMESTAMP in f:
        fpath = os.path.join(PLOT_DIR, f)
        print(f'    {f} ({os.path.getsize(fpath)/1024:.1f} KB)')

print(f'\n  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)
