# AkShare 加密货币数据接口使用指南

## 📌 接口概述

**数据源**: 金十数据中心
**接口数量**: 3个核心接口
**更新频率**: 实时更新
**适用场景**: 市场监控、持仓分析、机构资金流向研究

---

## 📋 接口列表

### 接口1：虚拟货币实时行情 - crypto_js_spot

**功能**: 获取全球主要交易所的虚拟货币实时行情

**接口调用**:
```python
import akshare as ak
df = ak.crypto_js_spot()
```

**参数说明**: 无参数

**返回字段**:
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 市场 | str | 交易所名称（如Bitfinex(香港）、Kraken(美国)） |
| 交易品种 | str | 货币对（如BTCUSD, LTCUSD） |
| 最近报价 | float | 当前价格 |
| 涨跌额 | float | 价格变化 |
| 涨跌幅 | float | 百分比变化 |
| 24小时最高 | float | 当日最高价 |
| 24小时最低 | float | 当日最低价 |
| 24小时成交量 | float | 交易量 |
| 更新时间 | str | 数据时间戳 |

**⚠️ 严重局限性**:
- **数据量极少**: 仅10条数据，远不能满足完整市场分析需求
- **币种覆盖极窄**: 主要只覆盖比特币(BTC)、莱特币(LTC)、比特币现金(BCH)
- **缺少主流币种**: 没有以太坊(ETH)、狗狗币(DOGE)、币安币(BNB)、索拉纳(SOL)、瑞波(XRP)等主流币种
- **数据时效性**: 更新时间戳显示为2023年，可能不是真正的实时数据
- **不适合专业交易**: 数据量和覆盖面远不足以支持实际的加密货币交易和研究

**使用示例**:
```python
import akshare as ak

# 获取实时行情
crypto_spot_df = ak.crypto_js_spot()

# 按涨跌幅排序
top_gainers = crypto_spot_df.nlargest(5, '涨跌幅')
top_losers = crypto_spot_df.nsmallest(5, '涨跌幅')

# 统计交易所分布
exchange_counts = crypto_spot_df['市场'].value_counts()

# 统计货币对分布
crypto_spot_df['基础货币'] = crypto_spot_df['交易品种'].str.extract(r'([A-Z]+)')[0]
base_currency_counts = crypto_spot_df['基础货币'].value_counts()
```

**数据特点**:
- 数据量：约10条主流交易所数据
- 覆盖交易所：Bitfinex、Kraken、Bitstamp、CEX.IO、OKCoin等
- 主要币种：BTC、LTC、BCH
- 更新频率：实时

---

### 接口2：比特币持仓报告 - crypto_bitcoin_hold_report

**功能**: 获取比特币持仓分布情况

**接口调用**:
```python
import akshare as ak
df = ak.crypto_bitcoin_hold_report()
```

**参数说明**: 无参数

**返回字段**:
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 代码 | str | 股票代码 |
| 公司名称-英文 | str | 英文名称 |
| 公司名称-中文 | str | 中文名称 |
| 国家/地区 | str | 所在国家 |
| 市值 | float | 公司市值 |
| 比特币占市值比重 | float | BTC占比 |
| 持仓成本 | float | 平均成本 |
| 持仓占比 | float | 持有比例 |
| 持仓量 | float | BTC数量 |
| 当日持仓市值 | float | 当前价值 |
| 查询日期 | str | 数据日期 |
| 公告链接 | str | 官方公告URL |
| 分类 | str | 实体类型 |
| 倍数 | float | 杠杆倍数 |

**使用示例**:
```python
import akshare as ak

# 获取持仓报告
holdings_df = ak.crypto_bitcoin_hold_report()

# 持仓量最多的10个实体
top_holders = holdings_df.nlargest(10, '持仓量')

# 按类型统计
category_counts = holdings_df['分类'].value_counts()

# 总持仓量
total_holdings = holdings_df['持仓量'].sum()

# 重点关注大额持仓（>100000 BTC）
large_holders = holdings_df[holdings_df['持仓量'] > 100000]
```

**数据特点**:
- 数据量：约59条记录
- 实体类型：上市公司、ETF、私营企业、政府机构
- 更新频率：实时
- 分析价值：极高，可分析机构资金流向

---

### 接口3：CME交易所数据 - crypto_bitcoin_cme

**功能**: 获取芝加哥商品交易所比特币期货期权数据

**接口调用**:
```python
import akshare as ak
df = ak.crypto_bitcoin_cme(date="20230830")
```

**参数说明**:
- `date`: 交易日期，格式为YYYYMMDD（如"20230830"）

**返回字段**:
| 字段名 | 类型 | 说明 |
|--------|------|------|
| 商品 | str | 商品名称 |
| 类型 | str | 期货/期权/看涨/看跌 |
| 电子交易合约 | int | 电子成交量 |
| 场内成交合约 | int | 场内成交量 |
| 场外成交合约 | int | 场外成交量 |
| 成交量 | int | 总成交量 |
| 未平仓合约 | int | 持仓量 |
| 持仓变化 | int | 持仓变动 |

**使用示例**:
```python
import akshare as ak
from datetime import datetime

# 获取指定日期的CME数据
cme_df = ak.crypto_bitcoin_cme(date="20230830")

# 分析期货与期权
futures_data = cme_df[cme_df['类型'] == '期货']
options_data = cme_df[cme_df['类型'].isin(['看涨', '看跌'])]

# 持仓量分析
open_interest = cme_df['未平仓合约'].sum()
```

**注意事项**:
- 需要使用有效的交易日
- 当前日期可能无数据
- 数据延迟较大

---

## 🔬 数据分析示例

### 实时行情分析

```python
import akshare as ak

# 获取实时行情
crypto_spot_df = ak.crypto_js_spot()

# 市场分析
print("=== 实时行情分析 ===")
print(f"数据量: {len(crypto_spot_df)}条")
print(f"交易所数量: {crypto_spot_df['市场'].nunique()}个")

# 涨跌幅分析
print(f"\n涨幅最大:")
top_gainer = crypto_spot_df.nlargest(1, '涨跌幅')
print(top_gainer[['交易品种', '最近报价', '涨跌幅']])

print(f"\n跌幅最大:")
top_loser = crypto_spot_df.nsmallest(1, '涨跌幅')
print(top_loser[['交易品种', '最近报价', '涨跌幅']])

# 成交量分析
print(f"\n24小时成交量最大:")
high_volume = crypto_spot_df.nlargest(1, '24小时成交量')
print(high_volume[['交易品种', '最近报价', '24小时成交量']])
```

### 持仓分析

```python
import akshare as ak

# 获取持仓报告
holdings_df = ak.crypto_bitcoin_hold_report()

# 持仓集中度分析
print("=== 比特币持仓分析 ===")

# TOP 10 持仓者
print("\n持仓量TOP 10:")
top_10 = holdings_df.nlargest(10, '持仓量')
for idx, row in top_10.iterrows():
    print(f"{row['公司名称-中文']}: {row['持仓量']:,.0f} BTC ({row['持仓占比']:.3f}%)")

# 持仓类型分布
print("\n按类型分布:")
category_summary = holdings_df.groupby('分类')['持仓量'].agg(['sum', 'count'])
print(category_summary)

# 机构持仓分析
institutional = holdings_df[holdings_df['分类'].isin(['上市公司', 'ETF', '政府机构'])]
inst_holdings = institutional['持仓量'].sum()
total_holdings = holdings_df['持仓量'].sum()
print(f"\n机构持仓比例: {inst_holdings/total_holdings:.2%}")
```

---

## 📈 可视化示例

### 持仓分布可视化

```python
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
chinese_font = fm.FontProperties(fname=font_path, size=12)

# 获取数据
holdings_df = ak.crypto_bitcoin_hold_report()
top_10 = holdings_df.nlargest(10, '持仓量')

# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制柱状图
bars = ax.barh(range(len(top_10)), top_10['持仓量'])
ax.set_yticks(range(len(top_10)))
ax.set_yticklabels(top_10['公司名称-中文'], fontproperties=chinese_font)
ax.set_xlabel('持仓量 (BTC)', fontproperties=chinese_font)
ax.set_title('比特币持仓量TOP 10', fontproperties=chinese_font, fontweight='bold')

# 添加数值标签
for i, (bar, value) in enumerate(zip(bars, top_10['持仓量'])):
    ax.text(value, i, f' {value:,.0f}', va='center', fontproperties=chinese_font)

plt.tight_layout()
plt.savefig('holdings_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## 💡 最佳实践

### 1. 数据获取策略

**实时监控**:
```python
# 定期获取实时行情
import akshare as ak
import time

while True:
    crypto_spot_df = ak.crypto_js_spot()
    btc_price = crypto_spot_df[crypto_spot_df['交易品种']=='BTCUSD']['最近报价'].values[0]
    print(f"BTC价格: {btc_price}")
    time.sleep(60)  # 每分钟更新
```

**持仓跟踪**:
```python
# 每日更新持仓报告
import akshare as ak
from datetime import datetime

holdings_df = ak.crypto_bitcoin_hold_report()

# 重点关注大额持仓
large_holders = holdings_df[holdings_df['持仓量'] > 100000]

print(f"大额持仓者数量: {len(large_holders)}")
print(f"总持仓量: {holdings_df['持仓量'].sum():.0f} BTC")
```

### 2. 数据融合策略

**结合专业API**:
```python
# 结合AkShare和专业API
import akshare as ak
import ccxt

# 使用AkShare获取市场概览和持仓数据
ak_spot = ak.crypto_js_spot()
ak_holdings = ak.crypto_bitcoin_hold_report()

# 使用CCXT获取详细历史数据和订单簿
exchange = ccxt.binance()
ticker = exchange.fetch_ticker('BTC/USDT')
orderbook = exchange.fetch_order_book('BTC/USDT')
```

---

## ❓ 常见问题

### Q1: 实时行情数据量为什么只有10条？

**A**: AkShare的加密货币实时行情接口主要提供主流交易所的代表性数据，不是所有交易所的全部数据。如果需要更详细的数据，建议使用CCXT等专业API。

### Q2: 持仓报告的更新频率如何？

**A**: 持仓报告相对稳定，通常在季度或半年度更新。上市公司和ETF的持仓数据相对固定，政府机构的持仓会有调整。

### Q3: CME数据为什么有时候返回空？

**A**: CME数据需要使用有效的交易日。如果查询当天没有数据，可能是非交易日或数据延迟。建议查询历史日期进行测试。

### Q4: 如何获取更多币种的数据？

**A**: AkShare主要提供主流币种（BTC、LTC、BCH等）。如果需要更多币种，建议结合其他专业API使用。

### Q5: 数据可以用于量化交易吗？

**A**: AkShare的加密货币接口更适合市场概览和持仓分析。如果需要做量化交易，建议使用CCXT等专业API获取更详细的历史数据和实时数据。

---

## 🎯 适用场景

### 适合场景
- ✓ 市场监控和概览
- ✓ 持仓分析和机构资金流向研究
- ✓ 跨交易所价格对比
- ✓ 投资决策参考
- ✓ 学术研究和报告

### 不适合场景
- ✗ 高频交易（数据延迟较大）
- ✓ 详细技术分析（数据量太少）
- ✓ 历史数据回测（无历史接口）
- ✓ 链上数据分析（无链上数据）

---

## 📞 支持和反馈

- **数据源**: 金十数据中心
- **文档**: AkShare官方文档
- **社区**: GitHub Issues

---

## 🚨 重要警告：AkShare加密货币接口的严重局限性

### 数据覆盖面极窄 - 不适合专业加密货币研究

您的问题非常准确：**AkShare的加密货币接口覆盖面太窄，远不能满足实际研究需求**。

#### 核心问题

1. **币种覆盖严重不足**
   - **实时行情仅10条数据**: 仅覆盖BTC、LTC、BCH等少数币种
   - **缺少主流币种**:
     - ❌ 以太坊(ETH) - 第二大加密货币
     - ❌ 狗狗币(DOGE) - 热门Meme币
     - ❌ 币安币(BNB) - 全球最大交易所平台币
     - ❌ 索拉纳(SOL) - 高性能公链
     - ❌ 瑞波(XRP) - 跨境支付
     - ❌ 波场(TRON/TRX)、Cardano(ADA)、Polygon(MATIC)等

2. **数据深度不足**
   - ❌ 无DeFi协议数据
   - ❌ 无NFT市场数据
   - ❌ 无链上数据（Gas费用、交易量、活跃地址）
   - ❌ 无交易所储备金数据
   - ❌ 无资金费率、合约持仓等衍生品数据

3. **接口数量极少**
   - 仅3个接口（vs股票50+、基金20+、期货30+）
   - 无历史K线数据接口
   - 无多时间周期数据
   - 无技术指标计算

#### 根本原因

**AkShare专注传统金融**，加密货币接口只是后期补充功能：
- 数据源单一（仅金十数据中心）
- 缺乏多数据源容错机制
- 不是AkShare的核心模块

#### 如果您需要全面的加密货币数据

**推荐的替代方案**:

1. **CoinGecko API** (免费，推荐入门)
   - 覆盖10000+种加密货币
   - 实时价格、市值、交易量
   - 历史数据和交易所排名
   - 文档: https://www.coingecko.com/en/api

2. **Binance API** (部分免费，推荐专业用途)
   - 全球最大交易所数据
   - 实时K线、深度、交易数据
   - WebSocket实时推送
   - 文档: https://binance-docs.github.io/apidocs/

3. **CCXT库** (开源免费，支持多交易所)
   - 统一接口，支持100+交易所
   - Python库，安装: `pip install ccxt`
   - GitHub: https://github.com/ccxt/ccxt
   - 适合量化交易系统

4. **CryptoCompare API** (免费+付费)
   - 专业级加密货币数据
   - 历史K线、社交数据、挖掘数据
   - 指数和衍生品数据
   - 文档: https://min-api.cryptocompare.com/

#### AkShare加密货币接口适用场景

✅ **适合**:
- 比特币基础价格和机构持仓分析
- 学习加密货币数据处理方法
- 教学演示简单示例
- 比特币专题研究（持仓报告、CME期货）

❌ **不适合**:
- 真实加密货币交易决策
- 多币种投资组合分析
- DeFi、NFT等新兴领域研究
- 高频量化交易
- 市场深度分析和套利策略

### 总结建议

**AkShare不是加密货币数据分析的首选工具**。如果您的研究重点是：

- 📊 **传统金融**（股票、基金、期货、债券）→ ✅ **AkShare是理想选择**
- 🪙 **加密货币**（多币种、DeFi、NFT）→ ❌ **使用CoinGecko、Binance API或CCXT**

**下一阶段学习建议**: 考虑加密货币接口的局限性，建议将重点转向**AkShare的优势领域**：股票数据、指数数据、基金数据、期货数据等。这些领域AkShare的覆盖面更广、数据质量更高、接口更丰富。

---

**最后更新**: 2026-04-28
**模板版本**: 标准模板 v1.0