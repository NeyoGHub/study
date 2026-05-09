#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AkShare 债券数据综合示例 (阶段2.2)

功能：
1. 国债收益率曲线 - bond_china_yield()
2. 中美收益率对比 - bond_zh_us_rate()
3. 债券指数走势 - bond_treasury_index_cbond() + bond_composite_index_cbond()
4. 可转债市场 - bond_cb_jsl()
5. 可转债行情 - bond_zh_hs_cov_spot()
6. 中国国债期货 - bond_gb_zh_sina() + bond_gb_us_sina()

运行：./venv/bin/python scripts/s2.2_demo_bond.py
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
DATA_DIR = os.path.join(OUTPUT_DIR, 'data', 'bond')
PLOT_DIR = os.path.join(OUTPUT_DIR, 'plots', 'bond')
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
# 第一部分：国债收益率曲线
# ============================================================
print_header('第一部分：国债收益率曲线 (bond_china_yield)')

china_yield = safe_api_call(ak.bond_china_yield)
if china_yield is not None:
    print(f'  ✓ 成功获取: {len(china_yield)} 条数据')
    print(f'  列名: {list(china_yield.columns)}')

    # 提取"中债国债收益率曲线"行
    yield_curve_row = None
    for col in china_yield.columns:
        if '曲线名称' in str(col) or 'curve' in str(col).lower():
            curve_name_col = col
            break
    else:
        # 尝试第一列作为曲线名称
        curve_name_col = china_yield.columns[0]

    cn_label = '中债国债收益率曲线'
    mask = china_yield[curve_name_col].astype(str).str.contains(cn_label)
    if mask.any():
        yield_curve_row = china_yield[mask].iloc[-1]  # 最新一期
        print(f'  ✓ 找到"{cn_label}"行 (最新日期: {yield_curve_row.iloc[0]})')
    else:
        # 如果没有找到，取最后一行
        print(f'  未找到"{cn_label}"，使用最后一行数据')
        yield_curve_row = china_yield.iloc[-1]

    # 提取收益率曲线的maturities
    maturity_map = {
        '3月': '3M', '6月': '6M', '1年': '1Y', '3年': '3Y',
        '5年': '5Y', '7年': '7Y', '10年': '10Y', '30年': '30Y'
    }

    curve_data = {}
    for cn_name, en_name in maturity_map.items():
        if cn_name in china_yield.columns:
            try:
                val = pd.to_numeric(yield_curve_row[cn_name], errors='coerce')
                curve_data[en_name] = val
            except (ValueError, TypeError):
                curve_data[en_name] = None

    print(f'\n  国债收益率曲线 (最新):')
    print(f'  {"期限":<8} {"收益率(%)":<12}')
    print(f'  {"-"*20}')
    for maturity in ['3M', '6M', '1Y', '3Y', '5Y', '7Y', '10Y', '30Y']:
        val = curve_data.get(maturity)
        if val is not None and not np.isnan(val):
            print(f'  {maturity:<8} {val:<12.4f}')
        else:
            print(f'  {maturity:<8} {"N/A":<12}')

    # 绘制收益率曲线
    print(f'\n  绘制国债收益率曲线图...')
    maturities_display = ['3M', '6M', '1Y', '3Y', '5Y', '7Y', '10Y', '30Y']
    yields_plot = []
    labels_plot = []
    for m in maturities_display:
        v = curve_data.get(m)
        if v is not None and not np.isnan(v):
            yields_plot.append(v)
            labels_plot.append(m)

    if len(yields_plot) >= 3:
        fig, ax1 = plt.subplots(figsize=(12, 7))
        fig.suptitle('中债国债收益率曲线', fontproperties=chinese_font_title, fontsize=16)

        x_pos = range(len(labels_plot))
        ax1.plot(x_pos, yields_plot, marker='o', color='#E74C3C', linewidth=2.5,
                 markersize=10, markerfacecolor='white', markeredgecolor='#E74C3C',
                 markeredgewidth=2, label='收益率')
        ax1.fill_between(x_pos, yields_plot, alpha=0.15, color='#E74C3C')

        for i, v in enumerate(yields_plot):
            ax1.annotate(f'{v:.2f}%', (i, v),
                        textcoords='offset points', xytext=(0, 15),
                        ha='center', fontproperties=chinese_font_small,
                        color='#C0392B', fontweight='bold')

        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(labels_plot, fontproperties=chinese_font)
        ax1.set_ylabel('收益率 (%)', fontproperties=chinese_font)
        ax1.set_xlabel('期限', fontproperties=chinese_font)
        ax1.grid(True, alpha=0.3)
        ax1.legend(prop=chinese_font_small, loc='upper left')

        plt.tight_layout()
        save_fig(fig, f'国债收益率曲线_{TIMESTAMP}.png')
    else:
        print(f'  ⚠ 收益率数据不足，无法绘图')

    # 保存完整数据到CSV
    csv_path = os.path.join(DATA_DIR, f'国债收益率曲线_{TIMESTAMP}.csv')
    china_yield.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取国债收益率数据失败')


