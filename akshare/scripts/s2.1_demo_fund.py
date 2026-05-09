#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 基金数据综合示例 (阶段2.1)

功能：
1. 基金列表概览 - fund_name_em()
2. 基金排名分析 - fund_open_fund_rank_em()
3. 单只基金净值分析 - fund_open_fund_info_em()
4. ETF市场概览 - fund_etf_category_sina()
5. 基金持仓分析 - fund_portfolio_hold_em()
6. 基金管理人信息 - fund_manager_em()
7. 基金评级与估值 - fund_rating_all() + fund_value_estimation_em()

运行：./venv/bin/python scripts/s2.1_demo_fund.py
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
    font_candidates = [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ]
    FONT_PATH = None
    for fp in font_candidates:
        if os.path.exists(fp):
            FONT_PATH = fp
            break
    if FONT_PATH:
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
OUTPUT_DIR = '/home/neyo/workspace/code/study/akshare/output'
DATA_DIR = os.path.join(OUTPUT_DIR, 'data', 'fund')
PLOT_DIR = os.path.join(OUTPUT_DIR, 'plots', 'fund')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# 时间戳
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')


def print_header(title):
    """打印分隔标题"""
    print()
    print('=' * 70)
    print(f'  {title}')
    print('=' * 70)


def safe_api_call(api_func, *args, **kwargs):
    """安全调用API，带错误处理"""
    try:
        result = api_func(*args, **kwargs)
        return result
    except Exception as e:
        print(f'  ⚠ 调用失败: {type(e).__name__}: {str(e)[:100]}')
        return None


def save_fig(fig, filename):
    """保存图表"""
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓ 已保存: {path}')


# ============================================================
# 第一部分：基金列表概览
# ============================================================
print_header('第一部分：基金列表概览 (fund_name_em)')

fund_list = safe_api_call(ak.fund_name_em)
if fund_list is not None:
    fund_count = len(fund_list)
    print(f'  ✓ 成功获取 {fund_count} 只基金')
    print(f'  列名: {list(fund_list.columns)}')

    # 基金类型分布
    if '基金类型' in fund_list.columns:
        print(f'\n  基金类型分布 (前15):')
        type_dist = fund_list['基金类型'].value_counts().head(15)
        for t, c in type_dist.items():
            print(f'    {t}: {c}只')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'基金列表_{TIMESTAMP}.csv')
    fund_list.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取基金列表失败')


# ============================================================
# 第二部分：基金排名分析
# ============================================================
print_header('第二部分：基金排名分析 (fund_open_fund_rank_em)')

fund_rank = safe_api_call(ak.fund_open_fund_rank_em)
if fund_rank is not None:
    print(f'  ✓ 成功获取 {len(fund_rank)} 只基金排名数据')
    print(f'  列名: {list(fund_rank.columns)}')

    # 找出近1周涨幅最大的基金
    if '近1周' in fund_rank.columns:
        # 转换为数值
        rank_for_sort = fund_rank.copy()
        for col in ['近1周', '近1月', '近3月', '近6月', '近1年', '近3年', '日增长率']:
            if col in rank_for_sort.columns:
                rank_for_sort[col] = pd.to_numeric(rank_for_sort[col], errors='coerce')

        top_weekly = rank_for_sort.nlargest(10, '近1周')[
            ['基金代码', '基金简称', '日期', '单位净值', '近1周', '近1月', '近3月', '日增长率']
        ]
        print(f'\n  近1周涨幅TOP10:')
        print(f'  {"基金代码":<10} {"基金简称":<22} {"近1周":>8} {"近1月":>8} {"近3月":>8} {"日增长率":>8}')
        print(f'  {"-"*60}')
        for _, r in top_weekly.iterrows():
            print(f'  {r["基金代码"]:<10} {str(r["基金简称"])[:20]:<22} '
                  f'{r["近1周"]:>8.2f} {r["近1月"]:>8.2f} {r["近3月"]:>8.2f} {r["日增长率"]:>8.2f}')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'基金排名_{TIMESTAMP}.csv')
    fund_rank.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')

    # 绘制TOP30周涨幅柱状图
    if '近1周' in fund_rank.columns:
        print(f'\n  绘制基金周涨幅TOP30柱状图...')

        top30 = rank_for_sort.nlargest(30, '近1周')
        names = [str(n)[:12] for n in top30['基金简称']]
        vals = top30['近1周'].values
        colors = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in vals]

        fig, ax = plt.subplots(figsize=(14, 9))
        fig.suptitle('开放式基金周涨幅TOP30', fontproperties=chinese_font_title, fontsize=16)

        bars = ax.barh(range(len(names)), vals, color=colors, alpha=0.8)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontproperties=chinese_font_small)
        ax.set_xlabel('近1周涨幅 (%)', fontproperties=chinese_font)
        ax.axvline(x=0, color='gray', linewidth=0.5)
        ax.grid(True, alpha=0.3, axis='x')

        for bar, val in zip(bars, vals):
            if val >= 0:
                ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                        f'{val:.2f}%', va='center', fontproperties=chinese_font_small)
            else:
                ax.text(val - 0.5, bar.get_y() + bar.get_height()/2,
                        f'{val:.2f}%', va='center', fontproperties=chinese_font_small)

        plt.tight_layout()
        save_fig(fig, f'基金周涨幅TOP30_{TIMESTAMP}.png')
