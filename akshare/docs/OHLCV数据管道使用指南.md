# OHLCV 数据管道使用指南 — OKX + CoinGecko 双源融合

> 最后更新: 2026-05-17
> 阶段: 9.1 — 量化数据基础设施

---

## 一、概述

本数据管道为加密货币量化交易系统提供稳定的 OHLCV 数据，融合两大免费数据源：

| 数据源 | 协议 | 定位 | 优势 |
|:------:|:----:|:----:|:----:|
| **OKX** (CCXT) | 交易所API | 主力实时 | 毫秒级、无限频、3976交易对 |
| **CoinGecko** | REST API | 历史补充 | 17405币种、数年历史、聚合价格 |

### 融合策略

```
CoinGecko 历史数据 (90天+) ─┐
                            ├→ 统一OHLCV数据集 → CSV存储 → 回测/策略
OKX 近期数据 (100-500条)   ─┘
```

---

## 二、快速开始

### 2.1 安装依赖

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/pip install ccxt pandas matplotlib numpy
```

### 2.2 运行管道

```bash
./venv/bin/python scripts/s9.1_demo_ohlcv_pipeline.py
```

输出：
- `output/data/crypto/ohlcv_merged_*` — 融合数据CSV
- `output/data/crypto/ohlcv_okx_*` — OKX原始数据
- `output/data/crypto/ohlcv_coingecko_*` — CoinGecko原始数据
- `output/plots/crypto/ohlcv_*` — 可视化图表

---

## 三、数据源使用

### 3.1 OKX (CCXT)

```python
import ccxt

ex = ccxt.okx({"enableRateLimit": True})

# 支持的时间周期
timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]

# 获取BTC/USDT日K线 (最近100条)
ohlcv = ex.fetch_ohlcv("BTC/USDT", "1d", limit=100)

# 列印
import pandas as pd
df = pd.DataFrame(ohlcv, columns=["timestamp","open","high","low","close","volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("timestamp", inplace=True)
print(df.tail())
```

### 3.2 CoinGecko API

```python
import requests

# BTC 90天OHLC (4小时K线)
resp = requests.get(
    "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc",
    params={"vs_currency": "usd", "days": 90},
    timeout=15
)
data = resp.json()

df = pd.DataFrame(data, columns=["timestamp","open","high","low","close"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("timestamp", inplace=True)
```

### 3.3 双源融合

```python
# 对齐到日期 (去除时间部分)
okx.index = okx.index.normalize()
cg.index = cg.index.normalize()

# 合并: OKX优先
merged = pd.concat([
    okx.add_suffix("_okx"),
    cg.add_suffix("_cg")
], axis=1)
merged = merged[~merged.index.duplicated(keep="first")].sort_index()

# 差异分析
overlap = merged.dropna()
diff_pct = abs(overlap["close_okx"] - overlap["close_cg"]) / overlap["close_cg"] * 100
print(f"收盘价平均差异: {diff_pct.mean():.2f}%")
```

---

## 四、数据字段说明

### 4.1 OKX 返回字段

| 字段 | 类型 | 说明 |
|:----:|:----:|------|
| timestamp | datetime | K线时间 (ms→datetime) |
| open | float | 开盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| close | float | 收盘价 |
| volume | float | 成交量 (基础币种) |

### 4.2 CoinGecko 返回字段

| 字段 | 类型 | 说明 |
|:----:|:----:|------|
| timestamp | datetime | K线时间 (ms→datetime) |
| open | float | 开盘价 (聚合) |
| high | float | 最高价 |
| low | float | 最低价 |
| close | float | 收盘价 |

### 4.3 融合后字段

| 字段 | 说明 |
|:----:|------|
| close_okx | OKX收盘价 (主) |
| close_cg | CoinGecko收盘价 (副) |
| close_diff_pct | 两源差异百分比 |
| volume | OKX成交量 |

---

## 五、时间周期说明

| K线周期 | 数据量 | 适合场景 |
|:-------:|:------:|:---------|
| 1m | OKX: ~500条 | 超短线/分钟级策略 |
| 5m | OKX: ~500条 | 短线交易 |
| 15m | OKX: ~500条 | 短线交易 |
| 1h | OKX: ~500条 | 日内交易 |
| 4h | OKX: ~500条 | 波段交易 |
| 1d | OKX: ~365条 / CG: 90-365条 | 中长线/回测 |
| 1w | OKX: 不限 | 长期趋势 |

---

## 六、常见问题

### Q1: OKX 最多能拿多少条历史数据？

默认500条。可通过 `fetch_ohlcv` 的 `since` 参数逐段获取更早数据，但OKX对历史数据有深度限制。

### Q2: CoinGecko 的 days 参数与K线周期的关系？

| days | K线周期 |
|:----:|:-------:|
| 1 | 分钟级 |
| 7 | 30分钟 |
| 14 | 4小时 |
| 30 | 4小时 |
| 90 | 4小时 |
| 180 | 日K |
| max | 日K (数年) |

### Q3: OKX 和 CoinGecko 数据差异有多大？

实测平均收盘价差异 < 1%。差异主要来自：
- OKX: 单一交易所价格
- CoinGecko: 多交易所聚合价格

### Q4: 如何添加更多币种？

在脚本 `COINS` 列表中添加，并在 `CoinGeckoSource.coin_id_map()` 中增加映射。

### Q5: 可以用其他交易所吗？

可以。替换 CCXT 的 exchange 实例即可：
```python
# 改为 KuCoin
ex = ccxt.kucoin({"enableRateLimit": True})
# 或 MEXC
ex = ccxt.mexc({"enableRateLimit": True})
```
