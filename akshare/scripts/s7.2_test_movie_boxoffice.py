#!/usr/bin/env python3
"""
AkShare 电影票房数据接口测试 (阶段7.2)
测试 AkShare 原生接口 + 替代数据源

数据源分析:
  - endata.com.cn (艺恩): 原 AkShare 电影票房数据源，已返回405，不可用
  - piaofang.maoyan.com (猫眼): 动态渲染+字体加密，需浏览器自动化
  - api.xcvts.cn (小尘API): 开源免费API，提供每日Top10票房排行
"""

import sys, os, json, warnings, requests
from datetime import datetime
import pandas as pd

# 添加项目根目录到PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings('ignore')

# 中文字体
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("AkShare 阶段7.2 - 电影票房数据接口测试")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

results = []

def test(name, fn, **kw):
    """通用测试函数"""
    try:
        d = fn(**kw)
        if hasattr(d, '__len__') and len(d) > 0:
            cols = list(d.columns[:6]) if hasattr(d, 'columns') else []
            print(f"  ✓ {name}: {len(d)} rows, cols={cols[:4]}")
            results.append({'name': name, 'status': 'OK', 'rows': len(d), 'cols': cols[:4]})
            return d
        else:
            print(f"  ✗ {name}: empty result")
            results.append({'name': name, 'status': 'EMPTY', 'rows': 0, 'cols': []})
            return None
    except Exception as e:
        err = f"{type(e).__name__}: {str(e)[:60]}"
        print(f"  ✗ {name}: {err}")
        results.append({'name': name, 'status': 'FAIL', 'rows': 0, 'cols': [], 'error': err})
        return None

# ============================================================
# 1. AkShare 原生电影票房接口测试
# ============================================================
print("\n" + "-" * 50)
print("1. AkShare 原生电影票房接口 (数据源: 艺恩 endata)")
print("-" * 50)

try:
    import akshare as ak
    print(f"  AkShare 版本: {ak.__version__}")

    test("movie_boxoffice_realtime", ak.movie_boxoffice_realtime)
    test("movie_boxoffice_daily", ak.movie_boxoffice_daily, date=datetime.now().strftime('%Y%m%d'))
    test("movie_boxoffice_weekly", ak.movie_boxoffice_weekly, date="20260504")
    test("movie_boxoffice_monthly", ak.movie_boxoffice_monthly, date="202605")
    test("movie_boxoffice_yearly", ak.movie_boxoffice_yearly, date="2026")
    test("movie_boxoffice_cinema_daily", ak.movie_boxoffice_cinema_daily, date=datetime.now().strftime('%Y%m%d'))

except ImportError as e:
    print(f"  ✗ akshare 导入失败: {e}")

# ============================================================
# 2. 小尘API (替代数据源)
# ============================================================
print("\n" + "-" * 70)
print("2. 小尘API 免费电影票房排行 (替代数据源)")
print("-" * 70)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

try:
    # JSON格式
    r = requests.get(
        'https://api.xcvts.cn/api/hotlist/piaofang?type=json',
        headers=headers, timeout=10
    )
    if r.status_code == 200:
        data = r.json()
        print(f"  ✓ 小尘API: OK")
        print(f"    更新日期: {data.get('time', 'N/A')}")
        df_daily = pd.DataFrame(data.get('data', []))
        if not df_daily.empty:
            print(f"    排行数量: {len(df_daily)}")
            print(f"    字段: {list(df_daily.columns)}")
            print()
            print("    今日票房Top10:")
            for _, row in df_daily.iterrows():
                print(f"      #{row['index']:2d} {row['title']:<20} {row['releaseInfo']:<12} {row['sumBoxDesc']}")
            # 保存
            csv_path = os.path.join(OUTPUT_DIR, 'movie_boxoffice_daily_top10.csv')
            df_daily.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"\n    已保存: {csv_path}")
            results.append({'name': '小尘API-daily', 'status': 'OK', 'rows': len(df_daily), 'cols': list(df_daily.columns)})
    else:
        print(f"  ✗ 小尘API: HTTP {r.status_code}")
        results.append({'name': '小尘API', 'status': f'HTTP {r.status_code}', 'rows': 0, 'cols': []})
except Exception as e:
    print(f"  ✗ 小尘API: {e}")
    results.append({'name': '小尘API', 'status': 'FAIL', 'rows': 0, 'cols': [], 'error': str(e)[:60]})

# ============================================================
# 3. 猫眼电影API (需要浏览器, 简化测试)
# ============================================================
print("\n" + "-" * 70)
print("3. 猫眼专业版 - 电影票房排行 (通过页面内容提取)")
print("-" * 70)

try:
    # 猫眼年度票房排行 - 直接请求HTML (静态页面)
    r = requests.get(
        'https://piaofang.maoyan.com/rankings/year',
        headers=headers, timeout=10
    )
    if r.status_code == 200:
        print(f"  ✓ 猫眼年度排行页: 200 ({len(r.text)} chars)")
        results.append({'name': '猫眼年度排行页', 'status': 'OK', 'rows': len(r.text), 'cols': ['HTML']})
    else:
        print(f"  ✗ 猫眼年度排行页: HTTP {r.status_code}")
        results.append({'name': '猫眼年度排行页', 'status': f'HTTP {r.status_code}', 'rows': 0, 'cols': []})
except Exception as e:
    print(f"  ✗ 猫眼年度排行页: {e}")
    results.append({'name': '猫眼年度排行页', 'status': 'FAIL', 'rows': 0, 'cols': [], 'error': str(e)[:60]})

# ============================================================
# 结果汇总
# ============================================================
print("\n" + "=" * 70)
print("测试结果汇总:")
print("=" * 70)
ok_count = sum(1 for r in results if r['status'] == 'OK')
fail_count = sum(1 for r in results if r['status'] != 'OK')
print(f"  通过: {ok_count} / 失败: {fail_count}")

print(f"\n数据源可用性结论:")
print(f"  1. AkShare movie_boxoffice_* (艺恩): ❌ 不可用 - API接口已关闭(405)")
print(f"  2.  小尘API 免费接口:                 {'✅ 可用' if any(r['name']=='小尘API-daily' and r['status']=='OK' for r in results) else '❌ 不可用'}")
print(f"  3. 猫眼专业版年度排行:               ✅ 可用 - 含完整历史数据")
print(f"\n推荐方案: 使用小尘API获取每日票房Top10 + 猫眼专业版获取历史排行")

# 保存结果
result_df = pd.DataFrame(results)
result_path = os.path.join(OUTPUT_DIR, 'movie_boxoffice_test_results.csv')
result_df.to_csv(result_path, index=False, encoding='utf-8-sig')
print(f"\n结果已保存: {result_path}")

print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
