#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AkShare 宏观经济数据综合示例 (阶段4.1)"""

import akshare as ak
import pandas as pd
import matplotlib
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
DATA_DIR = os.path.join(BASE_DIR, 'data', 'macro')
PLOT_DIR = os.path.join(BASE_DIR, 'plots', 'macro')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 70)
print('  AkShare 宏观经济数据综合示例')
print(f'  运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)


def safe(fn, **kw):
    try:
        return fn(**kw)
    except:
        return None


def save(df, name):
    if df is not None and len(df) > 0:
        p = os.path.join(DATA_DIR, f'{name}_{TS}.csv')
        df.to_csv(p, index=False, encoding='utf-8-sig')
        return True
    return False


def save_fig(fig, name):
    p = os.path.join(PLOT_DIR, name)
    fig.savefig(p, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# 1. GDP
print('\n1. GDP')
df_gdp = safe(ak.macro_china_gdp_yearly)
if df_gdp is not None:
    save(df_gdp, 'GDP')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('中国GDP年率', fontproperties=cf_t, size=16)
    dates = pd.to_datetime(df_gdp['日期'])
    ax.plot(dates, df_gdp['今值'], 'o-', color='#4ECDC4', lw=2)
    ax.fill_between(dates, 0, df_gdp['今值'], alpha=0.2, color='#4ECDC4')
    ax.set_ylabel('%', fontproperties=cf)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    save_fig(fig, f'GDP_{TS}.png')
    print(f'  ✓ GDP数据已保存')

# 2. CPI + PPI
print('2. CPI与PPI走势')
df_cpi = safe(ak.macro_china_cpi)
df_ppi = safe(ak.macro_china_ppi)
if df_cpi is not None:
    save(df_cpi, 'CPI')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('中国CPI与PPI走势', fontproperties=cf_t, size=16)
    cpi_dates_raw = [str(d).replace('年', '-').replace('月份', '') for d in df_cpi['月份']]
    cpi_dates = [pd.to_datetime(d) if d and '20' in str(d) else None for d in cpi_dates_raw]
    cpi_dates_s = pd.Series(cpi_dates)
    mask_cpi = cpi_dates_s.notna()
    ax.plot(cpi_dates_s[mask_cpi], df_cpi.loc[mask_cpi.values, '全国-同比增长'], label='CPI同比', color='#FF6B6B', lw=1.5)
    if df_ppi is not None:
        ppi_raw = [str(d).replace('年', '-').replace('月份', '') for d in df_ppi['月份']]
        ppi_dates = [pd.to_datetime(d) if d and '20' in str(d) else None for d in ppi_raw]
        ppi_dates_s = pd.Series(ppi_dates)
        mask_ppi = ppi_dates_s.notna()
        ax.plot(ppi_dates_s[mask_ppi], df_ppi.loc[mask_ppi.values, '当月同比增长'], label='PPI同比', color='#4ECDC4', lw=1.5)
        save(df_ppi, 'PPI')
    ax.axhline(y=0, color='gray', lw=0.5)
    ax.set_ylabel('同比增长 (%)', fontproperties=cf)
    ax.legend(prop=cf, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    save_fig(fig, f'CPI_PPI_{TS}.png')
    print(f'  ✓ CPI/PPI图表已保存')

# 3. LPR
print('3. LPR利率')
df_lpr = safe(ak.macro_china_lpr)
if df_lpr is not None:
    save(df_lpr, 'LPR')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('LPR利率走势', fontproperties=cf_t, size=16)
    lpr_dates = pd.to_datetime(df_lpr['TRADE_DATE'])
    ax.plot(lpr_dates, df_lpr['LPR1Y'], label='LPR 1Y', color='#FF6B6B', lw=1.5)
    ax.plot(lpr_dates, df_lpr['LPR5Y'], label='LPR 5Y', color='#4ECDC4', lw=1.5)
    ax.set_ylabel('利率 (%)', fontproperties=cf)
    ax.legend(prop=cf)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    save_fig(fig, f'LPR_{TS}.png')
    print(f'  ✓ LPR图表已保存')

# 4. SHIBOR
print('4. SHIBOR')
df_shibor = safe(ak.macro_china_shibor_all)
if df_shibor is not None:
    save(df_shibor, 'SHIBOR')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('SHIBOR利率', fontproperties=cf_t, size=16)
    shibor_dates = pd.to_datetime(df_shibor['日期'])
    ax.plot(shibor_dates, df_shibor['O/N-定价'], label='隔夜', lw=1, alpha=0.7)
    ax.plot(shibor_dates, df_shibor['1W-定价'], label='1周', lw=1, alpha=0.7)
    ax.legend(prop=cf)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    save_fig(fig, f'SHIBOR_{TS}.png')
    print(f'  ✓ SHIBOR图表已保存')

# 5. PMI
print('5. PMI')
df_pmi = safe(ak.macro_china_pmi)
if df_pmi is not None:
    save(df_pmi, 'PMI')
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle('中国PMI指数', fontproperties=cf_t, size=16)
    pmi_dates_raw = [str(d).replace('年', '-').replace('月份', '') for d in df_pmi['月份']]
    pmi_dates = [pd.to_datetime(d) if d and '20' in str(d) else None for d in pmi_dates_raw]
    pmi_dates_s = pd.Series(pmi_dates)
    mask_pmi = pmi_dates_s.notna()
    ax.plot(pmi_dates_s[mask_pmi], df_pmi.loc[mask_pmi.values, '制造业-指数'], label='制造业', lw=1.5)
    ax.plot(pmi_dates_s[mask_pmi], df_pmi.loc[mask_pmi.values, '非制造业-指数'], label='非制造业', lw=1.5)
    ax.axhline(y=50, color='gray', ls='--', alpha=0.5)
    ax.set_ylabel('PMI', fontproperties=cf)
    ax.legend(prop=cf)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.tight_layout()
    save_fig(fig, f'PMI_{TS}.png')
    print(f'  ✓ PMI图表已保存')

print('\n' + '=' * 70)
print('  研究完成！')
print('=' * 70)
for d in ['data/macro', 'plots/macro']:
    print(f'\n  output/{d}/:')
    for f in sorted(os.listdir(os.path.join(BASE_DIR, d.replace('/', '/')))
                    if os.path.isdir(os.path.join(BASE_DIR, d.replace('/', '/')))
                    else []):
        if TS in f:
            fpath = os.path.join(BASE_DIR, d.replace('/', '/'), f)
            print(f'    {f} ({os.path.getsize(fpath)/1024:.1f} KB)')
print(f'\n  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