# ============================================================
# 第二部分：中美收益率对比
# ============================================================
print_header('第二部分：中美收益率对比 (bond_zh_us_rate)')

cn_us_rate = safe_api_call(ak.bond_zh_us_rate)
if cn_us_rate is not None:
    print(f'  ✓ 成功获取: {len(cn_us_rate)} 条数据')
    print(f'  列名: {list(cn_us_rate.columns)}')

    # 尝试确定日期列和收益率列
    date_col = '日期' if '日期' in cn_us_rate.columns else cn_us_rate.columns[0]
    cn_col = None
    us_col = None
    for c in cn_us_rate.columns:
        c_str = str(c)
        if '中国' in c_str:
            cn_col = c
        if '美国' in c_str:
            us_col = c

    if cn_col and us_col:
        # 转换为数值
        cn_us_rate[cn_col] = pd.to_numeric(cn_us_rate[cn_col], errors='coerce')
        cn_us_rate[us_col] = pd.to_numeric(cn_us_rate[us_col], errors='coerce')
        cn_us_rate[date_col] = pd.to_datetime(cn_us_rate[date_col], errors='coerce')

        df_sorted = cn_us_rate.sort_values(date_col).dropna(subset=[cn_col, us_col])
        print(f'  日期范围: {df_sorted[date_col].iloc[0].strftime("%Y-%m-%d")} ~ {df_sorted[date_col].iloc[-1].strftime("%Y-%m-%d")}')
        print(f'  最新中国10Y: {df_sorted[cn_col].iloc[-1]:.4f}%')
        print(f'  最新美国10Y: {df_sorted[us_col].iloc[-1]:.4f}%')
        spread = df_sorted[cn_col].iloc[-1] - df_sorted[us_col].iloc[-1]
        print(f'  中美利差: {spread:.4f}%')

        # 只取最近3年数据绘图
        three_years_ago = datetime.now() - timedelta(days=3*365)
        df_recent = df_sorted[df_sorted[date_col] >= three_years_ago].copy()

        if len(df_recent) > 10:
            print(f'\n  绘制中美收益率对比图 (近3年)...')
            dates = df_recent[date_col]

            fig, ax1 = plt.subplots(figsize=(14, 7))
            fig.suptitle('中美10年期国债收益率对比', fontproperties=chinese_font_title, fontsize=16)

            line1, = ax1.plot(dates, df_recent[cn_col], label=f'{cn_col}',
                             color='#E74C3C', linewidth=2)
            line2, = ax1.plot(dates, df_recent[us_col], label=f'{us_col}',
                             color='#2980B9', linewidth=2)

            ax1.set_ylabel('收益率 (%)', fontproperties=chinese_font)
            ax1.legend(handles=[line1, line2], prop=chinese_font, loc='upper left')
            ax1.grid(True, alpha=0.3)
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

            # 在底部添加利差子图
            fig2, ax2 = plt.subplots(figsize=(14, 4))
            fig2.suptitle('中美利差 (中国-美国)', fontproperties=chinese_font_title, fontsize=14)

            spread_series = df_recent[cn_col] - df_recent[us_col]
            colors_spread = ['#E74C3C' if v < 0 else '#27AE60' for v in spread_series]
            ax2.bar(dates, spread_series, color=colors_spread, width=2, alpha=0.7)
            ax2.axhline(y=0, color='gray', linewidth=0.8)
            ax2.set_ylabel('利差 (%)', fontproperties=chinese_font)
            ax2.set_xlabel('日期', fontproperties=chinese_font)
            ax2.grid(True, alpha=0.3)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

            plt.tight_layout()
            save_fig(fig, f'中美收益率对比_{TIMESTAMP}.png')
            save_fig(fig2, f'中美利差_{TIMESTAMP}.png')
        else:
            print(f'  ⚠ 近3年数据不足，绘制全部数据...')
            # 备选: 绘制全部数据
            dates = df_sorted[date_col]
            fig, ax = plt.subplots(figsize=(14, 7))
            fig.suptitle('中美10年期国债收益率对比 (全历史)', fontproperties=chinese_font_title, fontsize=16)
            ax.plot(dates, df_sorted[cn_col], label=f'{cn_col}', color='#E74C3C', linewidth=1.5)
            ax.plot(dates, df_sorted[us_col], label=f'{us_col}', color='#2980B9', linewidth=1.5)
            ax.set_ylabel('收益率 (%)', fontproperties=chinese_font)
            ax.legend(prop=chinese_font, loc='upper left')
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.tight_layout()
            save_fig(fig, f'中美收益率对比_{TIMESTAMP}.png')
    else:
        print(f'  ⚠ 未找到中国/美国收益率列，可用列: {list(cn_us_rate.columns)}')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'中美收益率_{TIMESTAMP}.csv')
    cn_us_rate.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取中美收益率数据失败')


