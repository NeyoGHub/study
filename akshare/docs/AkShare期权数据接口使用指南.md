# AkShare 期权数据接口使用指南

> **文档类型**: 使用指南 | **创建日期**: 2026-05-12

## 核心接口

### ETF期权（上交所）

```python
import akshare as ak

# 获取期权合约代码列表
codes = ak.option_sse_codes_sina(symbol="看涨期权", trade_date="202605", underlying="510050")

# 实时行情（41字段：买量/价、卖量/价、希腊字母、隐含波动率等）
spot = ak.option_sse_spot_price_sina(symbol="10011381")

# 希腊字母
greeks = ak.option_sse_greeks_sina(symbol="10011381")

# 日线
daily = ak.option_sse_daily_sina(symbol="10011381")
```

### 股指期权（中金所）

```python
# 沪深300/上证50/中证1000 股指期权
hs300 = ak.option_cffex_hs300_spot_sina()  # 33行
sz50  = ak.option_cffex_sz50_spot_sina()   # 21行
zz1000 = ak.option_cffex_zz1000_spot_sina()  # 20行
```

### 波动率

```python
# 上期所期权隐含波动率
vol = ak.option_vol_shfe()
```
