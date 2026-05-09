# AkShare 股票数据接口使用指南

## 文档说明

**文档名称**: AkShare 股票数据接口使用指南
**创建日期**: 2026-04-27
**作者**: Adams
**适用对象**: AkShare初学者、股票数据分析师、量化交易研究者

---

## 目录

1. [概述](#概述)
2. [快速开始](#快速开始)
3. [核心接口详解](#核心接口详解)
4. [演示脚本使用](#演示脚本使用)
5. [实战案例](#实战案例)
6. [常见问题](#常见问题)
7. [最佳实践](#最佳实践)

---

## 概述

### AkShare是什么？

AkShare是一个基于Python的开源金融数据接口库，用于获取中国金融市场数据，包括股票、基金、期货、债券、宏观经济等。

### 为什么选择AkShare？

- **免费开源** - 所有接口完全免费使用
- **数据稳定** - 基于新浪财经等权威数据源
- **中文友好** - 中文文档，国内网络直接访问
- **易于使用** - 统一的API设计，返回Pandas DataFrame
- **功能丰富** - 覆盖股票、基金、期货、指数等多个领域

---

## 快速开始

### 环境安装

```bash
# 安装AkShare
pip install akshare

# 安装依赖
pip install pandas matplotlib
```

### 第一个示例

```python
import akshare as ak

# 获取浦发银行历史数据
df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")
print(df.head())
```

---

## 核心接口详解

### 接口1：获取历史K线数据

**接口名称**: `stock_zh_a_daily`

**功能**: 获取A股历史日K线数据

**参数说明**:
- `symbol`: 股票代码
  - 上交所：sh600000（浦发银行）
  - 深交所：sz002624（完美世界）
- `adjust`: 复权类型
  - `"qfq"`: 前复权（推荐用于技术分析）
  - `"hfq"`: 后复权（推荐用于计算复利）
  - `""`: 不复权（原始价格）

**使用示例**:

```python
import akshare as ak

# 获取浦发银行历史数据（前复权）
df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")

# 获取完美世界历史数据（后复权）
df = ak.stock_zh_a_daily(symbol="sz002624", adjust="hfq")

# 获取最近30天数据
df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")
recent_30 = df.tail(30)
```

**应用场景**:
- 技术指标计算
- 趋势分析
- K线图表制作
- 策略回测

---

### 接口2：获取实时行情数据

**接口名称**: `stock_zh_a_spot`

**功能**: 获取全市场实时行情数据

**参数说明**: 无参数

**使用示例**:

```python
import akshare as ak

# 获取全市场实时行情
df = ak.stock_zh_a_spot()

# 涨幅榜TOP10
top_gainers = df.nlargest(10, '涨跌幅')

# 跌幅榜TOP10
top_losers = df.nsmallest(10, '涨跌幅')

# 成交额TOP10
top_by_amount = df.nlargest(10, '成交额')
```

**应用场景**:
- 市场行情监控
- 涨跌幅分析
- 热点板块追踪
- 选股筛选

---

### 接口3：获取分钟级数据

**接口名称**: `stock_zh_a_minute`

**功能**: 获取分钟级K线数据

**参数说明**:
- `symbol`: 股票代码
- `period`: 分钟周期（1/5/15/30/60）
- `adjust`: 复权类型（默认不复权）

**使用示例**:

```python
import akshare as ak

# 获取5分钟K线
df = ak.stock_zh_a_minute(symbol="sh600000", period="5")

# 获取1分钟K线
df = ak.stock_zh_a_minute(symbol="sz002624", period="1")
```

**应用场景**:
- 日内交易分析
- 高频交易研究
- 短期价格波动分析

---

### 接口4：获取指数实时数据

**接口名称**: `stock_zh_index_spot_sina`

**功能**: 获取A股指数实时行情

**参数说明**: 无参数

**使用示例**:

```python
import akshare as ak

# 获取所有指数实时行情
df = ak.stock_zh_index_spot_sina()

# 查看主要指数
major_indices = df[df['指数名称'].str.contains('上证|深证|创业板')]
print(major_indices)
```

**应用场景**:
- 市场大盘分析
- 指数走势监控
- 市场情绪判断

---

## 演示脚本使用

### 脚本概述

本指南配套的演示脚本 `s1.1_demo_stock.py` 提供了完整的示例代码，涵盖所有核心接口的使用方法。

### 脚本功能

演示脚本包含6个主要功能模块：

1. **获取单只股票历史数据**
2. **获取全市场实时行情**
3. **获取分钟级数据**
4. **获取指数实时数据**
5. **技术分析和可视化**
6. **数据分析**

### 运行脚本

```bash
# 进入项目目录
cd /home/neyo/workspace/code/study/akshare

# 运行演示脚本
python scripts/s1.1_demo_stock.py
```

### 脚本输出

运行脚本后会生成以下文件：

```
output/
├── 浦发银行历史数据.csv
├── 全市场实时行情.csv
├── 浦发银行5分钟数据.csv
├── 指数实时行情.csv
└── 技术分析图表.png
```

---

## 实战案例

### 案例1：技术指标计算

```python
import akshare as ak

# 获取浦发银行历史数据
df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")

# 计算移动平均线
df['MA5'] = df['收盘'].rolling(window=5).mean()
df['MA10'] = df['收盘'].rolling(window=10).mean()
df['MA20'] = df['收盘'].rolling(window=20).mean()

# 查看最新数据
print(df[['日期', '收盘', 'MA5', 'MA10', 'MA20']].tail(10))
```

### 案例2：金叉死叉识别

```python
import akshare as ak

# 获取历史数据
df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")

# 计算移动平均线
df['MA5'] = df['收盘'].rolling(window=5).mean()
df['MA10'] = df['收盘'].rolling(window=10).mean()

# 识别金叉（MA5上穿MA10）
golden_cross = (df['MA5'] > df['MA10']) & (df['MA5'].shift(1) < df['MA10'].shift(1))

# 识别死叉（MA5下穿MA10）
death_cross = (df['MA5'] < df['MA10']) & (df['MA5'].shift(1) > df['MA10'].shift(1))

# 打印信号
print("金叉信号:")
print(df[golden_cross][['日期', '收盘', 'MA5', 'MA10']])

print("\n死叉信号:")
print(df[death_cross][['日期', '收盘', 'MA5', 'MA10']])
```

### 案例3：涨幅榜监控

```python
import akshare as ak

# 获取实时行情
df = ak.stock_zh_a_spot()

# 涨幅榜TOP10
top_gainers = df.nlargest(10, '涨跌幅')

# 筛选条件：涨幅>5%且成交额>1亿
hot_stocks = df[(df['涨跌幅'] > 5) & (df['成交额'] > 100000000)]

print("热门股票:")
print(hot_stocks[['代码', '名称', '最新价', '涨跌幅', '成交额']].head(20))
```

---

## 常见问题

### Q1: 股票代码格式是什么？

**A**: 股票代码格式为：
- 上交所：sh + 6位数字（如sh600000）
- 深交所：sz + 6位数字（如sz002624）

### Q2: 什么是复权？什么时候用？

**A**: 复权是为了消除分红、拆股等对股价的影响：
- 前复权（qfq）：技术分析推荐使用
- 后复权（hfq）：计算收益率和复利推荐使用
- 不复权：查看历史原始价格

### Q3: 如何获取多只股票的数据？

**A**: 使用循环逐个获取：

```python
import akshare as ak

stocks = ['sh600000', 'sz002624', 'sh600036']
all_data = []

for symbol in stocks:
    df = ak.stock_zh_a_daily(symbol=symbol, adjust="qfq")
    df['股票代码'] = symbol
    all_data.append(df)

result = pd.concat(all_data, ignore_index=True)
```

### Q4: 数据更新频率是多少？

**A**:
- 历史K线：日频更新
- 实时行情：实时更新（交易时间内）
- 分钟数据：分钟级更新

### Q5: 如何处理数据缺失？

**A**:

```python
# 检查缺失值
print(df.isnull().sum())

# 删除缺失值
df = df.dropna()

# 填充缺失值
df = df.fillna(method='ffill')
```

---

## 最佳实践

### 1. 数据保存

```python
# 保存为CSV
df.to_csv('data.csv', index=False, encoding='utf-8-sig')

# 保存为Excel
df.to_excel('data.xlsx', index=False)

# 保存为Parquet（高效）
df.to_parquet('data.parquet')
```

### 2. 数据可视化

```python
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制价格走势
plt.figure(figsize=(12, 6))
plt.plot(df['日期'], df['收盘'])
plt.title('浦发银行价格走势')
plt.xlabel('日期')
plt.ylabel('价格')
plt.xticks(rotation=45)
plt.show()
```

### 3. 异常处理

```python
import akshare as ak

try:
    df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")
    print("数据获取成功")
except Exception as e:
    print(f"数据获取失败: {e}")
```

### 4. 性能优化

```python
# 批量获取数据
symbols = ['sh600000', 'sz002624', 'sh600036']
# 使用多线程或异步IO提高效率

# 只获取需要的数据
df = ak.stock_zh_a_daily(symbol="sh600000", adjust="qfq")
recent_30 = df.tail(30)  # 只用最近30天
```

---

## 总结

本文档介绍了AkShare股票数据接口的核心功能和使用方法：

✓ **4个核心接口**
- 历史K线数据
- 实时行情数据
- 分钟级数据
- 指数实时数据

✓ **完整演示脚本**
- 6个功能模块
- 实用代码示例
- 可直接运行

✓ **实战案例**
- 技术指标计算
- 金叉死叉识别
- 涨幅榜监控

✓ **最佳实践**
- 数据保存方法
- 可视化技巧
- 性能优化建议

**下一步**: 尝试运行演示脚本，探索更多功能！

---

**文档完成日期**: 2026-04-27
**作者**: Adams
**联系方式**: 如有问题，请查阅AkShare官方文档