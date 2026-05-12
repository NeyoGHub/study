#!/usr/bin/env python3
"""AkShare 外汇数据综合示例 (阶段5.1)"""

import akshare as ak, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from datetime import datetime
import os, warnings
warnings.filterwarnings('ignore')

FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
cf = fm.FontProperties(fname=FONT_PATH, size=12) if os.path.exists(FONT_PATH) else fm.FontProperties(size=12)
cf_t = fm.FontProperties(fname=FONT_PATH, size=14) if os.path.exists(FONT_PATH) else fm.FontProperties(size=14)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'forex')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'forex')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  AkShare 外汇数据综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)

# 1. 中行外汇牌价
print('\n1. 外汇牌价')
df_boc = ak.currency_boc_sina()
df_boc.to_csv(os.path.join(DATA_DIR, f'中行外汇牌价_{TS}.csv'), index=False, encoding='utf-8-sig')
print(f'  ✓ {len(df_boc)} 行数据已保存')

# 2. 即期报价
df_spot = ak.fx_spot_quote()
df_spot.to_csv(os.path.join(DATA_DIR, f'即期报价_{TS}.csv'), index=False, encoding='utf-8-sig')
usd_cny = df_spot[df_spot['货币对'] == 'USD/CNY'].iloc[0] if len(df_spot) > 0 else None
if usd_cny is not None:
    print(f'  USD/CNY: {usd_cny["买报价"]} / {usd_cny["卖报价"]}')

# 3. 货币对报价
df_pairs = ak.fx_pair_quote()
df_pairs.to_csv(os.path.join(DATA_DIR, f'货币对报价_{TS}.csv'), index=False, encoding='utf-8-sig')

# 4. 掉期报价
df_swap = ak.fx_swap_quote()
df_swap.to_csv(os.path.join(DATA_DIR, f'掉期报价_{TS}.csv'), index=False, encoding='utf-8-sig')

# 5. 可视化：中行外汇牌价走势
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('美元/人民币 中行外汇牌价', fontproperties=cf_t, size=16)
dates = pd.to_datetime(df_boc['日期'])
ax.plot(dates, df_boc['中行汇买价'], label='汇买价', lw=1.5)
ax.plot(dates, df_boc['中行钞卖价/汇卖价'], label='汇卖价', lw=1.5)
ax.fill_between(dates, df_boc['中行汇买价'], df_boc['中行钞卖价/汇卖价'], alpha=0.15)
ax.set_ylabel('人民币/100外币', fontproperties=cf)
ax.legend(prop=cf)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.tight_layout()
fig.savefig(os.path.join(PLOT_DIR, f'美元牌价_{TS}.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'  ✓ 图表已保存')

print(f'\n{"="*70}')
print(f'  研究完成！')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