# ============================================================
# 第三部分：债券指数走势
# ============================================================
print_header('第三部分：债券指数走势')

# 3.1 国债指数
print('\n  3.1 国债指数 (bond_treasury_index_cbond)...')
treasury_idx = safe_api_call(ak.bond_treasury_index_cbond)
if treasury_idx is not None:
    print(f'  ✓ 成功获取: {len(treasury_idx)} 条数据')
    print(f'  列名: {list(treasury_idx.columns)}')

    # 统一列名
    idx_col = 'date' if 'date' in treasury_idx.columns else treasury_idx.columns[0]
    val_col = 'value' if 'value' in treasury_idx.columns else treasury_idx.columns[1]
    treasury_idx[idx_col] = pd.to_datetime(treasury_idx[idx_col], errors='coerce')
    treasury_idx[val_col] = pd.to_numeric(treasury_idx[val_col], errors='coerce')
    treasury_idx = treasury_idx.sort_values(idx_col).dropna(subset=[val_col])

    print(f'  日期范围: {treasury_idx[idx_col].iloc[0].strftime("%Y-%m-%d")} ~ {treasury_idx[idx_col].iloc[-1].strftime("%Y-%m-%d")}')
    print(f'  最新值: {treasury_idx[val_col].iloc[-1]:.4f}')

    csv_path = os.path.join(DATA_DIR, f'国债指数_{TIMESTAMP}.csv')
    treasury_idx.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取国债指数数据失败')

# 3.2 债券综合指数
print('\n  3.2 债券综合指数 (bond_composite_index_cbond)...')
composite_idx = safe_api_call(ak.bond_composite_index_cbond)
if composite_idx is not None:
    print(f'  ✓ 成功获取: {len(composite_idx)} 条数据')
    print(f'  列名: {list(composite_idx.columns)}')

    idx_col2 = 'date' if 'date' in composite_idx.columns else composite_idx.columns[0]
    val_col2 = 'value' if 'value' in composite_idx.columns else composite_idx.columns[1]
    composite_idx[idx_col2] = pd.to_datetime(composite_idx[idx_col2], errors='coerce')
    composite_idx[val_col2] = pd.to_numeric(composite_idx[val_col2], errors='coerce')
    composite_idx = composite_idx.sort_values(idx_col2).dropna(subset=[val_col2])

    print(f'  日期范围: {composite_idx[idx_col2].iloc[0].strftime("%Y-%m-%d")} ~ {composite_idx[idx_col2].iloc[-1].strftime("%Y-%m-%d")}')
    print(f'  最新值: {composite_idx[val_col2].iloc[-1]:.4f}')

    csv_path = os.path.join(DATA_DIR, f'债券综合指数_{TIMESTAMP}.csv')
    composite_idx.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取债券综合指数数据失败')

