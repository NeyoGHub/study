#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 空气质量+汽车+财富榜单 综合示例 (阶段7.1)"""

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
DATA_DIR = os.path.join(BASE_DIR, 'data', 'alternative')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'alternative')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  另类数据综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)

# 1. 空气质量
print('\n1. 空气质量排名')
df_air = ak.air_quality_rank()
df_air.to_csv(f'{DATA_DIR}/空气质量_{TS}.csv', index=False, encoding='utf-8-sig')

fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('全国城市AQI排名（倒序）', fontproperties=cf_t, size=16)
top = df_air.head(20)
colors = ['#FF6B6B' if v > 100 else '#4ECDC4' if v > 50 else '#45B7D1' for v in top['AQI']]
ax.barh(range(len(top)-1, -1, -1), top['AQI'].values[::-1], color=colors[::-1], alpha=0.8)
ax.set_yticks(range(len(top)))
ax.set_yticklabels(top['城市'].values[::-1], fontproperties=cf_s)
ax.set_xlabel('AQI', fontproperties=cf)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
fig.savefig(f'{PLOT_DIR}/空气质量_{TS}.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'  ✓ 空气质量图已保存 ({len(df_air)}城市)')

# 2. 汽车销量
print('\n2. 汽车销量排行')
df_car = ak.car_sale_rank_gasgoo()
df_car.to_csv(f'{DATA_DIR}/汽车销量_{TS}.csv', index=False, encoding='utf-8-sig')

if hasattr(df_car, 'columns') and '厂商' in df_car.columns:
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('汽车厂商销量排行', fontproperties=cf_t, size=16)
    top = df_car.head(15)
    ax.barh(range(len(top)-1, -1, -1), top.iloc[:, 1].values[::-1], color='#45B7D1', alpha=0.8)
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top['厂商'].values[::-1], fontproperties=cf_s)
    ax.set_xlabel('销量', fontproperties=cf)
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    fig.savefig(f'{PLOT_DIR}/汽车销量_{TS}.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  ✓ 汽车销量图已保存')

# 3. 财富榜单
print('\n3. 财富榜单')
try:
    df_forbes = ak.forbes_rank()
    df_forbes.to_csv(f'{DATA_DIR}/福布斯_{TS}.csv', index=False, encoding='utf-8-sig')
    print(f'  ✓ 福布斯榜单已保存')
except:
    print(f'  - 福布斯榜单获取失败')

try:
    df_hurun = ak.hurun_rank()
    df_hurun.to_csv(f'{DATA_DIR}/胡润_{TS}.csv', index=False, encoding='utf-8-sig')
    print(f'  ✓ 胡润榜单已保存 ({len(df_hurun)}人)')
except:
    print(f'  - 胡润榜单获取失败')

print(f'\n{"="*70}')
print(f'  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