else:
    print('  ✗ 获取基金排名失败')


# ============================================================
# 第三部分：单只基金净值分析（华夏成长混合 000001）
# ============================================================
print_header('第三部分：单只基金净值分析 (fund_open_fund_info_em)')

fund_nav = safe_api_call(ak.fund_open_fund_info_em, symbol='000001')
if fund_nav is not None:
    print(f'  ✓ 成功获取华夏成长混合(000001)净值数据: {len(fund_nav)} 条')
    print(f'  列名: {list(fund_nav.columns)}')
    print(f'  日期范围: {fund_nav["净值日期"].iloc[0]} ~ {fund_nav["净值日期"].iloc[-1]}')
    print(f'  最新净值: {fund_nav["单位净值"].iloc[-1]} (日期: {fund_nav["净值日期"].iloc[-1]})')

    # 计算均线
    fund_nav_sorted = fund_nav.sort_values('净值日期').reset_index(drop=True)
    fund_nav_sorted['MA5'] = fund_nav_sorted['单位净值'].rolling(window=5).mean()
    fund_nav_sorted['MA10'] = fund_nav_sorted['单位净值'].rolling(window=10).mean()
    fund_nav_sorted['MA20'] = fund_nav_sorted['单位净值'].rolling(window=20).mean()
    fund_nav_sorted['MA60'] = fund_nav_sorted['单位净值'].rolling(window=60).mean()

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'000001华夏成长净值_{TIMESTAMP}.csv')
    fund_nav_sorted.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')

    # 绘制净值走势图（最近1年）
    print(f'\n  绘制净值走势图...')
    df_plot = fund_nav_sorted.tail(250)  # 约1年交易日
    dates = pd.to_datetime(df_plot['净值日期'])

    fig, axes = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle('华夏成长混合 (000001) 净值走势', fontproperties=chinese_font_title, fontsize=16)

    # 上：净值 + 均线
    ax1 = axes[0]
    ax1.plot(dates, df_plot['单位净值'], label='单位净值', color='#333333', linewidth=1.5)
    ax1.plot(dates, df_plot['MA5'], label='MA5', color='#FF6B6B', linestyle='--', linewidth=1)
    ax1.plot(dates, df_plot['MA10'], label='MA10', color='#4ECDC4', linestyle='--', linewidth=1)
    ax1.plot(dates, df_plot['MA20'], label='MA20', color='#45B7D1', linestyle='--', linewidth=1)
    ax1.plot(dates, df_plot['MA60'], label='MA60', color='#96CEB4', linestyle='--', linewidth=1)

    ax1.set_ylabel('单位净值', fontproperties=chinese_font)
    ax1.legend(prop=chinese_font_small, loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # 下：日增长率
    ax2 = axes[1]
    colors_growth = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in df_plot['日增长率']]
    ax2.bar(dates, df_plot['日增长率'], color=colors_growth, width=1.5, alpha=0.7)
    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
    ax2.set_ylabel('日增长率 (%)', fontproperties=chinese_font)
    ax2.set_xlabel('日期', fontproperties=chinese_font)
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.tight_layout()
    save_fig(fig, f'000001华夏成长净值走势_{TIMESTAMP}.png')

    # 统计指标
    print(f'\n  净值统计:')
    print(f'    区间最大净值: {fund_nav_sorted["单位净值"].max():.4f}')
    print(f'    区间最小净值: {fund_nav_sorted["单位净值"].min():.4f}')
    print(f'    区间平均净值: {fund_nav_sorted["单位净值"].mean():.4f}')
    if '日增长率' in fund_nav_sorted.columns:
        print(f'    区间最大日涨幅: {fund_nav_sorted["日增长率"].max():.2f}%')
        print(f'    区间最大日跌幅: {fund_nav_sorted["日增长率"].min():.2f}%')
        print(f'    日增长率标准差: {fund_nav_sorted["日增长率"].std():.4f}')
