#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 上市公司基本面数据分析演示脚本 (阶段1.3)

功能：
1. 公司基本信息总览 - 深市行业分布
2. 财务指标分析 - ROE和EPS趋势
3. 财务摘要可视化 - 净利润趋势
4. 业绩报表分析 - EPS排名
5. 分红送配分析 - 分红历史
6. 全市场估值 - PE/PB分布概览

运行：./venv/bin/python scripts/s1.3_demo_fundamental.py
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

# ============================================================
# 中文字体设置（FontProperties）
# ============================================================
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
if os.path.exists(FONT_PATH):
    chinese_font = fm.FontProperties(fname=FONT_PATH, size=12)
    chinese_font_title = fm.FontProperties(fname=FONT_PATH, size=14)
    chinese_font_small = fm.FontProperties(fname=FONT_PATH, size=10)
    chinese_font_xs = fm.FontProperties(fname=FONT_PATH, size=8)
else:
    chinese_font = fm.FontProperties(size=12)
    chinese_font_title = fm.FontProperties(size=14)
    chinese_font_small = fm.FontProperties(size=10)
    chinese_font_xs = fm.FontProperties(size=8)

# ============================================================
# 输出目录
# ============================================================
BASE_DIR = '/home/neyo/workspace/code/study/akshare'
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DATA_DIR = os.path.join(OUTPUT_DIR, 'data', 'fundamental')
PLOT_DIR = os.path.join(OUTPUT_DIR, 'plots', 'fundamental')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

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
        print(f'  ⚠ 调用失败: {type(e).__name__}: {str(e)[:120]}')
        return None


def save_csv(df, filename):
    """保存DataFrame到CSV"""
    if df is None or len(df) == 0:
        print(f'  ⚠ 无数据可保存: {filename}')
        return None
    path = os.path.join(DATA_DIR, filename)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f'  ✓ CSV: {path}')
    return path


def save_fig(fig, filename):
    """保存图表"""
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  ✓ PNG: {path}')
    return path


# ============================================================
# 1. 公司基本信息总览：深市行业分布
# ============================================================
print_header('1. 公司基本信息总览 - 深市行业分布')

sz_df = safe_api_call(ak.stock_info_sz_name_code)

if sz_df is not None and len(sz_df) > 0:
    print(f'  ✓ 深市数据: {len(sz_df)} 条')
    print(f'  列名: {list(sz_df.columns)}')
    print(f'  前3行:')
    print(sz_df.head(3).to_string())

    # 保存原始数据
    save_csv(sz_df, f'深市公司列表_{TIMESTAMP}.csv')

    # 行业分布统计
    industry_col = None
    for col in sz_df.columns:
        if '行业' in col or 'INDUSTRY' in col.upper() or 'industry' in col.lower():
            industry_col = col
            break

    if industry_col:
        print(f'\n  行业列: {industry_col}')
        industry_counts = sz_df[industry_col].value_counts()
        print(f'  行业总数: {len(industry_counts)}')
        print(f'\n  行业分布（前15）:')
        for name, cnt in industry_counts.head(15).items():
            pct = cnt / len(sz_df) * 100
            print(f'    {name}: {cnt} 只 ({pct:.1f}%)')

        # 保存行业分布CSV
        industry_df = industry_counts.reset_index()
        industry_df.columns = ['行业', '公司数量']
        industry_df['占比%'] = round(industry_df['公司数量'] / len(sz_df) * 100, 2)
        save_csv(industry_df, f'深市行业分布_{TIMESTAMP}.csv')

        # 饼图：前10大行业 + 其他
        top_n = 10
        top_industries = industry_counts.head(top_n)
        others_count = industry_counts.iloc[top_n:].sum()
        if others_count > 0:
            top_industries = pd.concat([top_industries, pd.Series({'其他': others_count})])

        colors_pie = plt.cm.Set3(np.linspace(0, 1, len(top_industries)))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('深市上市公司行业分布', fontproperties=chinese_font_title, fontsize=16)

        # 饼图
        wedges, texts, autotexts = ax1.pie(
            top_industries.values,
            labels=None,
            autopct='%1.1f%%',
            colors=colors_pie,
            startangle=90,
            pctdistance=0.85
        )
        for t in autotexts:
            t.set_fontsize(9)
        ax1.legend(
            [f'{k} ({v}只)' for k, v in zip(top_industries.index, top_industries.values)],
            loc='center left',
            bbox_to_anchor=(1, 0.5),
            prop=chinese_font_small
        )
        ax1.set_title('行业占比', fontproperties=chinese_font)

        # 水平柱状图
        top15 = industry_counts.head(15).sort_values()
        colors_bar = plt.cm.Set2(np.linspace(0, 1, len(top15)))
        bars = ax2.barh(range(len(top15)), top15.values, color=colors_bar, alpha=0.85)
        ax2.set_yticks(range(len(top15)))
        ax2.set_yticklabels(top15.index, fontproperties=chinese_font_small)
        ax2.set_xlabel('公司数量（只）', fontproperties=chinese_font)
        ax2.set_title('前15大行业', fontproperties=chinese_font)
        ax2.grid(True, alpha=0.3, axis='x')

        for bar, val in zip(bars, top15.values):
            ax2.text(val + 5, bar.get_y() + bar.get_height() / 2,
                     str(val), va='center', fontproperties=chinese_font_small)

        plt.tight_layout()
        save_fig(fig, f'深市行业分布_{TIMESTAMP}.png')
    else:
        print('  未找到行业列，尝试使用板块分布')
        print(f'  全部列: {list(sz_df.columns)}')
