# AkShare 指数数据接口使用指南

> **文档类型**: 使用指南
> **创建日期**: 2026-05-08
> **对应版本**: AkShare 1.18.x

---

## 目录

1. [概述](#概述)
2. [环境准备](#环境准备)
3. [A股指数数据](#a股指数数据)
4. [港股指数数据](#港股指数数据)
5. [行业指数数据](#行业指数数据)
6. [指数成分股数据](#指数成分股数据)
7. [综合示例](#综合示例)
8. [常见问题](#常见问题)

---

## 概述

AkShare 提供了丰富的指数数据接口，涵盖 A股指数、港股指数、行业指数等，数据源主要来自新浪财经和中证指数公司。本指南系统介绍各类指数接口的使用方法。

### 支持的指数类型

| 指数类型 | 说明 | 主要数据源 |
|---------|------|-----------|
| A股主要指数 | 沪深300、上证50、中证500、科创50、创业板指 | 新浪/东方财富 |
| 指数实时行情 | 562个指数的实时行情 | 新浪 |
| 港股指数 | 恒生指数、国企指数等 | 新浪 |
| 申万行业指数 | 124个申万一级行业 | 东方财富 |
| 中证全指数 | 1406个中证系列指数 | 中证指数公司 |

---

## 环境准备

```bash
# 激活虚拟环境
cd /home/neyo/workspace/code/study/akshare
source venv/bin/activate

# 安装依赖
pip install akshare pandas matplotlib numpy
```

### 数据文件位置

```
/home/neyo/workspace/code/study/akshare/
├── scripts/
│   ├── s1.2_test_index.py        # 指数接口测试脚本
│   └── s1.2_demo_index.py        # 指数数据综合示例
├── output/
│   ├── data/index/          # 指数数据CSV文件
│   └── plots/index/         # 指数图表PNG文件
└── docs/
    └── 指数数据接口使用指南.md  # 本文件
```

---

## A股指数数据

### 指数历史日线数据

```python
import akshare as ak

# 获取沪深300指数历史数据
df_hs300 = ak.index_zh_a_hist(
    symbol="000300",       # 指数代码
    period="daily",        # daily/weekly/monthly
    start_date="20250101", # 起始日期
    end_date="20260507"    # 结束日期
)
```

**参数说明**:

| 参数 | 说明 | 示例值 |
|------|------|--------|
| symbol | 指数代码 | "000300"(沪深300), "000016"(上证50), "000905"(中证500), "000688"(科创50), "399006"(创业板指) |
| period | 周期 | "daily"(日线), "weekly"(周线), "monthly"(月线) |
| start_date | 起始日期 | "20250101" (YYYYMMDD格式) |
| end_date | 结束日期 | "20260507" |
| adjust | 复权方式 | 不适用（指数不需要复权） |

**返回数据字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| 日期 | str | 交易日期 (YYYY-MM-DD) |
| 开盘 | float | 开盘价 |
| 收盘 | float | 收盘价 |
| 最高 | float | 最高价 |
| 最低 | float | 最低价 |
| 成交量 | int64 | 成交量（手） |
| 成交额 | float64 | 成交金额（元） |
| 振幅 | float64 | 涨跌幅 |
| 涨跌幅 | float64 | 涨跌幅（%） |
| 涨跌额 | float64 | 涨跌额 |
| 换手率 | float64 | 换手率（%） |

### 主要指数代码对照表

| 指数名称 | 代码 | 说明 |
|---------|------|------|
| 沪深300 | 000300 | A股大盘蓝筹代表 |
| 上证50 | 000016 | 上海市场前50大 |
| 中证500 | 000905 | A股中盘股代表 |
| 科创50 | 000688 | 科创板代表 |
| 创业板指 | 399006 | 创业板代表 |
| 上证指数 | 000001 | 上海市场综合 |
| 深证成指 | 399001 | 深圳市场综合 |

### 指数实时行情

```python
# 获取所有指数实时行情（562个指数）
spot = ak.stock_zh_index_spot_sina()

# 查看主要指数
key_indices = ['上证指数', '深证成指', '沪深300', '上证50', '中证500', '科创50', '创业板指']
for _, row in spot.iterrows():
    if row['名称'] in key_indices:
        print(f"{row['名称']}: {row['最新价']} ({row['涨跌幅']})")
```

**返回数据字段**:

| 字段 | 说明 |
|------|------|
| 代码 | 指数代码 |
| 名称 | 指数名称 |
| 最新价 | 当前点位 |
| 涨跌额 | 涨跌点数 |
| 涨跌幅 | 涨跌幅（%） |
| 昨收 | 昨日收盘 |
| 今开 | 今日开盘 |
| 最高 | 今日最高 |
| 最低 | 今日最低 |
| 成交量 | 成交量 |
| 成交额 | 成交额 |

---

## 港股指数数据

```python
# 港股指数实时行情（38个指数）
hk_spot = ak.stock_hk_index_spot_sina()

# 恒生指数历史日线
hsi_daily = ak.stock_hk_index_daily_sina(symbol="HSI")
```

**港股指数代码**: HSI(恒生指数), HSCEI(国企指数), HSTECH(恒生科技指数)

---

## 行业指数数据

### 申万行业指数

```python
# 申万行业指数实时行情（124个行业）
realtime_sw = ak.index_realtime_sw()

# 手动计算涨跌幅
realtime_sw['涨跌幅'] = round(
    (realtime_sw['最新价'] - realtime_sw['昨收盘']) / 
    realtime_sw['昨收盘'] * 100, 2
)

# 申万行业指数历史数据
hist_sw = ak.index_hist_sw()

# 申万行业成分股
comp_sw = ak.index_component_sw()
```

### 银河行业指数

```python
# 银河行业指数（11个）
yw_index = ak.index_yw()
```

### 中证全指数列表

```python
# 获取所有中证指数列表（1406个指数）
all_cni = ak.index_all_cni()
```

---

## 指数成分股数据

```python
# 获取沪深300成分股
hs300_stocks = ak.index_stock_cons_sina(symbol="000300")
# 返回300只成分股及其行情数据

# 获取上证50成分股
sz50_stocks = ak.index_stock_cons_sina(symbol="000016")

# 使用中证接口
hs300_cons = ak.index_stock_cons_csindex(symbol="000300")
```

---

## 综合示例

完整示例脚本位于 `scripts/s1.2_demo_index.py`，包含以下功能：

1. **数据获取**: 5个主要A股指数历史数据
2. **实时行情**: 562个指数实时行情
3. **技术指标**: 均线(MA5/10/20/60)、MACD、RSI(14)、布林带
4. **信号识别**: 金叉死叉信号检测
5. **走势对比**: 多指数归一化对比
6. **行业分析**: 申万行业涨跌幅排行
7. **可视化**: 4张专业图表

### 运行方式

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/python scripts/s1.2_demo_index.py
```

### 输出文件

运行后会在以下目录生成数据文件和图表：

```
output/data/index/
├── 指数实时行情_*.csv
├── 沪深300技术指标_*.csv
├── 沪深300金叉死叉信号_*.csv
├── 指数对比分析_*.csv
└── 申万行业行情_*.csv

output/plots/index/
├── 沪深300技术分析_*.png
├── 指数走势对比_*.png
├── 沪深300金叉死叉_*.png
└── 申万行业涨跌幅_*.png
```

### 技术指标计算示例

```python
# 计算均线
df['MA5'] = df['收盘'].rolling(window=5).mean()
df['MA20'] = df['收盘'].rolling(window=20).mean()

# 计算MACD
ema_fast = df['收盘'].ewm(span=12).mean()
ema_slow = df['收盘'].ewm(span=26).mean()
df['DIF'] = ema_fast - ema_slow
df['DEA'] = df['DIF'].ewm(span=9).mean()
df['MACD'] = 2 * (df['DIF'] - df['DEA'])

# 计算RSI
delta = df['收盘'].diff()
gain = delta.where(delta > 0, 0)
loss = (-delta).where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
df['RSI'] = 100 - (100 / (1 + rs))
```

---

## 常见问题

### Q1: index_zh_a_hist 为什么有进度条？

A: 该接口需要分批请求数据，进度条是正常的。如果不需要查看进度，可以设置环境变量 `AKSHARE_PROGRESS=0` 或使用 `warnings.filterwarnings('ignore')`。

### Q2: 某些指数代码查不到数据？

A: 并非所有指数代码都支持。已验证支持的主要指数代码：000300, 000016, 000905, 000688, 399006, 000001, 399001。如需其他指数，可先通过 `stock_zh_index_spot_sina()` 获取所有支持的指数列表。

### Q3: 指数数据是否包含复权？

A: 指数数据本身不需要复权，因为指数已经考虑了成分股变动等因素。直接使用原始数据即可。

### Q4: 申万行业指数没有涨跌幅字段？

A: 是的，`index_realtime_sw()` 返回的数据不包含涨跌幅，需要根据最新价和昨收盘手动计算：
```python
df['涨跌幅'] = (df['最新价'] - df['昨收盘']) / df['昨收盘'] * 100
```

### Q5: 数据获取速度较慢？

A: 由于数据源限制，部分接口（尤其是 `index_zh_a_hist`）获取速度较慢。建议：
- 限制获取的日期范围，避免查询过长时间段
- 使用 `start_date` 参数只获取最近的数据
- 缓存已获取的数据到本地CSV文件

---

## 参考资料

- AkShare官方文档: https://akshare.akfamily.xyz/
- 新浪财经指数: https://finance.sina.com.cn/realstock/company/index_code/sh000300.html
- 申万指数: https://www.swsindex.com/
- 中证指数: https://www.csindex.com.cn/

---

**最后更新**: 2026-05-08
