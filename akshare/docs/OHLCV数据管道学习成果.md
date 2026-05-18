# OHLCV 数据管道学习成果

> 完成日期: 2026-05-17
> 阶段: 9.1 — 量化数据基础设施

---

## 一、学习收获

### 1.1 掌握双数据源架构

理解并实现了加密货币 OHLCV 数据的**双源融合策略**：

```
                    ┌─────────────────┐
                    │   基础数据层      │
                    ├─────────────────┤
                    │ OKX (CCXT)      │ ← 实时、高频、无限频
                    │ CoinGecko API   │ ← 历史、全市场、聚合价
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   数据融合层      │
                    ├─────────────────┤
                    │ 对齐 normalize() │
                    │ 合并 concat()    │
                    │ 去重 duplicated()│
                    │ 差异 diff_pct()  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   应用层          │
                    ├─────────────────┤
                    │ CSV持久化         │
                    │ 技术指标计算       │
                    │ 可视化输出         │
                    └─────────────────┘
```

### 1.2 理解数据源差异的本质

| 差异维度 | 原因 | 影响 |
|:--------:|:----:|:----:|
| 价格差异 | OKX单一交易所 vs CG聚合价格 | 差异<0.1%，可忽略 |
| 成交量差异 | 各交易所深度不同 | 需明确数据源用途 |
| K线时间差 | 时区处理不同 | 对齐到UTC日期 |
| 历史深度 | 交易所限制 vs API限制 | OKX近期+CG历史 |

**核心认知**: 没有"完美"的数据源，关键是理解差异来源，选择适合自己场景的策略。

### 1.3 CCXT 库深入

CCXT 不仅提供交易功能，其 `fetch_ohlcv` 方法是对接交易所OHLCV数据的统一接口：

```python
# 统一接口，100+交易所通用
exchange.fetch_ohlcv(symbol, timeframe, since, limit)

# 参数说明
symbol    = "BTC/USDT"       # 交易对格式统一
timeframe = "1d"             # 周期标准化
since     = 1704067200000    # Unix毫秒时间戳
limit     = 100              # 返回条数上限
```

OKX 有效，是因为 CCXT 自动处理了 OKX API 的参数转换、签名和错误重试。

### 1.4 技术指标工程化

将传统技术指标（均线/MACD/RSI/布林带/ATR）封装为可复用的计算函数：

```python
def compute_indicators(df):
    """单次调用计算全部指标"""
    # MA → MACD → RSI → BOLL → ATR → Signal
    return df
```

---

## 二、关键技术点

### 2.1 数据对齐

两个数据源的时间戳精度不同：
- OKX: 毫秒时间戳，带时区
- CoinGecko: 毫秒时间戳，UTC

对齐方法：
```python
# 标准化到日期
df.index = df.index.normalize()

# 去重（OKX优先）
merged = merged[~merged.index.duplicated(keep="first")]
```

### 2.2 限频处理

CoinGecko 免费层限制10-30次/分钟：
```python
time.sleep(2.5)  # 每次请求后休眠
# 或使用指数退避
```

OKX (CCXT) 无严格限频，但建议：
```python
ex = ccxt.okx({"enableRateLimit": True})  # CCXT内置限频
```

### 2.3 K线周期与数据量的关系

```python
# OKX默认limit=500，可通过since参数分段获取
# CoinGecko通过days参数控制
days=1   → 分钟K，~288条
days=7   → 30分钟K，~336条
days=30  → 4小时K，~180条
days=90  → 4小时K，~540条
days=max → 日K，数年数据
```

---

## 三、成果清单

### 3.1 脚本

| 文件 | 说明 |
|:----|:-----|
| `scripts/s9.1_demo_ohlcv_pipeline.py` | OHLCV双源融合管道（含技术分析+可视化） |

### 3.2 文档

| 文件 | 说明 |
|:----|:-----|
| `docs/OHLCV数据管道使用指南.md` | API使用方法和代码示例 |
| `docs/OHLCV数据管道演示总结.md` | 测试结果和数据对比 |
| `docs/OHLCV数据管道学习成果.md` | 学习收获和技术要点 |

### 3.3 数据输出

| 文件 | 内容 |
|:----|:-----|
| `output/data/crypto/ohlcv_merged_*.csv` | 双源融合数据 |
| `output/data/crypto/ohlcv_okx_*_1d_*.csv` | OKX日K线 |
| `output/data/crypto/ohlcv_okx_*_1h_*.csv` | OKX 1小时K线 |
| `output/data/crypto/ohlcv_okx_*_4h_*.csv` | OKX 4小时K线 |
| `output/data/crypto/ohlcv_coingecko_*_*.csv` | CoinGecko OHLCV |

### 3.4 图表

| 文件 | 内容 |
|:----|:-----|
| `output/plots/crypto/ohlcv_data_comparison_*.png` | 双源对比+多周期 |
| `output/plots/crypto/ohlcv_technical_analysis_*.png` | 技术分析全景图 |
| `output/plots/crypto/ohlcv_source_comparison_*.png` | 数据源质量对比 |

---

## 四、量化交易数据体系构建

### 4.1 数据分层架构

```
┌──────────────────────────────────────────────────────┐
│                  应用层                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ 策略回测 │  │ 实盘执行 │  │ 风险监控 │  │ 报告分析 │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘ │
├───────┴────────────┴────────────┴────────────┴───────┤
│                  数据服务层                           │
│  ┌──────────────────────────────────────────────────┐│
│  │  技术指标引擎 (MA/MACD/RSI/BOLL/ATR/Signal)     ││
│  └──────────────────────┬───────────────────────────┘│
├─────────────────────────┴────────────────────────────┤
│                  数据管道层                           │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐ │
│  │  OKX(CCXT)  │  │ CoinGecko  │  │ SQLite持久化  │ │
│  └─────────────┘  └─────────────┘  └──────────────┘ │
└──────────────────────────────────────────────────────┘
```

### 4.2 从数据到交易

```
OHLCV数据 → 技术指标 → 策略信号 → 资金管理 → 执行下单
    ↑          ↑           ↑          ↑          ↑
  数据管道    计算引擎   策略逻辑    风控规则   CCXT交易
```

### 4.3 可用交易所对比（中国网络环境）

| 交易所 | OHLCV | 交易API | 免费 | 需要KYC |
|:------:|:-----:|:-------:|:----:|:-------:|
| **OKX** | ✅ | ✅ | ✅ | ⚠ 需 |
| KuCoin | ✅ | ✅ | ✅ | ⚠ 需 |
| MEXC | ✅ | ✅ | ✅ | ⚠ 需 |

---

## 五、后续规划

### 阶段9.2: 策略回测引擎
- 基于管道数据实现回测框架
- 支持多策略并行回测
- 绩效指标（夏普/最大回撤/胜率）

### 阶段9.3: 模拟交易系统
- OKX模拟盘下单
- 实时信号+自动执行
- Telegram/飞书通知

### 阶段9.4: 实盘交易
- 风控模块（止损/仓位管理）
- 多账户管理
- 日志+审计

---

## 六、参考资料

1. CCXT 文档: https://docs.ccxt.com/
2. CoinGecko API: https://docs.coingecko.com/
3. OKX API: https://www.okx.com/api-v5
4. Pandas OHLCV: https://pandas.pydata.org/
5. Matplotlib: https://matplotlib.org/