else:
    print('  ✗ 获取深市数据失败')


# ============================================================
# 2. 财务指标分析：ROE和EPS趋势（平安银行）
# ============================================================
print_header('2. 财务指标分析 - ROE和EPS趋势（平安银行 000001）')

indicator = safe_api_call(ak.stock_financial_analysis_indicator,
                          symbol='000001', start_year='2023')

if indicator is not None and len(indicator) > 0:
    print(f'  ✓ 财务指标: {len(indicator)} 行, {len(indicator.columns)} 列')
    print(f'  列名: {list(indicator.columns)[:10]}...')
    print(indicator.head(3).to_string())

    save_csv(indicator, f'平安银行财务指标_{TIMESTAMP}.csv')

    # 尝试找到 ROE 和 EPS 相关列
    roe_col = None
    eps_col = None
    date_col = None

    for col in indicator.columns:
        col_lower = str(col).lower()
        if 'roe' in col_lower or '净资产收益率' in col or '加权净资产' in col:
            roe_col = col
        if 'eps' in col_lower or '每股收益' in col or '基本每股收益' in col:
            eps_col = col
        if 'date' in col_lower or '日期' in col or '报告期' in col or 'end_date' in col_lower or 'index' in col_lower:
            date_col = col

    print(f'    ROE列: {roe_col}')
    print(f'    EPS列: {eps_col}')
    print(f'    日期列: {date_col}')

    if roe_col and eps_col:
        # 尝试构建日期
        plot_df = indicator.copy()
        if date_col:
            plot_df['date'] = pd.to_datetime(plot_df[date_col], errors='coerce')
        else:
            plot_df['date'] = range(len(plot_df))

        plot_df = plot_df.dropna(subset=[roe_col, eps_col])
        plot_df = plot_df.sort_values('date')

        # 数值化
        plot_df[roe_col] = pd.to_numeric(plot_df[roe_col], errors='coerce')
        plot_df[eps_col] = pd.to_numeric(plot_df[eps_col], errors='coerce')
        plot_df = plot_df.dropna(subset=[roe_col, eps_col])

        if len(plot_df) > 0:
            print(f'\n  ROE和EPS趋势（{len(plot_df)}期）:')
            for _, row in plot_df.iterrows():
                d = row.get('date', '').strftime('%Y-%m-%d') if hasattr(row.get('date', ''), 'strftime') else str(row.get('date', ''))
                print(f'    {d}: ROE={row[roe_col]:.2f}%, EPS={row[eps_col]:.4f}')

            # 绘制双轴图
            fig, ax1 = plt.subplots(figsize=(14, 7))
            fig.suptitle('平安银行（000001）ROE与EPS趋势', fontproperties=chinese_font_title, fontsize=16)

            dates = plot_df['date'] if isinstance(plot_df['date'].iloc[0], pd.Timestamp) else range(len(plot_df))
            x_labels = [d.strftime('%Y-%m') if hasattr(d, 'strftime') else str(d) for d in plot_df['date']]

            color_roe = '#E74C3C'
            color_eps = '#2980B9'

            line_roe = ax1.plot(dates, plot_df[roe_col], color=color_roe, marker='o',
                                linewidth=2, markersize=6, label=f'ROE (%)')
            ax1.set_ylabel('ROE (%)', fontproperties=chinese_font, color=color_roe)
            ax1.tick_params(axis='y', labelcolor=color_roe)
            ax1.grid(True, alpha=0.3)

            ax2 = ax1.twinx()
            line_eps = ax2.plot(dates, plot_df[eps_col], color=color_eps, marker='s',
                                linewidth=2, markersize=6, label=f'EPS (元)')
            ax2.set_ylabel('EPS (元)', fontproperties=chinese_font, color=color_eps)
            ax2.tick_params(axis='y', labelcolor=color_eps)

            # 设置x轴标签
            if isinstance(plot_df['date'].iloc[0], pd.Timestamp):
                step = max(1, len(dates) // 8)
                ax1.set_xticks(dates[::step])
                ax1.set_xticklabels([d.strftime('%Y-%m') for d in dates[::step]],
                                    fontproperties=chinese_font_small, rotation=45)
            else:
                ax1.set_xlabel('期数', fontproperties=chinese_font)

            lines = line_roe + line_eps
            labels = [l.get_label() for l in lines]
            ax1.legend(lines, labels, loc='upper left', prop=chinese_font_small)

            plt.title('', fontproperties=chinese_font)  # placeholder
            plt.tight_layout()
            save_fig(fig, f'平安银行ROE_EPS趋势_{TIMESTAMP}.png')
        else:
            print('  ⚠ 数值化后无有效数据')
    else:
        print(f'  未找到ROE/EPS列，可用列: {list(indicator.columns)}')
else:
    print('  ✗ 获取财务指标失败')


# ============================================================
# 3. 财务摘要可视化：净利润趋势（平安银行）
# ============================================================
print_header('3. 财务摘要可视化 - 净利润趋势（平安银行 000001）')

abstract = safe_api_call(ak.stock_financial_abstract_ths, symbol='000001')

if abstract is not None and len(abstract) > 0:
    print(f'  ✓ 财务摘要: {len(abstract)} 行, {len(abstract.columns)} 列')
    print(f'  列名: {list(abstract.columns)[:10]}...')
    print(abstract.head(5).to_string())

    save_csv(abstract, f'平安银行财务摘要_{TIMESTAMP}.csv')

    # 查找净利润和日期列
    profit_col = None
    date_col = None

    # 尝试常见的净利润列名
    profit_keywords = ['净利润', '归属于母公司', '归母净利润', 'net_profit', 'profit']
    date_keywords = ['date', '日期', '报告期', 'end_date', 'index']

    for col in abstract.columns:
        col_str = str(col)
        for kw in profit_keywords:
            if kw in col_str:
                profit_col = col
                break
        for kw in date_keywords:
            if kw in col_str.lower():
                date_col = col
                break

    if not profit_col:
        # 尝试数值列，找第一个看起来像净利润的
        for col in abstract.columns:
            if abstract[col].dtype in ['float64', 'int64']:
                vals = pd.to_numeric(abstract[col], errors='coerce').dropna()
                if len(vals) > 0 and vals.abs().max() > 1e6:  # 大数值通常是财务数据
                    profit_col = col
                    break

    print(f'    净利润列: {profit_col}')
    print(f'    日期列: {date_col}')

    if profit_col:
        plot_df = abstract.copy()
        if date_col:
            plot_df['date'] = pd.to_datetime(plot_df[date_col], errors='coerce')
        else:
            plot_df['date'] = range(len(plot_df))

        plot_df['profit'] = pd.to_numeric(plot_df[profit_col], errors='coerce')
        plot_df = plot_df.dropna(subset=['profit'])
        plot_df = plot_df.sort_values('date')

        # 取前20条（最近的报告期）
        plot_df = plot_df.tail(20)

        if len(plot_df) > 0:
            print(f'\n  净利润趋势（最近{len(plot_df)}期）:')
            for _, row in plot_df.iterrows():
                d = row.get('date', '')
                d_str = d.strftime('%Y-%m-%d') if hasattr(d, 'strftime') else str(d)
                profit_val = row['profit'] / 1e8  # 转为亿元
                print(f'    {d_str}: {profit_val:.2f} 亿元')

            # 绘制净利润柱状图
            fig, ax = plt.subplots(figsize=(14, 7))
            fig.suptitle('平安银行（000001）净利润趋势', fontproperties=chinese_font_title, fontsize=16)

            dates = plot_df['date']
            profits = plot_df['profit'] / 1e8  # 转为亿元

            colors_bar = ['#2ECC71' if v >= 0 else '#E74C3C' for v in profits]
            bars = ax.bar(range(len(dates)), profits.values, color=colors_bar, alpha=0.85, width=0.6)

            ax.set_xticks(range(len(dates)))
            if hasattr(dates.iloc[0], 'strftime'):
                ax.set_xticklabels([d.strftime('%Y-%m') for d in dates],
                                   fontproperties=chinese_font_small, rotation=45)
            else:
                ax.set_xticklabels([str(d) for d in dates],
                                   fontproperties=chinese_font_small, rotation=45)
            ax.set_ylabel('净利润（亿元）', fontproperties=chinese_font)
            ax.grid(True, alpha=0.3, axis='y')

            # 在柱子上标注数值
            for bar, val in zip(bars, profits):
                y_pos = bar.get_height() if val >= 0 else bar.get_height()
                va = 'bottom' if val >= 0 else 'top'
                ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                        f'{val:.1f}', ha='center', va=va,
                        fontproperties=chinese_font_xs,
                        color='#333333')

            plt.tight_layout()
            save_fig(fig, f'平安银行净利润趋势_{TIMESTAMP}.png')
        else:
            print('  ⚠ 无有效净利润数据')
    else:
        print(f'  ⚠ 未找到净利润列，可用列: {list(abstract.columns)}')