# 3.3 绘制债券指数走势对比图
print('\n  3.3 绘制债券指数走势对比图...')
has_treasury = treasury_idx is not None and len(treasury_idx) > 50
has_composite = composite_idx is not None and len(composite_idx) > 50

if has_treasury and has_composite:
    # 取最近3年
    three_years_ago = datetime.now() - timedelta(days=3*365)
    t_df = treasury_idx[treasury_idx[idx_col] >= three_years_ago].copy()
    c_df = composite_idx[composite_idx[idx_col2] >= three_years_ago].copy()

    if len(t_df) > 10 and len(c_df) > 10:
        # 归一化到100
        t_df['normalized'] = t_df[val_col] / t_df[val_col].iloc[0] * 100
        c_df['normalized'] = c_df[val_col2] / c_df[val_col2].iloc[0] * 100

        fig, axes = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 2]})
        fig.suptitle('债券指数走势', fontproperties=chinese_font_title, fontsize=16)

        # 上：归一化对比
        ax1 = axes[0]
        ax1.plot(t_df[idx_col], t_df['normalized'], label='国债指数', color='#E74C3C', linewidth=2)
        ax1.plot(c_df[idx_col2], c_df['normalized'], label='债券综合指数', color='#2980B9', linewidth=2)
        ax1.set_ylabel('归一化值 (基期=100)', fontproperties=chinese_font)
        ax1.legend(prop=chinese_font, loc='upper left')
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        # 下：原始值
        ax2 = axes[1]
        ax2.plot(t_df[idx_col], t_df[val_col], label='国债指数', color='#E74C3C', linewidth=2)
        ax2.set_ylabel('国债指数值', fontproperties=chinese_font, color='#E74C3C')

        ax3 = ax2.twinx()
        ax3.plot(c_df[idx_col2], c_df[val_col2], label='债券综合指数', color='#2980B9', linewidth=2)
        ax3.set_ylabel('债券综合指数值', fontproperties=chinese_font, color='#2980B9')

        # 合并图例
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax3.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, prop=chinese_font, loc='upper left')
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax2.set_xlabel('日期', fontproperties=chinese_font)

        plt.tight_layout()
        save_fig(fig, f'债券指数走势_{TIMESTAMP}.png')
    else:
        print(f'  ⚠ 近3年数据不足，无法绘图')
elif has_treasury:
    # 只绘制国债指数
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('国债指数走势', fontproperties=chinese_font_title, fontsize=16)
    ax.plot(treasury_idx[idx_col], treasury_idx[val_col], color='#E74C3C', linewidth=1.5)
    ax.set_ylabel('指数值', fontproperties=chinese_font)
    ax.set_xlabel('日期', fontproperties=chinese_font)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    save_fig(fig, f'国债指数走势_{TIMESTAMP}.png')
elif has_composite:
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('债券综合指数走势', fontproperties=chinese_font_title, fontsize=16)
    ax.plot(composite_idx[idx_col2], composite_idx[val_col2], color='#2980B9', linewidth=1.5)
    ax.set_ylabel('指数值', fontproperties=chinese_font)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.tight_layout()
    save_fig(fig, f'债券综合指数走势_{TIMESTAMP}.png')
else:
    print('  ⚠ 两个债券指数数据均不可用，跳过绘图')


# ============================================================
# 第四部分：可转债市场 (bond_cb_jsl)
# ============================================================
print_header('第四部分：可转债市场 (bond_cb_jsl)')

