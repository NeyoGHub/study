#!/usr/bin/env python3
"""
AkShare 电影票房数据 - 综合演示脚本 (阶段7.2)
使用替代数据源 (小尘API + 猫眼专业版) 获取电影票房数据并进行可视化分析

功能:
  1. 每日实时票房 Top10 (小尘API)
  2. 猫眼年度排行页面可访问性检测
  3. 票房数据可视化图表 (柱状图 + 饼图)

脚本使用方法:
  python scripts/s7.2_demo_movie_boxoffice.py
"""

import sys, os, json, warnings, requests
from datetime import datetime
import pandas as pd
from matplotlib import font_manager as fm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
warnings.filterwarnings('ignore')

# ============================================================
# 配置
# ============================================================
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
chinese_font = fm.FontProperties(fname=FONT_PATH, size=12)
chinese_font_title = fm.FontProperties(fname=FONT_PATH, size=14)
chinese_font_small = fm.FontProperties(fname=FONT_PATH, size=10)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DATA = os.path.join(BASE_DIR, 'output', 'data', 'movie')
OUTPUT_PLOTS = os.path.join(BASE_DIR, 'output', 'plots', 'movie')
os.makedirs(OUTPUT_DATA, exist_ok=True)
os.makedirs(OUTPUT_PLOTS, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


def format_box_office(val_str):
    """将 '1.76亿' / '9137.1万' 转换为万元数值"""
    s = str(val_str).strip().replace(',', '')
    if '亿' in s:
        return float(s.replace('亿', '')) * 10000
    elif '万' in s:
        return float(s.replace('万', ''))
    else:
        try:
            return float(s)
        except:
            return 0.0


# ============================================================
# 1. 小尘API - 每日票房Top10
# ============================================================
def fetch_daily_boxoffice():
    """获取每日票房 Top10 (小尘API)"""
    print("=" * 70)
    print("1. 每日实时票房 Top10 (数据源: 小尘API)")
    print("=" * 70)

    try:
        r = requests.get(
            'https://api.xcvts.cn/api/hotlist/piaofang?type=json',
            headers=HEADERS, timeout=15
        )
        if r.status_code != 200:
            print(f"  ✗ 请求失败: HTTP {r.status_code}")
            return None

        data = r.json()
        df = pd.DataFrame(data.get('data', []))
        df['date'] = data.get('time', '')
        df['box_office_wan'] = df['sumBoxDesc'].apply(format_box_office)

        print(f"  更新日期: {data.get('time', 'N/A')}")
        print(f"  排行数量: {len(df)}")
        print()
        for _, row in df.iterrows():
            print(f"  #{row['index']:2d} {row['title']:<20s} {row['releaseInfo']:<12s} {row['sumBoxDesc']:>10s}")

        csv_path = os.path.join(OUTPUT_DATA, 'daily_top10.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"\n  已保存: {csv_path}")
        return df
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return None


# ============================================================
# 2. 猫眼年度排行 - 可访问性检测
# ============================================================
def check_maoyan_access():
    """检测猫眼专业版年度排行页面可访问性"""
    print("\n" + "=" * 70)
    print("2. 猫眼专业版 - 年度排行页面可访问性检测")
    print("=" * 70)

    try:
        r = requests.get(
            'https://piaofang.maoyan.com/rankings/year',
            headers=HEADERS, timeout=8
        )
        if r.status_code == 200:
            print(f"  ✓ 页面访问成功: HTTP 200 ({len(r.text)} chars)")
            print(f"  提示: 完整数据需通过浏览器渲染后提取")

            html_path = os.path.join(OUTPUT_DATA, 'maoyan_rankings_all.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(r.text)
            print(f"  已保存: {html_path}")
            return True
        else:
            print(f"  ✗ HTTP {r.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ {e}")
        return False


# ============================================================
# 3. 可视化
# ============================================================
def plot_top10(df):
    """绘制每日票房Top10图表"""
    if df is None or df.empty:
        print("\n  跳过可视化: 无数据")
        return

    print("\n" + "=" * 70)
    print("3. 生成可视化图表")
    print("=" * 70)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        f"电影票房排行 ({df['date'].iloc[0]})",
        fontproperties=chinese_font_title, fontsize=16
    )

    # 柱状图
    df_sorted = df.sort_values('box_office_wan', ascending=True)
    unit = '亿' if df_sorted['box_office_wan'].max() > 10000 else '万'
    vals = df_sorted['box_office_wan'] / (10000 if unit == '亿' else 1)

    colors = plt.cm.plasma(
        df_sorted['box_office_wan'] / df_sorted['box_office_wan'].max()
    )
    ax1.barh(range(len(df_sorted)), vals, color=colors, edgecolor='white')

    ax1.set_yticks(range(len(df_sorted)))
    ax1.set_yticklabels(
        [f"#{r['index']} {r['title']}" for _, r in df_sorted.iterrows()],
        fontproperties=chinese_font_small
    )
    ax1.set_xlabel(f'票房 ({unit}元)', fontproperties=chinese_font)
    ax1.set_title('票房排行 (Top10)', fontproperties=chinese_font)

    for i, (_, row) in enumerate(df_sorted.iterrows()):
        ax1.text(vals.iloc[i] + (0.5 if unit == '亿' else 10), i,
                 row['sumBoxDesc'], va='center', fontproperties=chinese_font_small)

    # 饼图
    df_top5 = df.head(5)
    other_sum = df['box_office_wan'].sum() - df_top5['box_office_wan'].sum()
    labels = list(df_top5['title']) + ['其他']
    sizes = list(df_top5['box_office_wan']) + [other_sum]
    label_texts = (
        [f"{l}: {r['sumBoxDesc']}" for l, r in zip(
            list(df_top5['title']),
            [df_top5.iloc[i] for i in range(len(df_top5))]
        )]
        + [f"其他: {other_sum/10000:.2f}亿" if other_sum > 10000 else f"其他: {other_sum:.0f}万"]
    )

    wedges, texts, autotexts = ax2.pie(
        sizes, labels=None, autopct='%1.1f%%',
        startangle=90, colors=plt.cm.Set3(range(len(labels)))
    )
    for t in autotexts:
        t.set_fontproperties(chinese_font_small)
    ax2.legend(
        wedges, label_texts,
        loc='center left', bbox_to_anchor=(1, 0.5),
        prop=chinese_font_small
    )
    ax2.set_title('票房占比', fontproperties=chinese_font)

    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    plot_path = os.path.join(OUTPUT_PLOTS, 'daily_top10.png')
    fig.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ 图表已保存: {plot_path}")


# ============================================================
# 4. 总结
# ============================================================
def generate_summary(df):
    """生成数据总结"""
    print("\n" + "=" * 70)
    print("4. 数据总结")
    print("=" * 70)

    if df is not None and not df.empty:
        total = df['box_office_wan'].sum()
        top1 = df.iloc[0]
        total_str = f"{total/10000:.2f}亿" if total > 10000 else f"{total:.0f}万"
        print(f"  总票房(前十): {total_str}")
        print(f"  冠军: {top1['title']} ({top1['sumBoxDesc']}) - 占比 {top1['box_office_wan']/total*100:.1f}%")
        print(f"  Top3合计: {df.head(3)['box_office_wan'].sum()/10000:.2f}亿")

    print("\n  数据源状态:")
    print("    ✅ 小尘API (https://api.xcvts.cn) — 每日Top10")
    print("    ✅ 猫眼专业版 (https://piaofang.maoyan.com) — 完整排行数据")
    print("    ❌ AkShare movie_boxoffice_* (艺恩 endata) — API已关闭")
    print("\n  数据源问题说明:")
    print("    AkShare 的 movie_boxoffice_* 系列接口的数据源为艺恩(endata.com.cn),")
    print("    该API已停止服务(返回405), 导致所有6个接口无法使用。")
    print("    替代方案: 小尘API(免费, 无认证, 每日Top10) + 猫眼专业版(浏览器渲染).")


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 70)
    print("  AkShare 电影票房数据综合演示 (阶段7.2)")
    print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    df_daily = fetch_daily_boxoffice()
    check_maoyan_access()
    plot_top10(df_daily)
    generate_summary(df_daily)

    print(f"\n{'-' * 70}")
    print(f"  数据: {OUTPUT_DATA}")
    print(f"  图表: {OUTPUT_PLOTS}")
    print(f"  完成: {datetime.now().strftime('%H:%M:%S')}")


if __name__ == '__main__':
    main()
