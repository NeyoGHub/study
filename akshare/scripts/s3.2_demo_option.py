#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 期权数据综合示例 (阶段3.2)

功能：
1. ETF期权行情总览（50ETF）
2. 看涨/看跌期权对比
3. 期权希腊字母分析
4. 股指期权行情
5. 波动率分析
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
if os.path.exists(FONT_PATH):
    cf = fm.FontProperties(fname=FONT_PATH, size=12)
    cf_t = fm.FontProperties(fname=FONT_PATH, size=14)
    cf_s = fm.FontProperties(fname=FONT_PATH, size=10)
else:
    cf = cf_t = cf_s = fm.FontProperties(size=12)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'option')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'option')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  AkShare 期权数据综合示例')
print(f'  运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)


def safe(fn, **kw):
    try:
        return fn(**kw)
    except:
        return None


def save_fig(fig, name):
    path = os.path.join(PLOT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓ 图表: {name}')


# ============================================================
# 1. ETF期权行情总览
# ============================================================
print('\n1. ETF期权行情（50ETF）')

# 获取50ETF看涨/看跌期权代码
calls = safe(ak.option_sse_codes_sina, symbol='看涨期权', trade_date='202605', underlying='510050')
puts = safe(ak.option_sse_codes_sina, symbol='认沽期权', trade_date='202605', underlying='510050')

if calls is not None and puts is not None:
    print(f'  50ETF 5月期权: 看涨{len(calls)}个, 认沽{len(puts)}个')

    # 获取所有期权实时行情
    call_data = []
    for _, row in calls.iterrows():
        code = row['期权代码']
        d = safe(ak.option_sse_spot_price_sina, symbol=code)
        if d is not None:
            vals = dict(zip(d['字段'], d['值']))
            call_data.append(vals)

    put_data = []
    for _, row in puts.iterrows():
        code = row['期权代码']
        d = safe(ak.option_sse_spot_price_sina, symbol=code)
        if d is not None:
            vals = dict(zip(d['字段'], d['值']))
            put_data.append(vals)

    if call_data:
        df_calls = pd.DataFrame(call_data)
        csv = os.path.join(DATA_DIR, f'50ETF看涨期权_{TS}.csv')
        df_calls.to_csv(csv, index=False, encoding='utf-8-sig')
        print(f'  ✓ 数据: 看涨期权行情已保存')
        # 绘制行权价-价格曲线
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.suptitle('50ETF 5月看涨期权 - 行权价 vs 价格', fontproperties=cf_t, size=16)
        strikes = [float(v) for v in df_calls['行权价']]
        prices = [float(v) for v in df_calls['最新价']]
        ax.plot(strikes, prices, 'o-', color='#4ECDC4', lw=2)
        ax.set_xlabel('行权价', fontproperties=cf)
        ax.set_ylabel('期权价格', fontproperties=cf)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        save_fig(fig, f'50ETF看涨期权_{TS}.png')

    if put_data:
        df_puts = pd.DataFrame(put_data)
        csv = os.path.join(DATA_DIR, f'50ETF认沽期权_{TS}.csv')
        df_puts.to_csv(csv, index=False, encoding='utf-8-sig')
        print(f'  ✓ 数据: 认沽期权行情已保存')

# ============================================================
# 2. 期权希腊字母
# ============================================================
print('\n2. 期权希腊字母分析')
greeks = safe(ak.option_sse_greeks_sina, symbol='10011381')
if greeks is not None:
    vals = dict(zip(greeks['字段'], greeks['值']))
    print(f'  Delta: {vals.get("Delta")}, Gamma: {vals.get("Gamma")}')
    print(f'  Theta: {vals.get("Theta")}, Vega: {vals.get("Vega")}')
    print(f'  隐含波动率: {vals.get("隐含波动率")}')
    csv = os.path.join(DATA_DIR, f'希腊字母_{TS}.csv')
    greeks.to_csv(csv, index=False, encoding='utf-8-sig')

# ============================================================
# 3. 股指期权行情
# ============================================================
print('\n3. 股指期权行情')
for name, fn in [('沪深300', ak.option_cffex_hs300_spot_sina),
                  ('上证50', ak.option_cffex_sz50_spot_sina),
                  ('中证1000', ak.option_cffex_zz1000_spot_sina)]:
    d = safe(fn)
    if d is not None:
        print(f'  {name}: {len(d)} 个行权价合约')

# ============================================================
# 4. 波动率
# ============================================================
print('\n4. 波动率分析')
d = safe(ak.option_vol_shfe)
if d is not None:
    print(f'  上期所: {len(d)} 个合约系列')
    csv = os.path.join(DATA_DIR, f'波动率_{TS}.csv')
    d.to_csv(csv, index=False, encoding='utf-8-sig')

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('上期所期权隐含波动率', fontproperties=cf_t, size=16)
    contracts = d['合约系列'].tolist()
    vols = []
    for v in d['隐含波动率'].tolist():
        try:
            vols.append(float(v))
        except:
            vols.append(0)
    colors = ['#4ECDC4' if v < 0.2 else '#FF6B6B' for v in vols]
    bars = ax.bar(range(len(contracts)), vols, color=colors, alpha=0.8)
    ax.set_xticks(range(len(contracts)))
    ax.set_xticklabels(contracts, fontproperties=cf_s, rotation=45)
    ax.set_ylabel('隐含波动率', fontproperties=cf)
    ax.axhline(y=0.2, color='gray', ls='--', alpha=0.5)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    save_fig(fig, f'隐含波动率_{TS}.png')

print('\n' + '=' * 70)
print('  研究完成！')
print('=' * 70)
print(f'\n  数据文件: {DATA_DIR}/')
for f in sorted(os.listdir(DATA_DIR)):
    if TS in f:
        print(f'    {f}')
print(f'\n  图表文件: {PLOT_DIR}/')
for f in sorted(os.listdir(PLOT_DIR)):
    if TS in f:
        print(f'    {f}')
print(f'\n  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)