cb_market = safe_api_call(ak.bond_cb_jsl)
if cb_market is not None:
    print(f'  ✓ 成功获取: {len(cb_market)} 条数据')
    print(f'  列名: {list(cb_market.columns)}')

    # 关键指标列
    metric_cols = ['现价', '涨跌幅', '转股溢价率', '到期税前收益', '双低']
    available_metrics = [c for c in metric_cols if c in cb_market.columns]

    print(f'\n  可转债关键指标列表 (前30只):')
    display_cols = ['代码', '转债名称'] + available_metrics
    actual_display = [c for c in display_cols if c in cb_market.columns]

    if len(actual_display) >= 3:
        print(cb_market[actual_display].head(30).to_string(index=False))

    # 统计信息
    print(f'\n  关键指标统计:')
    for col in available_metrics:
        numeric_vals = pd.to_numeric(cb_market[col], errors='coerce')
        print(f'    {col}: 均值={numeric_vals.mean():.2f}, '
              f'最大={numeric_vals.max():.2f}, 最小={numeric_vals.min():.2f}')

    # 绘制可转债涨跌幅排名柱状图
    print(f'\n  绘制可转债涨跌幅排名柱状图...')
    if '涨跌幅' in cb_market.columns and '转债名称' in cb_market.columns:
        cb_for_plot = cb_market.copy()
        cb_for_plot['涨跌幅_num'] = pd.to_numeric(cb_for_plot['涨跌幅'], errors='coerce')
        cb_for_plot = cb_for_plot.dropna(subset=['涨跌幅_num'])

        if len(cb_for_plot) >= 10:
            # 取涨跌幅前15和后15
            top_cb = cb_for_plot.nlargest(15, '涨跌幅_num')
            bottom_cb = cb_for_plot.nsmallest(15, '涨跌幅_num')
            cb_rank = pd.concat([top_cb, bottom_cb], ignore_index=True)

            names_cb = [str(n)[:14] for n in cb_rank['转债名称']]
            vals_cb = cb_rank['涨跌幅_num'].values
            colors_cb = ['#E74C3C' if v < 0 else '#27AE60' for v in vals_cb]

            fig, ax = plt.subplots(figsize=(14, 10))
            fig.suptitle('可转债涨跌幅排名 (TOP15 & BOTTOM15)', fontproperties=chinese_font_title, fontsize=16)

            bars = ax.barh(range(len(names_cb)), vals_cb, color=colors_cb, alpha=0.8, edgecolor='white')
            ax.set_yticks(range(len(names_cb)))
            ax.set_yticklabels(names_cb, fontproperties=chinese_font_small)
            ax.set_xlabel('涨跌幅 (%)', fontproperties=chinese_font)
            ax.axvline(x=0, color='gray', linewidth=0.5)
            ax.grid(True, alpha=0.3, axis='x')

            for bar, val in zip(bars, vals_cb):
                x_pos = val + 0.05 if val >= 0 else val - 0.5
                ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                       f'{val:.2f}%', va='center', fontproperties=chinese_font_small, fontsize=8)

            plt.tight_layout()
            save_fig(fig, f'可转债涨跌幅排名_{TIMESTAMP}.png')
        else:
            print(f'  ⚠ 有效涨跌幅数据不足，无法绘图')

    # 双低策略分析 (双低 = 价格 + 转股溢价率*100)
    if '现价' in cb_market.columns and '转股溢价率' in cb_market.columns:
        print(f'\n  双低策略分析:')
        cb_market['现价_num'] = pd.to_numeric(cb_market['现价'], errors='coerce')
        cb_market['转股溢价率_num'] = pd.to_numeric(cb_market['转股溢价率'], errors='coerce')
        cb_market['双低计算'] = cb_market['现价_num'] + cb_market['转股溢价率_num']

        valid_cb = cb_market.dropna(subset=['现价_num', '转股溢价率_num'])
        if len(valid_cb) > 0:
            low_dual = valid_cb.nsmallest(10, '双低计算')
            print(f'  双低值最低的10只可转债:')
            print(f'  {"转债名称":<16} {"现价":>8} {"转股溢价率":>10} {"双低值":>8}')
            print(f'  {"-"*44}')
            for _, r in low_dual.iterrows():
                name = str(r.get('转债名称', ''))[:14]
                price = r['现价_num']
                premium = r['转股溢价率_num']
                dual_val = r['双低计算']
                print(f'  {name:<16} {price:>8.2f} {premium:>10.2f} {dual_val:>8.2f}')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'可转债市场_{TIMESTAMP}.csv')
    cb_market.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取可转债市场数据失败')


