# AkShare 加密货币数据接口 + CoinGecko API 使用指南

> 最后更新: 2026-05-17

## 概述

本指南介绍如何使用两种数据源获取加密货币数据：

1. **AkShare 原生加密接口** — 3个接口，数据有限（仅BTC/LTC/BCH）
2. **CoinGecko API（推荐）** — 30+公开端点，覆盖12000+币种

由于 AkShare 原生加密接口数量极少、覆盖面窄，**强烈推荐使用 CoinGecko API** 作为主要数据源。

---

## 一、AkShare 原生接口（备用）

### 1.1 实时行情

```python
import akshare as ak

# 获取虚拟货币实时行情
df = ak.crypto_js_spot()
print(df.head())
```

**返回数据**: 约30-50条记录，以USDT交易对为主。

### 1.2 比特币持仓报告

```python
# 获取比特币持仓报告
df = ak.crypto_bitcoin_hold_report()
```

### 1.3 CME 比特币数据

```python
# 获取CME交易所比特币数据
df = ak.crypto_bitcoin_cme(date="20260513")
```

> ⚠ **AkShare 加密接口局限性**：
> - 仅覆盖20-30个主要交易对
> - 无历史OHLCV数据
> - 无市值/交易量等全局数据
> - 数据源稳定性一般

---

## 二、CoinGecko API（推荐）

### 2.1 基础配置

```python
import requests
import pandas as pd
from datetime import datetime

API_BASE = "https://api.coingecko.com/api/v3"

def cg_get(endpoint, params=None):
    """调用CoinGecko API通用函数"""
    url = f"{API_BASE}{endpoint}"
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()
```

> **免费层限制**：10-30次/分钟，建议请求间隔2-3秒

### 2.2 实时价格

```python
# 多币种实时价格
data = cg_get("/simple/price", {
    "ids": "bitcoin,ethereum,solana,ripple",
    "vs_currencies": "usd",
    "include_24hr_change": "true",
    "include_market_cap": "true"
})

for coin_id, info in data.items():
    print(f"{coin_id}: ${info['usd']:,.2f} ({info['usd_24h_change']:+.2f}%)")
```

**返回**: 实时价格、24h变化、市值、24h交易量。

### 2.3 OHLCV 历史K线

```python
# BTC 30天OHLC数据 (4小时K线)
data = cg_get("/coins/bitcoin/ohlc", {
    "vs_currency": "usd",
    "days": "30"
})

df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.set_index("timestamp", inplace=True)
print(df.tail(5))
```

**days 参数**：
| 天数 | K线周期 |
|:----:|:-------:|
| 1 | 分钟级 |
| 7-30 | 4小时 |
| 90+ | 日K |

### 2.4 行情列表（全市场）

```python
# 按市值排序的Top 50
data = cg_get("/coins/markets", {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "1h,24h,7d"
})

df = pd.DataFrame(data)
print(f"共获取 {len(df)} 个币种行情")
```

**返回字段**: 排名、价格、24h/7d变化、市值、交易量、流通量、历史最高等15+字段。

### 2.5 全局市场数据

```python
# 全球加密市场总览
data = cg_get("/global")
gd = data["data"]

print(f"活跃币种: {gd['active_cryptocurrencies']}")
print(f"总市值: ${gd['total_market_cap']['usd']:,.0f}")
print(f"24h量: ${gd['total_volume']['usd']:,.0f}")
print(f"BTC占比: {gd['market_cap_percentage']['btc']:.1f}%")
```

### 2.6 交易所数据

```python
# 交易所列表
data = cg_get("/exchanges", {"per_page": 5, "page": 1})
for ex in data:
    print(f"{ex['name']:20s} #{ex['trust_score_rank']} 24h量: {ex['trade_volume_24h_btc']:,.0f} BTC")

# 衍生品交易所
data = cg_get("/derivatives/exchanges", {"order": "open_interest_btc_desc", "per_page": 5})
for ex in data:
    print(f"{ex['name']:20s} 未平仓量: {ex['open_interest_btc']:,.0f} BTC")
```

### 2.7 市场趋势