else:
    print('  ✗ 获取财务摘要失败')


# ============================================================
# 4. 业绩报表分析：EPS排名
# ============================================================
print_header('4. 业绩报表分析 - EPS排名')

yjbb = safe_api_call(ak.stock_yjbb_em)

if yjbb is not None and len(yjbb) > 0:
    print(f'  ✓ 业绩报表: {len(yjbb)} 行, {len(yjbb.columns)} 列')
    print(f'  列名: {list(yjbb.columns)[:12]}...')
    print(yjbb.head(3).to_string())

    save_csv(yjbb, f'全市场业绩报表_{TIMESTAMP}.csv')

    # 查找EPS列和股票代码/名称列
    eps_col = None
    name_col = None
    code_col = None

    for col in yjbb.columns:
        col_str = str(col)
        if '每股收益' in col_str or 'eps' in col_str.lower():
            eps_col = col
        if '名称' in col_str or '股票简称' in col_str or 'name' in col_str.lower():
            name_col = col
        if '代码' in col_str or '股票代码' in col_str or 'code' in col_str.lower():
            code_col = col

    print(f'    EPS列: {eps_col}')
    print(f'    名称列: {name_col}')
    print(f'    代码列: {code_col}')

    if eps_col and name_col:
        yjbb['eps_num'] = pd.to_numeric(yjbb[eps_col], errors='coerce')
        yjbb_valid = yjbb.dropna(subset=['eps_num'])

        if len(yjbb_valid) > 0:
            # TOP 10 EPS
            top_eps = yjbb_valid.nlargest(10, 'eps_num')
            # BOTTOM 10 EPS
            bottom_eps = yjbb_valid.nsmallest(10, 'eps_num')

            print(f'\n  EPS排名前10:')
            for _, row in top_eps.iterrows():
                print(f'    {row[name_col]} ({row.get(code_col, "")}): EPS={row["eps_num"]:.4f}')

            print(f'\n  EPS排名后10:')
            for _, row in bottom_eps.iterrows():
                print(f'    {row[name_col]} ({row.get(code_col, "")}): EPS={row["eps_num"]:.4f}')

            # 保存排名数据
            top_eps_out = top_eps[[c for c in [name_col, code_col, eps_col] if c in top_eps.columns]].copy()
            top_eps_out = top_eps_out.rename(columns={eps_col: '基本每股收益'})
            save_csv(top_eps_out, f'EPS排名前10_{TIMESTAMP}.csv')

            bottom_eps_out = bottom_eps[[c for c in [name_col, code_col, eps_col] if c in bottom_eps.columns]].copy()
            bottom_eps_out = bottom_eps_out.rename(columns={eps_col: '基本每股收益'})
            save_csv(bottom_eps_out, f'EPS排名后10_{TIMESTAMP}.csv')

            # 绘制EPS排名柱状图
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
            fig.suptitle('全市场业绩报表 - EPS排行', fontproperties=chinese_font_title, fontsize=16)

            # TOP 10
            top_data = top_eps.head(10)
            top_names = [str(n)[:10] for n in top_data[name_col]]
            top_vals = top_data['eps_num'].values
            colors_top = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_names)))
            bars1 = ax1.barh(range(len(top_names)), top_vals, color=colors_top[::-1], alpha=0.85)
            ax1.set_yticks(range(len(top_names)))
            ax1.set_yticklabels(top_names, fontproperties=chinese_font_small)
            ax1.set_xlabel('基本每股收益', fontproperties=chinese_font)
            ax1.set_title('EPS前10', fontproperties=chinese_font)
            ax1.grid(True, alpha=0.3, axis='x')
            for bar, val in zip(bars1, top_vals):
                ax1.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                         f'{val:.4f}', va='center', fontproperties=chinese_font_xs)

            # BOTTOM 10
            bottom_data = bottom_eps.head(10)
            bottom_names = [str(n)[:10] for n in bottom_data[name_col]]
            bottom_vals = bottom_data['eps_num'].values
            colors_bottom = plt.cm.Reds(np.linspace(0.9, 0.4, len(bottom_names)))
            bars2 = ax2.barh(range(len(bottom_names)), bottom_vals, color=colors_bottom[::-1], alpha=0.85)
            ax2.set_yticks(range(len(bottom_names)))
            ax2.set_yticklabels(bottom_names, fontproperties=chinese_font_small)
            ax2.set_xlabel('基本每股收益', fontproperties=chinese_font)
            ax2.set_title('EPS后10', fontproperties=chinese_font)
            ax2.grid(True, alpha=0.3, axis='x')
            for bar, val in zip(bars2, bottom_vals):
                ax2.text(val - 0.3 if val < 0 else val + 0.01,
                         bar.get_y() + bar.get_height()/2,
                         f'{val:.4f}', va='center', fontproperties=chinese_font_xs)

            plt.tight_layout()
            save_fig(fig, f'EPS排名_{TIMESTAMP}.png')

            # EPS分布直方图
            fig, ax = plt.subplots(figsize=(14, 6))
            fig.suptitle('全市场EPS分布', fontproperties=chinese_font_title, fontsize=16)

            eps_valid = yjbb_valid['eps_num'].dropna()
            eps_valid = eps_valid[eps_valid.abs() < 10]  # 剔除极端值
            ax.hist(eps_valid, bins=80, color='#3498DB', alpha=0.8, edgecolor='white', linewidth=0.5)
            ax.axvline(x=0, color='red', linestyle='--', linewidth=1, label='盈亏线')
            ax.set_xlabel('基本每股收益', fontproperties=chinese_font)
            ax.set_ylabel('公司数量', fontproperties=chinese_font)
            ax.legend(prop=chinese_font_small)
            ax.grid(True, alpha=0.3, axis='y')

            mean_eps = eps_valid.mean()
            median_eps = eps_valid.median()
            ax.axvline(x=mean_eps, color='green', linestyle=':', linewidth=1.5, label=f'均值={mean_eps:.3f}')
            ax.axvline(x=median_eps, color='orange', linestyle=':', linewidth=1.5, label=f'中位数={median_eps:.3f}')
            ax.legend(prop=chinese_font_small)

            plt.tight_layout()
            save_fig(fig, f'EPS分布_{TIMESTAMP}.png')

            print(f'\n  EPS统计:')
            print(f'    均值: {mean_eps:.4f}')
            print(f'    中位数: {median_eps:.4f}')
            print(f'    盈利公司: {(eps_valid > 0).sum()} / {len(eps_valid)} ({(eps_valid > 0).mean()*100:.1f}%)')
            print(f'    亏损公司: {(eps_valid < 0).sum()} / {len(eps_valid)} ({(eps_valid < 0).mean()*100:.1f}%)')
        else:
            print('  ⚠ 无有效EPS数值')
    else:
        print(f'  未找到EPS/名称列, 全部列名: {list(yjbb.columns)}')