# ============================================================
# 第五部分：可转债行情
# ============================================================
print_header('第五部分：可转债行情 (bond_zh_hs_cov_spot)')

cb_spot = safe_api_call(ak.bond_zh_hs_cov_spot)
if cb_spot is not None:
    print(f'  ✓ 成功获取: {len(cb_spot)} 条数据')
    print(f'  列名: {list(cb_spot.columns)}')

    # 显示前10只
    display_cols_spot = [c for c in ['转债名称', '转债代码', '最新价', '涨跌幅', '成交量', '成交额']
                        if c in cb_spot.columns]
    if len(display_cols_spot) >= 3:
        print(f'\n  可转债实时行情 (前10只):')
        print(cb_spot[display_cols_spot].head(10).to_string(index=False))

    # 统计
    print(f'\n  市场统计:')
    numeric_cols = ['最新价', '涨跌幅', '成交量', '成交额']
    for col in numeric_cols:
        if col in cb_spot.columns:
            vals = pd.to_numeric(cb_spot[col], errors='coerce')
            print(f'    {col}: 均值={vals.mean():.2f}, 总量={vals.sum():.2f}')

    # 保存CSV
    csv_path = os.path.join(DATA_DIR, f'可转债行情_{TIMESTAMP}.csv')
    cb_spot.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'\n  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取可转债行情数据失败')


# ============================================================
# 第六部分：国债期货
# ============================================================
print_header('第六部分：国债期货分析')

# 6.1 中国国债期货
print('\n  6.1 中国国债期货 (bond_gb_zh_sina)...')
gb_zh = safe_api_call(ak.bond_gb_zh_sina)
if gb_zh is not None:
    print(f'  ✓ 成功获取: {len(gb_zh)} 条数据')
    print(f'  列名: {list(gb_zh.columns)}')

    # 统一列名
    date_col_zh = 'date' if 'date' in gb_zh.columns else gb_zh.columns[0]
    close_col_zh = 'close' if 'close' in gb_zh.columns else '收盘' if '收盘' in gb_zh.columns else gb_zh.columns[4]
    gb_zh[date_col_zh] = pd.to_datetime(gb_zh[date_col_zh], errors='coerce')
    gb_zh[close_col_zh] = pd.to_numeric(gb_zh[close_col_zh], errors='coerce')
    gb_zh = gb_zh.sort_values(date_col_zh).dropna(subset=[close_col_zh])

    print(f'  日期范围: {gb_zh[date_col_zh].iloc[0].strftime("%Y-%m-%d")} ~ {gb_zh[date_col_zh].iloc[-1].strftime("%Y-%m-%d")}')
    print(f'  最新收盘: {gb_zh[close_col_zh].iloc[-1]:.4f}')

    # 计算均线
    gb_zh['MA5'] = gb_zh[close_col_zh].rolling(window=5).mean()
    gb_zh['MA20'] = gb_zh[close_col_zh].rolling(window=20).mean()

    csv_path = os.path.join(DATA_DIR, f'中国国债期货_{TIMESTAMP}.csv')
    gb_zh.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取中国国债期货数据失败')

