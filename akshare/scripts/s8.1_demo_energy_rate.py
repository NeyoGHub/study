#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 能源+利率 综合示例 (阶段8.1)"""

import akshare as ak
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import os, warnings
warnings.filterwarnings('ignore')

FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
cf = fm.FontProperties(fname=FONT_PATH, size=12) if os.path.exists(FONT_PATH) else fm.FontProperties(size=12)
cf_t = fm.FontProperties(fname=FONT_PATH, size=14) if os.path.exists(FONT_PATH) else fm.FontProperties(size=14)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'energy_rate')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'energy_rate')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  能源与利率综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)


def safe(fn, **kw):
    try:
        return fn(**kw)
    except:
        return None


def save_csv(df, name):
    if df is not None and hasattr(df, 'to_csv'):
        df.to_csv(f'{DATA_DIR}/{name}_{TS}.csv', index=False, encoding='utf-8-sig')
        return True
    return False


def save_fig(fig, name):
    fig.savefig(f'{PLOT_DIR}/{name}_{TS}.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# 1. 能源
print('\n1. 能源数据')
df_oil = safe(ak.energy_oil_detail)
if df_oil is not None:
    save_csv(df_oil, '原油价格')
    print(f'  ✓ 原油价格已保存')

df_oil_hist = safe(ak.energy_oil_hist)
if df_oil_hist is not None:
    save_csv(df_oil_hist, '油价调整历史')
    print(f'  ✓ 油价调整历史已保存 ({len(df_oil_hist)}次)')

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('国内油价调整历史', fontproperties=cf_t, size=16)
    dates = pd.to_datetime(df_oil_hist['调整日期'])
    ax.plot(dates, df_oil_hist['汽油价格'], label='汽油', color='#FF6B6B', lw=1.5)
    ax.plot(dates, df_oil_hist['柴油价格'], label='柴油', color='#4ECDC4', lw=1.5)
    ax.set_ylabel('价格 (元/吨)', fontproperties=cf)
    ax.legend(prop=cf)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_fig(fig, '油价走势')
    print(f'  ✓ 油价走势图已保存')

# 2. 利率
print('\n2. 利率数据')
rates = [
    ('美联储', ak.macro_bank_usa_interest_rate),
    ('中国央行', ak.macro_bank_china_interest_rate),
    ('欧央行', ak.macro_bank_euro_interest_rate),
]
for name, fn in rates:
    d = safe(fn)
    if d is not None:
        save_csv(d, name)
        print(f'  ✓ {name}利率已保存')

# 回购利率
df_repo = safe(ak.repo_rate_query)
if df_repo is not None:
    save_csv(df_repo, '回购利率')
    print(f'  ✓ 回购利率已保存')

# 利率走势图
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('主要国家央行利率对比', fontproperties=cf_t, size=16)
colors = {'美联储': '#FF6B6B', '欧央行': '#4ECDC4', '中国央行': '#45B7D1'}
for name, fn in rates:
    d = safe(fn)
    if d is not None and '日期' in d.columns:
        dates = pd.to_datetime(d['日期'])
        val_col = [c for c in d.columns if '今值' in c or '利率' in c][0]
        ax.plot(dates, d[val_col], label=name, color=colors.get(name), lw=1.5)
ax.legend(prop=cf)
ax.set_ylabel('利率 (%)', fontproperties=cf)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_fig(fig, '利率对比')
print(f'  ✓ 利率对比图已保存')

print(f'\n{"="*70}')
print(f'  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