else:
    print('  ✗ 获取基金净值失败')


# ============================================================
# 第四部分：ETF市场概览
# ============================================================
print_header('第四部分：ETF市场概览 (fund_etf_category_sina)')

etf_market = safe_api_call(ak.fund_etf_category_sina, symbol='ETF基金')
if etf_market is not None:
    print(f'  ✓ 成功获取 {len(etf_market)} 只ETF数据')
    print(f'  列名: {list(etf_market.columns)}')

    # 转换为数值
    for col in ['最新价', '涨跌幅', '涨跌额', '成交量', '成交额']:
        if col in etf_market.columns:
            etf_market[col] = pd.to_numeric(etf_market[col], errors='coerce')

    # 涨跌幅TOP10
    if '涨跌幅' in etf_market.columns:
        top_gainers = etf_market.nlargest(10, '涨跌幅')[['代码', '名称', '最新价', '涨跌幅', '成交量', '成交额']]
        top_losers = etf_market.nsmallest(10, '涨跌幅')[['代码', '名称', '最新价', '涨跌幅', '成交量', '成交额']]

        print(f'\n  ETF涨幅TOP10:')
        print(f'  {"代码":<12} {"名称":<20} {"最新价":>8} {"涨跌幅":>8} {"成交量":>12}')
        print(f'  {"-"*62}')
        for _, r in top_gainers.iterrows():
            print(f'  {r["代码"]:<12} {str(r["名称"])[:18]:<20} {r["最新价"]:>8.4f} {r["涨跌幅"]:>8.2f} {r["成交量"]:>12.0f}')

        print(f'\n  ETF跌幅TOP10:')
        print(f'  {"代码":<12} {"名称":<20} {"最新价":>8} {"涨跌幅":>8} {"成交量":>12}')
        print(f'  {"-"*62}')
        for _, r in top_losers.iterrows():
            print(f'  {r["代码"]:<12} {str(r["名称"])[:18]:<20} {r["最新价"]:>8.4f} {r["涨跌幅"]:>8.2f} {r["成交量"]:>12.0f}')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'ETF市场行情_{TIMESTAMP}.csv')
    etf_market.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')

    # 绘制ETF涨跌幅TOP30柱状图
    if '涨跌幅' in etf_market.columns:
        print(f'\n  绘制ETF涨跌幅TOP30柱状图...')

        etf_sorted = etf_market.sort_values('涨跌幅', ascending=False)
        top_etf = etf_sorted.head(30)
        names_etf = [str(n)[:14] for n in top_etf['名称']]
        vals_etf = top_etf['涨跌幅'].values
        colors_etf = ['#FF6B6B' if v < 0 else '#4ECDC4' for v in vals_etf]

        fig, ax = plt.subplots(figsize=(14, 9))
        fig.suptitle('ETF涨跌幅TOP30', fontproperties=chinese_font_title, fontsize=16)

        bars = ax.barh(range(len(names_etf)), vals_etf, color=colors_etf, alpha=0.8)
        ax.set_yticks(range(len(names_etf)))
        ax.set_yticklabels(names_etf, fontproperties=chinese_font_small)
        ax.set_xlabel('涨跌幅 (%)', fontproperties=chinese_font)
        ax.axvline(x=0, color='gray', linewidth=0.5)
        ax.grid(True, alpha=0.3, axis='x')

        for bar, val in zip(bars, vals_etf):
            x_pos = val + 0.05 if val >= 0 else val - 0.8
            ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                    f'{val:.2f}%', va='center', fontproperties=chinese_font_small)

        plt.tight_layout()
        save_fig(fig, f'ETF涨跌幅TOP30_{TIMESTAMP}.png')

    # 获取ETF历史数据 - 选一只日内成交活跃的ETF做演示
    # 从ETF列表中找一只成交额最大的ETF
    print(f'\n  获取ETF历史数据（选取成交额最大的ETF）...')
    etf_hist = None
    if '成交额' in etf_market.columns:
        top_etf_by_volume = etf_market.nlargest(1, '成交额')
        top_etf_code = str(top_etf_by_volume['代码'].iloc[0])
        top_etf_name = str(top_etf_by_volume['名称'].iloc[0])
        print(f'  选取: {top_etf_code} {top_etf_name}')
        # 尝试东方财富ETF历史接口
        etf_hist = safe_api_call(ak.fund_etf_hist_em,
                                 symbol=top_etf_code.replace('sh', '').replace('sz', ''),
                                 period='daily',
                                 start_date='20250101', end_date='20260508')
    else:
        # 默认用510050
        top_etf_code = '510050'
        top_etf_name = '上证50ETF'
        etf_hist = safe_api_call(ak.fund_etf_hist_em,
                                 symbol='510050', period='daily',
                                 start_date='20250101', end_date='20260508')

    # 如果东方财富ETF历史接口失败，尝试用同花顺ETF历史接口
    if etf_hist is None or len(etf_hist) == 0:
        print(f'  东方财富ETF历史接口不可用，尝试 fund_etf_hist_ths...')
        try:
            etf_hist_ths = ak.fund_etf_hist_ths(symbol=top_etf_code.replace('sh', '').replace('sz', ''))
            if etf_hist_ths is not None and len(etf_hist_ths) > 0:
                etf_hist = etf_hist_ths
                print(f'  ✓ 同花顺接口获取成功: {len(etf_hist)} 条')
        except Exception as e:
            print(f'  同花顺接口也失败: {type(e).__name__}: {str(e)[:60]}')

    # 最后再尝试用 stock_zh_a_daily
    if etf_hist is None or len(etf_hist) == 0:
        print(f'  再尝试 stock_zh_a_daily 接口...')
        stock_symbol = top_etf_code if top_etf_code.startswith(('sh', 'sz')) else f'sh{top_etf_code}'
        try:
            etf_hist_sina = ak.stock_zh_a_daily(symbol=stock_symbol, adjust='qfq')
            if etf_hist_sina is not None and len(etf_hist_sina) > 0:
                etf_hist = etf_hist_sina.rename(columns={
                    'date': '日期', 'open': '开盘', 'close': '收盘',
                    'high': '最高', 'low': '最低', 'volume': '成交量'
                })
                print(f'  ✓ stock_zh_a_daily 获取成功: {len(etf_hist)} 条')
        except Exception as e:
            print(f'  stock_zh_a_daily 也失败: {type(e).__name__}: {str(e)[:60]}')

    if etf_hist is not None and len(etf_hist) > 0:
        print(f'  ✓ 成功获取 {len(etf_hist)} 条ETF历史数据')

        # 保存CSV
        csv_path = os.path.join(DATA_DIR, f'510050上证50ETF历史_{TIMESTAMP}.csv')
        etf_hist.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f'  ✓ 已保存: {csv_path}')

        # 绘制ETF走势图
        print(f'  绘制上证50ETF走势图...')
        close_col = '收盘' if '收盘' in etf_hist.columns else 'close'
        date_col = '日期' if '日期' in etf_hist.columns else 'date'

        etf_hist_sorted = etf_hist.sort_values(date_col).reset_index(drop=True)
        etf_hist_sorted['MA5'] = etf_hist_sorted[close_col].rolling(window=5).mean()
        etf_hist_sorted['MA20'] = etf_hist_sorted[close_col].rolling(window=20).mean()
        etf_hist_sorted['MA60'] = etf_hist_sorted[close_col].rolling(window=60).mean()

        dates_etf = pd.to_datetime(etf_hist_sorted[date_col])

        fig, ax = plt.subplots(figsize=(14, 7))
        fig.suptitle('上证50ETF (510050) 走势图', fontproperties=chinese_font_title, fontsize=16)

        ax.plot(dates_etf, etf_hist_sorted[close_col], label='收盘价', color='#333333', linewidth=1.5)
        ax.plot(dates_etf, etf_hist_sorted['MA5'], label='MA5', color='#FF6B6B', linestyle='--', linewidth=1)
        ax.plot(dates_etf, etf_hist_sorted['MA20'], label='MA20', color='#45B7D1', linestyle='--', linewidth=1)
        ax.plot(dates_etf, etf_hist_sorted['MA60'], label='MA60', color='#96CEB4', linestyle='--', linewidth=1)

        ax.set_ylabel('价格', fontproperties=chinese_font)
        ax.set_xlabel('日期', fontproperties=chinese_font)
        ax.legend(prop=chinese_font_small, loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        plt.tight_layout()
        save_fig(fig, f'510050上证50ETF走势_{TIMESTAMP}.png')
    else:
        print(f'  ✗ ETF历史数据获取失败 (两次接口均不可用)')
else:
    print('  ✗ 获取ETF市场数据失败')


# ============================================================
# 第五部分：基金持仓分析
# ============================================================
print_header('第五部分：基金持仓分析 (fund_portfolio_hold_em)')

holdings = safe_api_call(ak.fund_portfolio_hold_em, symbol='000001')
if holdings is not None:
    print(f'  ✓ 成功获取华夏成长混合(000001)持仓数据: {len(holdings)} 条')
    print(f'  列名: {list(holdings.columns)}')

    # 获取最新季度数据
    quarters = holdings['季度'].unique()
    latest_quarter = quarters[-1] if len(quarters) > 0 else None
    print(f'  所有季度: {list(quarters)}')
    print(f'  最新季度: {latest_quarter}')

    if latest_quarter:
        latest_holdings = holdings[holdings['季度'] == latest_quarter].copy()
        latest_holdings = latest_holdings.sort_values('占净值比例', ascending=False)

        print(f'\n  最新季度持仓TOP10:')
        print(f'  {"序号":<6} {"股票代码":<10} {"股票名称":<12} {"占净值比例(%)":<16} {"持仓市值(万)":<14}')
        print(f'  {"-"*58}')
        for _, r in latest_holdings.head(10).iterrows():
            print(f'  {r["序号"]:<6} {r["股票代码"]:<10} {str(r["股票名称"]):<12} '
                  f'{r["占净值比例"]:<16.2f} {r["持仓市值"]:<14.2f}')

        # 保存CSV
        csv_path = os.path.join(DATA_DIR, f'000001华夏成长持仓_{TIMESTAMP}.csv')
        holdings.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f'\n  ✓ 已保存: {csv_path}')

        # 绘制持仓饼图（TOP10）
        print(f'\n  绘制持仓TOP10饼图...')
        top10 = latest_holdings.head(10)
        labels = [str(n) for n in top10['股票名称']]
        sizes = top10['占净值比例'].values

        # 计算"其他"占净值比例
        other_pct = max(0, 100 - sizes.sum())

        # 准备饼图数据
        pie_labels = labels + ['其他'] if other_pct > 0 else labels
        pie_sizes = list(sizes) + [other_pct] if other_pct > 0 else list(sizes)

        # 颜色方案
        colors_pie = plt.cm.Set3(np.linspace(0, 1, len(pie_labels)))

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle(f'华夏成长混合 (000001) 最新持仓 TOP10\n{latest_quarter}',
                     fontproperties=chinese_font_title, fontsize=14)

        wedges, texts, autotexts = ax.pie(
            pie_sizes, labels=pie_labels, autopct='%1.1f%%',
            colors=colors_pie, startangle=90,
            textprops={'fontproperties': chinese_font_small}
        )
        # 改善小标签可读性
        for t in autotexts:
            t.set_fontsize(9)

        ax.axis('equal')
        plt.tight_layout()
        save_fig(fig, f'000001华夏成长持仓饼图_{TIMESTAMP}.png')

        # 绘制持仓占净值比例柱状图
        print(f'  绘制持仓比例柱状图...')
        top15 = latest_holdings.head(15)
        names_hold = [str(n)[:10] for n in top15['股票名称']]
        vals_hold = top15['占净值比例'].values

        fig, ax = plt.subplots(figsize=(12, 7))
        fig.suptitle(f'华夏成长混合 (000001) TOP15持仓占比\n{latest_quarter}',
                     fontproperties=chinese_font_title, fontsize=14)

        bars = ax.bar(names_hold, vals_hold, color='#45B7D1', alpha=0.8, edgecolor='white')
        ax.set_ylabel('占净值比例 (%)', fontproperties=chinese_font)
        ax.set_xlabel('股票名称', fontproperties=chinese_font)
        ax.set_xticklabels(names_hold, fontproperties=chinese_font_small, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')

        for bar, val in zip(bars, vals_hold):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'{val:.2f}%', ha='center', va='bottom', fontproperties=chinese_font_small)

        plt.tight_layout()
        save_fig(fig, f'000001华夏成长持仓柱状图_{TIMESTAMP}.png')