```python
# 热门搜索
data = cg_get("/search/trending")
for item in data["coins"][:5]:
    coin = item["item"]
    print(f"{coin['name']:20s} ({coin['symbol']}) #{coin['market_cap_rank']}")

# 搜索
data = cg_get("/search", {"query": "bitcoin"})
for coin in data["coins"][:3]:
    print(f"{coin['name']:20s} ({coin['symbol']})")
```

### 2.8 NFT 数据

```python
# 热门NFT集合
data = cg_get("/nfts/list", {"per_page": 5, "page": 1})

# 指定NFT详情
data = cg_get("/nfts/bored-ape-yacht-club")
print(f"地板价: ${data['floor_price']['usd']:,}")
```

### 2.9 上市公司持仓

```python
# BTC公开持仓
data = cg_get("/companies/public_treasury/bitcoin")
print(f"上市公司数: {len(data['companies'])}")
print(f"总持仓: {data['total_holdings']:,.0f} BTC")
print(f"总价值: ${data['total_value_usd']:,.0f}")
```

### 2.10 汇率

```python
data = cg_get("/exchange_rates")
rates = data["rates"]
print(f"1 BTC = {rates['usd']['value']:,.2f} USD")
print(f"1 BTC = {rates['cny']['value']:,.2f} CNY")
```

---

## 三、完整脚本示例

见 `scripts/s5.2_test_crypto.py`，该脚本覆盖全部30+端点，并包含：
- 实时价格获取
- OHLCV历史K线
- 技术指标计算（MA/MACD/RSI/布林带）
- 金叉死叉信号识别
- 4张可视化图表（价格走势/MACD/RSI/多币种对比）
- CSV数据导出

---

## 四、API端点清单

| 分类 | 端点 | 说明 |
|:----:|------|------|
| 系统 | `/ping` | 服务器状态 |
| 简单价格 | `/simple/price` | 多币种实时价格 |
| 简单价格 | `/simple/supported_vs_currencies` | 支持63种计价货币 |
| 币种 | `/coins/list` | 共17405个币种 |
| 币种 | `/coins/markets` | 按市值排序的行情列表 |
| 币种 | `/coins/{id}` | 币种详情（社交/开发者/描述） |
| 币种 | `/coins/{id}/tickers` | 交易所Ticker |
| 币种 | `/coins/{id}/history` | 指定日期历史数据 |
| 币种 | `/coins/{id}/market_chart` | 市场图表数据 |
| 币种 | `/coins/{id}/market_chart/range` | 时间范围图表 |
| 币种 | `/coins/{id}/ohlc` | OHLC K线数据 |
| 币种 | `/coins/categories` | 分类市场数据 |
| 资产 | `/asset_platforms` | 449条区块链网络 |
| 交易所 | `/exchanges` | 1465个交易所 |
| 交易所 | `/exchanges/{id}/tickers` | 交易所Ticker |
| 衍生品 | `/derivatives` | 衍生品Ticker |
| 衍生品 | `/derivatives/exchanges` | 衍生品交易所 |
| 全局 | `/global` | 全球市场总览 |
| 全局 | `/global/decentralized_finance_defi` | DeFi数据 |
| 搜索 | `/search` | 搜索 |
| 搜索 | `/search/trending` | 热门趋势 |
| NFT | `/nfts/list` | NFT集合列表 |
| NFT | `/nfts/{id}` | NFT详情 |
| 持仓 | `/companies/public_treasury/{coin_id}` | 上市公司/政府持仓 |
| 汇率 | `/exchange_rates` | BTC汇率（63种） |

---

## 五、常见问题

### Q1: 需要API Key吗？
**不需要**。CoinGecko Demo API（公开API）完全免费，无需注册即可使用。

### Q2: 国内网络能用吗？
**可以**。`api.coingecko.com` 在国内可直接访问，无需VPN。

### Q3: 免费API的限制是什么？
- 10-30次/分钟的速率限制
- 无WebSocket支持
- 部分高级端点（如历史数据更多）需要Pro API

### Q4: 数据更新频率？
- 价格/行情数据：实时更新（1-2分钟延迟）
- OHLCV数据：每4小时/天更新一次
- 全局数据：每分钟更新

### Q5: 如何获取更快的访问？
- 请求之间加 `time.sleep(2)` 避免429错误
- 缓存常用数据避免重复请求
- 升级到Pro API（付费）获取更高频率
