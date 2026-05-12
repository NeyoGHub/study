#!/usr/bin/env python3
"""AkShare REITs数据接口测试 (阶段5.3 - 使用新浪替代数据源)"""

import akshare as ak, pandas as pd, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

print("=" * 70)
print("AkShare REITs数据接口测试（新浪数据源替代）")
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

reits = [
    ('sh508000','张江REIT','产业园'), ('sh508001','浙江杭徽','高速公路'),
    ('sh508006','首创水务','水务'), ('sh508008','国金铁建','高速公路'),
    ('sh508027','东吴苏园','产业园'), ('sh508056','中金普洛斯','仓储物流'),
    ('sh508066','京东仓储','仓储物流'), ('sh508077','京能光伏','能源'),
    ('sh508088','国泰君安','产业园'), ('sh508096','中国交建','高速公路'),
    ('sh508097','中国铁建','高速公路'), ('sh508098','电建清源','能源'),
    ('sh508099','国家电投','能源'), ('sz180101','平安广州','水务'),
    ('sz180102','蛇口产园','产业园'), ('sz180103','红土盐田','仓储物流'),
    ('sz180201','鹏华前海','综合'),
]

ok = 0
for code, name, cat in reits:
    try:
        d = ak.fund_etf_hist_sina(symbol=code)
        if hasattr(d, '__len__') and len(d) > 0:
            print(f'  ✓ {code} {name:10s} ({cat}): {len(d):5} rows')
            ok += 1
        else:
            print(f'  - {code} {name:10s}: 空数据')
    except Exception as e:
        print(f'  ✗ {code} {name:10s}: {type(e).__name__}')

print(f"\n成功: {ok}/{len(reits)} (使用 fund_etf_hist_sina 替代东方财富)")
print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
