#!/usr/bin/env python3
"""AkShare QDII数据综合示例 (阶段5.4)"""

import akshare as ak, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
import os, warnings
warnings.filterwarnings('ignore')

FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
cf = fm.FontProperties(fname=FONT_PATH, size=12) if os.path.exists(FONT_PATH) else fm.FontProperties(size=12)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'qdii')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'qdii')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  AkShare QDII数据综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)

# QDII数据
df_a = ak.qdii_a_index_jsl()
df_e = ak.qdii_e_comm_jsl()
df_i = ak.qdii_e_index_jsl()

for name, d in [('QDII指数型', df_a), ('QDII商品型', df_e), ('QDII股票型', df_i)]:
    p = os.path.join(DATA_DIR, f'{name}_{TS}.csv')
    d.to_csv(p, index=False, encoding='utf-8-sig')
    print(f'\n{name} ({len(d)}只):')
    print(d.head(3).to_string())

# 涨幅排行
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('QDII基金涨幅排行', fontproperties=fm.FontProperties(fname=FONT_PATH, size=14) if os.path.exists(FONT_PATH) else fm.FontProperties(size=14))

for ax, data, title in zip(axes, [df_a, df_e, df_i], ['QDII指数型', 'QDII商品型', 'QDII股票型']):
    top = data.head(10)
    names = top['名称'].tolist()
    changes_raw = top['涨幅'].str.rstrip('%').astype(float) if '涨幅' in top.columns else pd.Series([0]*len(top))
    changes = changes_raw.tolist()
    colors = ['#4ECDC4' if c >= 0 else '#FF6B6B' for c in changes]
    bars = ax.barh(range(len(names)), changes, color=colors, alpha=0.8)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontproperties=cf)
    ax.set_title(title, fontproperties=cf)
    ax.axvline(x=0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
fig.savefig(os.path.join(PLOT_DIR, f'QDII涨幅_{TS}.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'\n✓ 图表: QDII涨幅_{TS}.png')

print(f'\n{"="*70}')
print(f'  QDII研究完成！')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