# 6.2 美国国债期货
print('\n  6.2 美国国债期货 (bond_gb_us_sina)...')
gb_us = safe_api_call(ak.bond_gb_us_sina)
if gb_us is not None:
    print(f'  ✓ 成功获取: {len(gb_us)} 条数据')
    print(f'  列名: {list(gb_us.columns)}')

    date_col_us = 'date' if 'date' in gb_us.columns else gb_us.columns[0]
    close_col_us = 'close' if 'close' in gb_us.columns else '收盘' if '收盘' in gb_us.columns else gb_us.columns[4]
    gb_us[date_col_us] = pd.to_datetime(gb_us[date_col_us], errors='coerce')
    gb_us[close_col_us] = pd.to_numeric(gb_us[close_col_us], errors='coerce')
    gb_us = gb_us.sort_values(date_col_us).dropna(subset=[close_col_us])

    print(f'  日期范围: {gb_us[date_col_us].iloc[0].strftime("%Y-%m-%d")} ~ {gb_us[date_col_us].iloc[-1].strftime("%Y-%m-%d")}')
    print(f'  最新收盘: {gb_us[close_col_us].iloc[-1]:.4f}')

    gb_us['MA5'] = gb_us[close_col_us].rolling(window=5).mean()
    gb_us['MA20'] = gb_us[close_col_us].rolling(window=20).mean()

    csv_path = os.path.join(DATA_DIR, f'美国国债期货_{TIMESTAMP}.csv')
    gb_us.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f'  ✓ 已保存: {csv_path}')
else:
    print('  ✗ 获取美国国债期货数据失败')

# 6.3 绘制国债期货对比图
print('\n  6.3 绘制国债期货对比图...')
has_zh = gb_zh is not None and len(gb_zh) > 20
has_us = gb_us is not None and len(gb_us) > 20