else:
    print('  ✗ 获取业绩报表失败')


# ============================================================
# 5. 分红送配分析：平安银行分红历史
# ============================================================
print_header('5. 分红送配分析 - 平安银行（000001）分红历史')

fhps = safe_api_call(ak.stock_fhps_detail_em, symbol='000001')

if fhps is not None and len(fhps) > 0:
    print(f'  ✓ 分红送配: {len(fhps)} 行, {len(fhps.columns)} 列')
    print(f'  列名: {list(fhps.columns)}')
    print(fhps.head(5).to_string())

    save_csv(fhps, f'平安银行分红送配_{TIMESTAMP}.csv')

    # 查找分红相关列
    date_col = None
    dividend_col = None
    stock_col = None  # 送转股

    for col in fhps.columns:
        col_str = str(col)
        if '日期' in col_str or '股权登记' in col_str or 'date' in col_str.lower():
            date_col = col
        if '分红' in col_str or '派息' in col_str or '股息' in col_str or '现金' in col_str:
            dividend_col = col
        if '送转' in col_str or '转增' in col_str:
            stock_col = col

    print(f'    日期列: {date_col}')
    print(f'    分红列: {dividend_col}')
    print(f'    送转列: {stock_col}')

    if dividend_col:
        plot_df = fhps.copy()
        if date_col:
            plot_df['date'] = pd.to_datetime(plot_df[date_col], errors='coerce')
        else:
            plot_df['date'] = range(len(plot_df))

        plot_df['dividend'] = pd.to_numeric(plot_df[dividend_col], errors='coerce')
        plot_df = plot_df.dropna(subset=['dividend'])
        plot_df = plot_df.sort_values('date')

        if len(plot_df) > 0:
            print(f'\n  分红历史（{len(plot_df)}期）:')
            for _, row in plot_df.iterrows():
                d = row.get('date', '')
                d_str = d.strftime('%Y-%m-%d') if hasattr(d, 'strftime') else str(d)
                print(f'    {d_str}: 每10股派 {row["dividend"]:.4f} 元')

            # 绘制分红柱状图
            fig, ax = plt.subplots(figsize=(14, 7))
            fig.suptitle('平安银行（000001）分红历史', fontproperties=chinese_font_title, fontsize=16)

            dates = plot_df['date']
            dividends = plot_df['dividend'].values

            colors_bar = ['#27AE60' if v >= 0 else '#E74C3C' for v in dividends]
            bars = ax.bar(range(len(dates)), dividends, color=colors_bar, alpha=0.85, width=0.6)

            ax.set_xticks(range(len(dates)))
            if hasattr(dates.iloc[0], 'strftime'):
                ax.set_xticklabels([d.strftime('%Y-%m') for d in dates],
                                   fontproperties=chinese_font_small, rotation=45)
            else:
                ax.set_xticklabels([str(d) for d in dates],
                                   fontproperties=chinese_font_small, rotation=45)
            ax.set_ylabel('每10股派息（元）', fontproperties=chinese_font)
            ax.grid(True, alpha=0.3, axis='y')

            for bar, val in zip(bars, dividends):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                        f'{val:.2f}', ha='center', va='bottom',
                        fontproperties=chinese_font_xs)

            plt.tight_layout()
            save_fig(fig, f'平安银行分红历史_{TIMESTAMP}.png')
        else:
            print('  ⚠ 无有效分红数据')
    else:
        print(f'  未找到分红列, 全部列: {list(fhps.columns)}')
