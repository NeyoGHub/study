#!/usr/bin/env python3
"""AkShare REITs数据综合示例 (阶段5.3 - 新浪替代)"""

import akshare as ak, pandas as pd, numpy as np, matplotlib
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
cf_s = fm.FontProperties(fname=FONT_PATH, size=9) if os.path.exists(FONT_PATH) else fm.FontProperties(size=9)

BASE_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(BASE_DIR, 'data', 'reits')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'reits')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

reits = [
    ('sh508000','张江REIT','产业园'),('sh508001','浙江杭徽','高速'),
    ('sh508006','首创水务','水务'),('sh508008','国金铁建','高速'),
    ('sh508027','东吴苏园','产业园'),('sh508056','中金普洛斯','仓储'),
    ('sh508066','京东仓储','仓储'),('sh508077','京能光伏','能源'),
    ('sh508088','国泰君安','产业园'),('sh508096','中国交建','高速'),
    ('sh508097','中国铁建','高速'),('sh508098','电建清源','能源'),
    ('sh508099','国家电投','能源'),('sz180101','平安广州','水务'),
    ('sz180102','蛇口产园','产业园'),('sz180103','红土盐田','仓储'),
    ('sz180201','鹏华前海','综合'),
]

print('=' * 70)
print('  AkShare REITs数据综合示例')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)

all_data = {}
for code, name, cat in reits:
    d = ak.fund_etf_hist_sina(symbol=code)
    if d is not None and len(d) > 0:
        d['name'] = name
        d['category'] = cat
        all_data[code] = d

print(f'\n获取 {len(all_data)}/{len(reits)} 个REITs数据')

# 按类别汇总
cats = {}
for code, d in all_data.items():
    cat = d['category'].iloc[0]
    if cat not in cats: cats[cat] = []
    cats[cat].append(d['name'].iloc[0])

print('\n类别分布:')
for cat, names in sorted(cats.items()):
    print(f'  {cat}: {len(names)} 只 - {", ".join(names)}')

# 计算各REIT最新价和涨跌幅
summary = []
for code, d in all_data.items():
    d_sorted = d.sort_values('date')
    if len(d_sorted) >= 2:
        first = d_sorted['close'].iloc[0]
        last = d_sorted['close'].iloc[-1]
        pct = (last - first) / first * 100
        name = d['name'].iloc[0]
        cat = d['category'].iloc[0]
        summary.append({'代码': code, '名称': name, '类别': cat,
                       '上市价': round(first,3), '最新价': round(last,3),
                       '涨跌幅%': round(pct,1), '天数': len(d)})

df_summary = pd.DataFrame(summary)
df_summary.to_csv(os.path.join(DATA_DIR, f'REITs汇总_{TS}.csv'), index=False, encoding='utf-8-sig')
print(f'\n✓ REITs汇总表已保存')

# 走势对比图
fig, ax = plt.subplots(figsize=(14, 7))
fig.suptitle('中国REITs走势对比（归一化）', fontproperties=cf_t, size=16)
colors = plt.cm.Set3(np.linspace(0, 1, len(all_data)))
for (code, d), color in zip(all_data.items(), colors):
    d_sorted = d.sort_values('date')
    norm = d_sorted['close'] / d_sorted['close'].iloc[0] * 100
    dates = pd.to_datetime(d_sorted['date'])
    ax.plot(dates, norm, label=d['name'].iloc[0], lw=1, alpha=0.7, color=color)
ax.set_ylabel('归一化价格 (基期=100)', fontproperties=cf)
ax.legend(prop=cf_s, ncol=3, fontsize=8)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.tight_layout()
fig.savefig(os.path.join(PLOT_DIR, f'REITs走势_{TS}.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'✓ 走势对比图已保存')

# 涨跌幅排行
fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('REITs上市以来涨跌幅', fontproperties=cf_t, size=16)
df_sorted = df_summary.sort_values('涨跌幅%')
colors_bar = ['#4ECDC4' if v >= 0 else '#FF6B6B' for v in df_sorted['涨跌幅%']]
bars = ax.barh(range(len(df_sorted)), df_sorted['涨跌幅%'], color=colors_bar, alpha=0.8)
ax.set_yticks(range(len(df_sorted)))
ax.set_yticklabels([f"{r['名称']}({r['类别']})" for _, r in df_sorted.iterrows()], fontproperties=cf_s)
ax.set_xlabel('涨跌幅 (%)', fontproperties=cf)
ax.axvline(x=0, color='gray', lw=0.5)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
fig.savefig(os.path.join(PLOT_DIR, f'REITs涨跌幅_{TS}.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'✓ 涨跌幅排行图已保存')

print(f'\n{"="*70}')
print(f'  REITs研究完成！（使用 fund_etf_hist_sina 替代东方财富）')
print(f'  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'{"="*70}')
