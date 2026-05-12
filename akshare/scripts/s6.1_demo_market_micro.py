#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 龙虎榜+融资融券+沪深港通 综合示例 (阶段6.1)"""

import akshare as ak
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import os, warnings
warnings.filterwarnings('ignore')

FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
cf = fm.FontProperties(fname=FONT_PATH, size=12) if os.path.exists(FONT_PATH) else fm.FontProperties(size=12)
cf_t = fm.FontProperties(fname=FONT_PATH, size=14) if os.path.exists(FONT_PATH) else fm.FontProperties(size=14)
cf_s = fm.FontProperties(fname=FONT_PATH, size=9) if os.path.exists(FONT_PATH) else fm.FontProperties(size=9)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'market_micro')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'market_micro')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  市场微观数据综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)

# 1. 龙虎榜
print('\n1. 龙虎榜分析')
df_lhb = ak.stock_lhb_detail_em()
df_lhb.to_csv(f'{DATA_DIR}/龙虎榜_{TS}.csv', index=False, encoding='utf-8-sig')
print(f'  ✓ 当日上榜 {len(df_lhb)} 只股票')

# 上榜原因分布
if '上榜原因' in df_lhb.columns:
    reasons = df_lhb['上榜原因'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('龙虎榜上榜原因分布', fontproperties=cf_t, size=16)
    bars = ax.barh(range(len(reasons)), reasons.values, color='#FF6B6B', alpha=0.8)
    ax.set_yticks(range(len(reasons)))
    ax.set_yticklabels([r[:25] for r in reasons.index], fontproperties=cf_s)
    ax.set_xlabel('次数', fontproperties=cf)
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    fig.savefig(f'{PLOT_DIR}/龙虎榜原因_{TS}.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  ✓ 龙虎榜原因分布图已保存')

# 2. 融资融券
print('\n2. 融资融券分析')
df_margin = ak.stock_margin_sse()
df_margin.to_csv(f'{DATA_DIR}/融资融券_{TS}.csv', index=False, encoding='utf-8-sig')
print(f'  ✓ 上交所两融 {len(df_margin)} 行数据')

# 融资余额走势
if len(df_margin) > 0:
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('上交所融资余额走势', fontproperties=cf_t, size=16)
    dates = pd.to_datetime(df_margin['信用交易日期'])
    ax.plot(dates, df_margin['融资余额'] / 1e8, color='#4ECDC4', lw=1.5)
    ax.fill_between(dates, 0, df_margin['融资余额'] / 1e8, alpha=0.15, color='#4ECDC4')
    ax.set_ylabel('融资余额 (亿元)', fontproperties=cf)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{PLOT_DIR}/融资余额_{TS}.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  ✓ 融资余额走势图已保存')

# 3. 沪深港通
print('\n3. 沪深港通分析')
df_hsgt = ak.stock_hsgt_hist_em()
df_hsgt.to_csv(f'{DATA_DIR}/沪深港通_{TS}.csv', index=False, encoding='utf-8-sig')
print(f'  ✓ 沪深港通 {len(df_hsgt)} 行数据')

if len(df_hsgt) > 0:
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('沪深港通当日成交净买额', fontproperties=cf_t, size=16)
    dates = pd.to_datetime(df_hsgt['日期'])
    vals = df_hsgt['当日成交净买额']
    colors = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in vals]
    ax.bar(dates, vals, color=colors, width=1, alpha=0.7)
    ax.set_ylabel('净买额 (亿元)', fontproperties=cf)
    ax.axhline(y=0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{PLOT_DIR}/沪深港通净买额_{TS}.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  ✓ 沪深港通净买额图已保存')

print(f'\n{"="*70}')
print(f'  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