else:
    print('  ✗ 获取基金持仓数据失败')


# ============================================================
# 第六部分：基金管理人信息
# ============================================================
print_header('第六部分：基金管理人信息 (fund_manager_em)')

fund_mgrs = safe_api_call(ak.fund_manager_em)
if fund_mgrs is not None:
    print(f'  ✓ 成功获取 {len(fund_mgrs)} 位基金经理数据')
    print(f'  列名: {list(fund_mgrs.columns)}')

    # 按"现任基金资产总规模"排序（若存在）
    if '现任基金资产总规模' in fund_mgrs.columns:
        fund_mgrs['现任基金资产总规模'] = pd.to_numeric(
            fund_mgrs['现任基金资产总规模'], errors='coerce'
        )

        # 同一基金经理管理多只基金，按姓名去重后取最大规模
        mgr_dedup = fund_mgrs.sort_values('现任基金资产总规模', ascending=False)
        mgr_dedup = mgr_dedup.drop_duplicates(subset=['姓名', '所属公司'])

        top_mgrs = mgr_dedup.head(15)[
            ['姓名', '所属公司', '累计从业时间', '现任基金资产总规模', '现任基金最佳回报']
        ]
        print(f'\n  管理规模TOP15基金经理:')
        print(f'  {"姓名":<10} {"所属公司":<16} {"累计从业时间":<12} {"管理规模(亿)":<14} {"最佳回报":<10}')
        print(f'  {"-"*64}')
        for _, r in top_mgrs.iterrows():
            print(f'  {str(r["姓名"]):<10} {str(r["所属公司"])[:14]:<16} '
                  f'{str(r["累计从业时间"])[:10]:<12} {r["现任基金资产总规模"]:<14.2f} '
                  f'{str(r["现任基金最佳回报"])[:8]:<10}')

    # 按最佳回报排序
    if '现任基金最佳回报' in fund_mgrs.columns:
        fund_mgrs['最佳回报_numeric'] = pd.to_numeric(
            fund_mgrs['现任基金最佳回报'].astype(str).str.replace('%', '', regex=False),
            errors='coerce'
        )
        # 按姓名去重
        mgr_ret = fund_mgrs.sort_values('最佳回报_numeric', ascending=False)
        mgr_ret = mgr_ret.drop_duplicates(subset=['姓名', '所属公司'])

        top_return = mgr_ret.head(15)[
            ['姓名', '所属公司', '现任基金', '累计从业时间', '现任基金资产总规模', '现任基金最佳回报']
        ]
        print(f'\n  最佳回报TOP15基金经理:')
        print(f'  {"姓名":<10} {"所属公司":<16} {"累计从业时间":<12} {"管理规模(亿)":<14} {"最佳回报":<10}')
        print(f'  {"-"*64}')
        for _, r in top_return.iterrows():
            mgr_name = str(r['姓名'])[:8]
            company = str(r['所属公司'])[:14]
            exp = str(r['累计从业时间'])[:10]
            scale = r['现任基金资产总规模'] if pd.notna(r['现任基金资产总规模']) else 0
            try:
                scale_f = float(scale)
            except (ValueError, TypeError):
                scale_f = 0
            ret = str(r['现任基金最佳回报'])[:8]
            print(f'  {mgr_name:<10} {company:<16} {exp:<12} {scale_f:<14.2f} {ret:<10}')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'基金经理列表_{TIMESTAMP}.csv')
    fund_mgrs.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取基金经理数据失败')