else:
    print('  ✗ 获取分红送配失败')


# ============================================================
# 6. 全市场估值：PE(TTM)和PB分布
# ============================================================
print_header('6. 全市场估值概览 - PE(TTM)和PB分布')

# 6.1 PE(TTM)
ttm_df = safe_api_call(ak.stock_a_ttm_lyr)

# 6.2 PB
pb_df = safe_api_call(ak.stock_a_all_pb)

if ttm_df is not None and len(ttm_df) > 0:
    print(f'  ✓ PE(TTM)数据: {len(ttm_df)} 行, {len(ttm_df.columns)} 列')
    print(f'  列名: {list(ttm_df.columns)[:10]}...')
    print(ttm_df.head(3).to_string())
    save_csv(ttm_df, f'全市场PE_{TIMESTAMP}.csv')

if pb_df is not None and len(pb_df) > 0:
    print(f'  ✓ PB数据: {len(pb_df)} 行, {len(pb_df.columns)} 列')
    print(f'  列名: {list(pb_df.columns)[:10]}...')
    print(pb_df.head(3).to_string())
    save_csv(pb_df, f'全市场PB_{TIMESTAMP}.csv')

# 绘制PE分布
if ttm_df is not None and len(ttm_df) > 0:
    # 找寻PE列
    pe_col = None
    name_col_pe = None
    for col in ttm_df.columns:
        col_str = str(col).lower()
        if 'pe' in col_str or '市盈率' in col_str or 'ttm' in col_str:
            pe_col = col
        if '名称' in col_str or 'name' in col_str:
            name_col_pe = col

    print(f'  PE列: {pe_col}')

    if pe_col:
        ttm_df['pe_value'] = pd.to_numeric(ttm_df[pe_col], errors='coerce')
        pe_valid = ttm_df['pe_value'].dropna()

        # 过滤合理范围 PE: 0~200
        pe_filtered = pe_valid[(pe_valid > 0) & (pe_valid <= 200)]

        if len(pe_filtered) > 0:
            # PE分布统计
            pe_ranges = [
                ('0~10倍', (pe_filtered >= 0) & (pe_filtered <= 10)),
                ('10~20倍', (pe_filtered > 10) & (pe_filtered <= 20)),
                ('20~30倍', (pe_filtered > 20) & (pe_filtered <= 30)),
                ('30~50倍', (pe_filtered > 30) & (pe_filtered <= 50)),
                ('50~100倍', (pe_filtered > 50) & (pe_filtered <= 100)),
                ('100~200倍', (pe_filtered > 100) & (pe_filtered <= 200)),
            ]

            print(f'\n  PE(TTM)分布（剔除负值）:')
            pe_stats = {}
            for label, cond in pe_ranges:
                count = cond.sum()
                pct = count / len(pe_filtered) * 100
                pe_stats[label] = count
                print(f'    {label}: {count} 只 ({pct:.1f}%)')

            print(f'  PE统计: 均值={pe_filtered.mean():.2f}, 中位数={pe_filtered.median():.2f}')
            print(f'  负PE（亏损）: {(pe_valid <= 0).sum()} 只')
