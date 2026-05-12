#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 行业数据综合示例 (阶段4.2)"""

import akshare as ak, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import os, warnings
warnings.filterwarnings('ignore')

FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
cf = fm.FontProperties(fname=FONT_PATH, size=12) if os.path.exists(FONT_PATH) else fm.FontProperties(size=12)
cf_t = fm.FontProperties(fname=FONT_PATH, size=14) if os.path.exists(FONT_PATH) else fm.FontProperties(size=14)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'industry')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'industry')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  AkShare 行业数据综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)

# 获取申万行业分类
d1 = ak.sw_index_first_info()
d2 = ak.sw_index_second_info()
d3 = ak.sw_index_third_info()

print(f'\n申万行业: 一级{len(d1)}个 → 二级{len(d2)}个 → 三级{len(d3)}个')

# 保存CSV
for name, d in [('一级行业', d1), ('二级行业', d2), ('三级行业', d3)]:
    p = os.path.join(DATA_DIR, f'{name}_{TS}.csv')
    d.to_csv(p, index=False, encoding='utf-8-sig')

# 一级行业成分个数排行
fig, ax = plt.subplots(figsize=(14, 10))
fig.suptitle('申万一级行业 - 成分股个数', fontproperties=cf_t, size=16)
d1_sorted = d1.sort_values('成份个数', ascending=True).tail(25)
ax.barh(range(len(d1_sorted)), d1_sorted['成份个数'], color='#4ECDC4', alpha=0.8)
ax.set_yticks(range(len(d1_sorted)))
ax.set_yticklabels(d1_sorted['行业名称'], fontproperties=cf)
ax.set_xlabel('成份个数', fontproperties=cf)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
p = os.path.join(PLOT_DIR, f'行业成分个数_{TS}.png')
fig.savefig(p, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'\n✓ 图表: 行业成分个数_{TS}.png')

# 行业层级树状统计
fig, ax = plt.subplots(figsize=(14, 6))
fig.suptitle('申万行业层次结构 - 各级别行业数', fontproperties=cf_t, size=16)
levels = ['一级行业', '二级行业', '三级行业']
counts = [len(d1), len(d2), len(d3)]
bars = ax.bar(levels, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
for bar, c in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            str(c), ha='center', fontsize=14, fontweight='bold')
ax.set_ylabel('行业数量', fontproperties=cf)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
p = os.path.join(PLOT_DIR, f'行业层次_{TS}.png')
fig.savefig(p, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'✓ 图表: 行业层次_{TS}.png')

print(f'\n{"="*70}')
print(f'  研究完成！')
print(f'  数据: {DATA_DIR}/')
print(f'  图表: {PLOT_DIR}/')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