# ============================================================
# 第七部分：基金评级与估值（补充数据）
# ============================================================
print_header('第七部分：基金评级与估值补充分析')

# 7.1 基金评级
print('\n  7.1 基金评级 (fund_rating_all)')
fund_ratings = safe_api_call(ak.fund_rating_all)
if fund_ratings is not None:
    print(f'  ✓ 成功获取 {len(fund_ratings)} 只基金评级数据')
    print(f'  列名: {list(fund_ratings.columns)}')

    # 显示五星基金
    if '5星评级家数' in fund_ratings.columns:
        fund_ratings['5星评级家数'] = pd.to_numeric(
            fund_ratings['5星评级家数'], errors='coerce'
        )
        five_star = fund_ratings[fund_ratings['5星评级家数'] >= 3].head(10)
        print(f'\n  多机构五星评级基金 (>=3家):')
        cols_show = [c for c in ['代码', '简称', '基金经理', '基金公司', '5星评级家数']
                     if c in five_star.columns]
        if len(cols_show) > 0 and len(five_star) > 0:
            print(f'  {five_star[cols_show].head(10).to_string(index=False)}')

    csv_path = os.path.join(DATA_DIR, f'基金评级_{TIMESTAMP}.csv')
    fund_ratings.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取基金评级失败')