else:
    print('  ⚠ PE数据不可用')

# 绘制PB分布
if pb_df is not None and len(pb_df) > 0:
    pb_col = None
    for col in pb_df.columns:
        col_str = str(col).lower()
        if 'pb' in col_str or '市净率' in col_str:
            pb_col = col
            break

    print(f'  PB列: {pb_col}')

    if pb_col:
        pb_df['pb_value'] = pd.to_numeric(pb_df[pb_col], errors='coerce')
        pb_valid = pb_df['pb_value'].dropna()

        # 过滤合理范围
        pb_filtered = pb_valid[(pb_valid > 0) & (pb_valid <= 20)]

        if len(pb_filtered) > 0:
            pb_ranges = [
                ('0~1倍（破净）', (pb_filtered > 0) & (pb_filtered <= 1)),
                ('1~2倍', (pb_filtered > 1) & (pb_filtered <= 2)),
                ('2~3倍', (pb_filtered > 2) & (pb_filtered <= 3)),
                ('3~5倍', (pb_filtered > 3) & (pb_filtered <= 5)),
                ('5~10倍', (pb_filtered > 5) & (pb_filtered <= 10)),
                ('10~20倍', (pb_filtered > 10) & (pb_filtered <= 20)),
            ]

            print(f'\n  PB分布（剔除负值）:')
            pb_stats = {}
            for label, cond in pb_ranges:
                count = cond.sum()
                pct = count / len(pb_filtered) * 100
                pb_stats[label] = count
                print(f'    {label}: {count} 只 ({pct:.1f}%)')

            print(f'  PB统计: 均值={pb_filtered.mean():.2f}, 中位数={pb_filtered.median():.2f}')
            print(f'  破净公司: {(pb_filtered <= 1).sum()} 只 ({(pb_filtered <= 1).mean()*100:.1f}%)')
            print(f'  负PB: {(pb_valid <= 0).sum()} 只')
