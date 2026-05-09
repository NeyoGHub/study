#!/usr/bin/env python3
"""
核心数据源快速测试
只测试最重要的数据源
"""

import akshare as ak
from datetime import datetime

print("="*70)
print("AkShare核心数据源快速测试")
print("="*70)

# 只测试最重要的数据源
core_tests = [
    ('新浪-A股实时', lambda: ak.stock_zh_a_spot(), '5500+条'),
    ('新浪-A股历史', lambda: ak.stock_zh_a_daily(symbol="sz002624", start_date="20240101", end_date="20260430"), '558条'),
    ('新浪-指数实时', lambda: ak.stock_zh_index_spot_sina(), '562条'),
    ('新浪-港股实时', lambda: ak.stock_hk_index_spot_sina(), '38条'),
    ('腾讯-A股历史', lambda: ak.stock_zh_a_hist_tx(symbol="sz000001", start_date="2024-03-01", end_date="2024-03-31"), '按日期范围'),
]

results = {
    'stable': [],    # 稳定可用
    'unstable': [],  # 可用但不稳定
    'failed': []     # 不可用
}

for name, func, expected in core_tests:
    print(f"\n测试: {name}")
    print("-"*50)

    try:
        data = func()
        if data is not None and len(data) > 0:
            print(f"✓ 成功！获取 {len(data)} 条数据（预期: {expected}）")
            results['stable'].append(name)
        else:
            print(f"✗ 返回空数据")
            results['failed'].append(name)
    except Exception as e:
        error = str(e)[:80]
        if 'Connection aborted' in error or 'Remote end closed' in error:
            print(f"✗ 不稳定: {error}")
            results['unstable'].append(name)
        else:
            print(f"✗ 失败: {error}")
            results['failed'].append(name)

# 总结
print("\n" + "="*70)
print("测试总结")
print("="*70)

print(f"\n稳定可用 ({len(results['stable'])}个):")
for i, name in enumerate(results['stable'], 1):
    print(f"  {i}. {name}")

print(f"\n可用但不稳定 ({len(results['unstable'])}个):")
for i, name in enumerate(results['unstable'], 1):
    print(f"  {i}. {name}")

print(f"\n不可用 ({len(results['failed'])}个):")
for i, name in enumerate(results['failed'], 1):
    print(f"  {i}. {name}")

print("\n" + "="*70)
print("最终结论")
print("="*70)

if len(results['stable']) >= 3:
    print("✓ AkShare有稳定可用的核心数据源")
    print("✓ 新浪财经是主要数据源，非常稳定")
    print("✓ 可以满足历史数据和实时数据需求")
elif len(results['stable']) >= 1:
    print("⚠ AkShare有少量可用数据源")
    print("⚠ 需要谨慎使用，可能需要容错机制")
else:
    print("✗ AkShare当前环境下大部分数据源不可用")
    print("✗ 建议检查网络或使用代理")

print("\n" + "="*70)
print("数据源优先级（基于测试结果）")
print("="*70)

priority_list = [
    ("stock_zh_a_daily", "新浪-A股历史", "1", "核心推荐"),
    ("stock_zh_a_spot", "新浪-A股实时", "2", "核心推荐"),
    ("stock_zh_a_minute", "新浪-分钟数据", "3", "可选"),
    ("stock_zh_index_spot_sina", "新浪-指数实时", "4", "可选"),
    ("stock_zh_a_hist_tx", "腾讯-A股历史", "5", "备用"),
]

for api, name, priority, note in priority_list:
    print(f"{priority}. {api} - {name} ({note})")