# 7.2 基金估值
print('\n  7.2 基金实时估值 (fund_value_estimation_em)')
fund_est = safe_api_call(ak.fund_value_estimation_em)
if fund_est is not None:
    print(f'  ✓ 成功获取 {len(fund_est)} 只基金估值数据')
    print(f'  列名: {list(fund_est.columns)}')

    # 找估值增长率较高的基金
    growth_col = [c for c in fund_est.columns if '估算增长率' in c]
    if growth_col:
        gc = growth_col[0]
        fund_est[gc] = pd.to_numeric(fund_est[gc], errors='coerce')
        top_est = fund_est.nlargest(10, gc)[
            ['基金代码', '基金名称', gc] + [c for c in fund_est.columns if '估算值' in c][:1]
        ]
        print(f'\n  估算增长率TOP10:')
        for _, r in top_est.iterrows():
            est_val_col = [c for c in fund_est.columns if '估算值' in c]
            ev = r[est_val_col[0]] if est_val_col else ''
            print(f'    {r["基金代码"]} {str(r["基金名称"])[:20]:<22} '
                  f'增长率: {r[gc]:>6.2f}%  估值: {ev}')

    csv_path = os.path.join(DATA_DIR, f'基金估值_{TIMESTAMP}.csv')
    fund_est.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取基金估值失败')


# ============================================================
# 汇总报告
# ============================================================
print_header('基金数据研究完成')

print(f'  研究时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print(f'  数据文件目录: {DATA_DIR}')
print(f'  图表文件目录: {PLOT_DIR}')
print()

# 列出生成的CSV文件
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and TIMESTAMP in f]
print(f'  生成的CSV文件 ({len(csv_files)}个):')
for f in sorted(csv_files):
    fpath = os.path.join(DATA_DIR, f)
    size = os.path.getsize(fpath)
    print(f'    - {f} ({size/1024:.1f} KB)')

# 列出生成的PNG文件
png_files = [f for f in os.listdir(PLOT_DIR) if f.endswith('.png') and TIMESTAMP in f]
print(f'\n  生成的PNG图表 ({len(png_files)}个):')
for f in sorted(png_files):
    fpath = os.path.join(PLOT_DIR, f)
    size = os.path.getsize(fpath)
    print(f'    - {f} ({size/1024:.1f} KB)')

print()
print('=' * 70)
print('  研究完成！')
print('=' * 70)