if has_zh or has_us:
    # 取最近1年数据
    one_year_ago = datetime.now() - timedelta(days=365)

    if has_zh and has_us:
        zh_recent = gb_zh[gb_zh[date_col_zh] >= one_year_ago]
        us_recent = gb_us[gb_us[date_col_us] >= one_year_ago]

        if len(zh_recent) > 10 and len(us_recent) > 10:
            # 归一化对比
            zh_norm = zh_recent[close_col_zh] / zh_recent[close_col_zh].iloc[0] * 100
            us_norm = us_recent[close_col_us] / us_recent[close_col_us].iloc[0] * 100

            fig, axes = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [1, 1]})
            fig.suptitle('中美国债期货走势对比', fontproperties=chinese_font_title, fontsize=16)

            # 上：中国国债期货
            ax1 = axes[0]
            ax1.plot(zh_recent[date_col_zh], zh_recent[close_col_zh], label='中国国债期货 (收盘)',
                    color='#E74C3C', linewidth=1.5)
            ax1.plot(zh_recent[date_col_zh], zh_recent['MA5'], label='MA5',
                    color='#F39C12', linestyle='--', linewidth=1)
            ax1.plot(zh_recent[date_col_zh], zh_recent['MA20'], label='MA20',
                    color='#8E44AD', linestyle='--', linewidth=1)
            ax1.set_ylabel('价格', fontproperties=chinese_font)
            ax1.legend(prop=chinese_font_small, loc='upper left')
            ax1.grid(True, alpha=0.3)
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax1.set_title('中国国债期货', fontproperties=chinese_font)

            # 下：美国国债期货
            ax2 = axes[1]
            ax2.plot(us_recent[date_col_us], us_recent[close_col_us], label='美国国债期货 (收盘)',
                    color='#2980B9', linewidth=1.5)
            ax2.plot(us_recent[date_col_us], us_recent['MA5'], label='MA5',
                    color='#F39C12', linestyle='--', linewidth=1)
            ax2.plot(us_recent[date_col_us], us_recent['MA20'], label='MA20',
                    color='#8E44AD', linestyle='--', linewidth=1)
            ax2.set_ylabel('价格', fontproperties=chinese_font)
            ax2.set_xlabel('日期', fontproperties=chinese_font)
            ax2.legend(prop=chinese_font_small, loc='upper left')
            ax2.grid(True, alpha=0.3)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax2.set_title('美国国债期货', fontproperties=chinese_font)

            plt.tight_layout()
            save_fig(fig, f'中美国债期货对比_{TIMESTAMP}.png')

            # 归一化对比图
            fig2, ax = plt.subplots(figsize=(14, 7))
            fig2.suptitle('中美国债期货走势对比 (归一化)', fontproperties=chinese_font_title, fontsize=16)
            ax.plot(zh_recent[date_col_zh], zh_norm, label='中国国债期货',
                   color='#E74C3C', linewidth=2)
            ax.plot(us_recent[date_col_us], us_norm, label='美国国债期货',
                   color='#2980B9', linewidth=2)
            ax.set_ylabel('归一化值 (基期=100)', fontproperties=chinese_font)
            ax.set_xlabel('日期', fontproperties=chinese_font)
            ax.legend(prop=chinese_font, loc='upper left')
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.tight_layout()
            save_fig(fig2, f'中美国债期货归一化对比_{TIMESTAMP}.png')
        else:
            print(f'  ⚠ 近1年数据不足，分别绘制各自走势')
            # 分别绘制
            if len(zh_recent) > 5:
                fig, ax = plt.subplots(figsize=(14, 7))
                fig.suptitle('中国国债期货走势', fontproperties=chinese_font_title, fontsize=16)
                ax.plot(zh_recent[date_col_zh], zh_recent[close_col_zh], color='#E74C3C', linewidth=1.5)
                ax.set_ylabel('价格', fontproperties=chinese_font)
                ax.grid(True, alpha=0.3)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                plt.tight_layout()
                save_fig(fig, f'中国国债期货走势_{TIMESTAMP}.png')
            if len(us_recent) > 5:
                fig, ax = plt.subplots(figsize=(14, 7))
                fig.suptitle('美国国债期货走势', fontproperties=chinese_font_title, fontsize=16)
                ax.plot(us_recent[date_col_us], us_recent[close_col_us], color='#2980B9', linewidth=1.5)
                ax.set_ylabel('价格', fontproperties=chinese_font)
                ax.grid(True, alpha=0.3)
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                plt.tight_layout()
                save_fig(fig, f'美国国债期货走势_{TIMESTAMP}.png')
    elif has_zh:
        zh_recent = gb_zh[gb_zh[date_col_zh] >= one_year_ago]
        if len(zh_recent) > 5:
            fig, ax = plt.subplots(figsize=(14, 7))
            fig.suptitle('中国国债期货走势', fontproperties=chinese_font_title, fontsize=16)
            ax.plot(zh_recent[date_col_zh], zh_recent[close_col_zh], color='#E74C3C', linewidth=1.5)
            ax.set_ylabel('价格', fontproperties=chinese_font)
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.tight_layout()
            save_fig(fig, f'中国国债期货走势_{TIMESTAMP}.png')
    elif has_us:
        us_recent = gb_us[gb_us[date_col_us] >= one_year_ago]
        if len(us_recent) > 5:
            fig, ax = plt.subplots(figsize=(14, 7))
            fig.suptitle('美国国债期货走势', fontproperties=chinese_font_title, fontsize=16)
            ax.plot(us_recent[date_col_us], us_recent[close_col_us], color='#2980B9', linewidth=1.5)
            ax.set_ylabel('价格', fontproperties=chinese_font)
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.tight_layout()
            save_fig(fig, f'美国国债期货走势_{TIMESTAMP}.png')
else:
    print('  ⚠ 国债期货数据均不可用，跳过绘图')


# ============================================================
# 总结
# ============================================================
print_header('运行完成')
print(f'  输出目录:')
print(f'    数据: {DATA_DIR}/')
print(f'    图表: {PLOT_DIR}/')
print(f'  时间戳: {TIMESTAMP}')

# 列出生成的文件
print(f'\n  生成的数据文件:')
if os.path.exists(DATA_DIR):
    for f in sorted(os.listdir(DATA_DIR)):
        if TIMESTAMP in f:
            fpath = os.path.join(DATA_DIR, f)
            fsize = os.path.getsize(fpath)
            print(f'    {f} ({fsize/1024:.1f} KB)')

print(f'\n  生成的图表文件:')
if os.path.exists(PLOT_DIR):
    for f in sorted(os.listdir(PLOT_DIR)):
        if TIMESTAMP in f:
            fpath = os.path.join(PLOT_DIR, f)
            fsize = os.path.getsize(fpath)
            print(f'    {f} ({fsize/1024:.1f} KB)')

print(f'\n  ✓ 债券数据综合示例运行完成!')