else:
    print('  ⚠ PB数据不可用')

# 联合PE/PB分布图
if ttm_df is not None and len(ttm_df) > 0 and pb_df is not None and len(pb_df) > 0:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('全市场估值分布', fontproperties=chinese_font_title, fontsize=16)

    # PE分布直方图
    pe_vals = pe_filtered if 'pe_filtered' in dir() and len(pe_filtered) > 0 else None
    if pe_vals is not None and len(pe_vals) > 0:
        ax1.hist(pe_vals, bins=60, color='#3498DB', alpha=0.8, edgecolor='white', linewidth=0.5)
        ax1.axvline(x=pe_vals.median(), color='#E74C3C', linestyle='--', linewidth=2,
                    label=f'中位数={pe_vals.median():.1f}')
        ax1.axvline(x=pe_vals.mean(), color='#2ECC71', linestyle=':', linewidth=2,
                    label=f'均值={pe_vals.mean():.1f}')
        ax1.set_xlabel('PE(TTM)', fontproperties=chinese_font)
        ax1.set_ylabel('公司数量', fontproperties=chinese_font)
        ax1.set_title('PE(TTM)分布（0~200倍）', fontproperties=chinese_font)
        ax1.legend(prop=chinese_font_small)
        ax1.grid(True, alpha=0.3, axis='y')

    # PB分布直方图
    pb_vals = pb_filtered if 'pb_filtered' in dir() and len(pb_filtered) > 0 else None
    if pb_vals is not None and len(pb_vals) > 0:
        ax2.hist(pb_vals, bins=60, color='#E67E22', alpha=0.8, edgecolor='white', linewidth=0.5)
        ax2.axvline(x=pb_vals.median(), color='#E74C3C', linestyle='--', linewidth=2,
                    label=f'中位数={pb_vals.median():.2f}')
        ax2.axvline(x=pb_vals.mean(), color='#2ECC71', linestyle=':', linewidth=2,
                    label=f'均值={pb_vals.mean():.2f}')
        ax2.axvline(x=1, color='#9B59B6', linestyle='-.', linewidth=1.5,
                    label='破净线(PB=1)')
        ax2.set_xlabel('PB', fontproperties=chinese_font)
        ax2.set_ylabel('公司数量', fontproperties=chinese_font)
        ax2.set_title('PB分布（0~20倍）', fontproperties=chinese_font)
        ax2.legend(prop=chinese_font_small)
        ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    save_fig(fig, f'全市场估值分布_{TIMESTAMP}.png')

    # PE vs PB 散点图（双坐标）
    print('\n  绘制PE/PB联合散点图...')
    try:
        # 尝试合并PE和PB数据
        pe_merged = ttm_df[['pe_value']].copy()
        pb_merged = pb_df[['pb_value']].copy()

        # 使用索引对齐（两个数据集长度接近）
        min_len = min(len(pe_merged), len(pb_merged))
        if min_len > 100:
            pe_vals_s = pe_merged['pe_value'].values[:min_len]
            pb_vals_s = pb_merged['pb_value'].values[:min_len]

            valid_mask = (pe_vals_s > 0) & (pe_vals_s <= 100) & (pb_vals_s > 0) & (pb_vals_s <= 15)
            pe_plot = pe_vals_s[valid_mask]
            pb_plot = pb_vals_s[valid_mask]

            if len(pe_plot) > 100:
                fig, ax = plt.subplots(figsize=(12, 8))
                fig.suptitle('全市场PE(TTM) vs PB 散点图', fontproperties=chinese_font_title, fontsize=16)

                scatter = ax.scatter(pe_plot, pb_plot, c=pe_plot, cmap='viridis',
                                     alpha=0.4, s=8, edgecolors='none')
                ax.set_xlabel('PE(TTM)', fontproperties=chinese_font)
                ax.set_ylabel('PB', fontproperties=chinese_font)
                ax.axhline(y=1, color='#E74C3C', linestyle='--', alpha=0.7, linewidth=1.5, label='PB=1(破净线)')
                ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
                ax.grid(True, alpha=0.2)
                cbar = plt.colorbar(scatter, ax=ax)
                cbar.set_label('PE(TTM)', fontproperties=chinese_font_small)
                ax.legend(prop=chinese_font_small)

                plt.tight_layout()
                save_fig(fig, f'全市场PE_PB散点图_{TIMESTAMP}.png')
    except Exception as e:
        print(f'  ⚠ 散点图绘制失败: {e}')


# ============================================================
# 总结
# ============================================================
print_header('分析完成')

print(f'  数据目录: {DATA_DIR}')
print(f'  图表目录: {PLOT_DIR}')
print(f'  生成CSV文件: {len(os.listdir(DATA_DIR))} 个')
print(f'  生成PNG图表: {len(os.listdir(PLOT_DIR))} 个')
print()

# 列出所有生成的文件
print('  CSV文件列表:')
for f in sorted(os.listdir(DATA_DIR)):
    fpath = os.path.join(DATA_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f'    {f} ({size_kb:.1f} KB)')

print()
print('  PNG文件列表:')
for f in sorted(os.listdir(PLOT_DIR)):
    fpath = os.path.join(PLOT_DIR, f)
    size_kb = os.path.getsize(fpath) / 1024
    print(f'    {f} ({size_kb:.1f} KB)')

print()
print(f'  完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('=' * 70)
