# AkShare 基金数据接口使用指南

> **文档类型**: 使用指南
> **创建日期**: 2026-05-09
> **对应版本**: AkShare 1.18.x

---

## 目录

1. [概述](#概述)
2. [环境准备](#环境准备)
3. [基金基础信息](#基金基础信息)
4. [开放式基金数据](#开放式基金数据)
5. [ETF基金数据](#etf基金数据)
6. [基金持仓分析](#基金持仓分析)
7. [基金管理人与评级](#基金管理人与评级)
8. [综合示例](#综合示例)
9. [常见问题](#常见问题)

---

## 概述

AkShare 提供了丰富的基金数据接口，涵盖基金基础信息、开放式基金、ETF、基金持仓、基金管理人和评级等。本指南系统介绍核心基金接口的使用方法。

### 支持的基金数据类型

| 数据类型 | 说明 | 主要数据源 |
|---------|------|-----------|
| 基金列表 | 26666只全市场基金基本信息 | 东方财富 |
| 净值数据 | 单只基金净值历史/全市场日线 | 东方财富 |
| 基金排行 | 按收益率、规模等多维度排行 | 东方财富 |
| ETF行情 | ETF/LOF实时行情、分类 | 同花顺/新浪 |
| 基金持仓 | 持仓明细、变动、行业配置 | 东方财富 |
| 基金管理人 | 基金经理信息、业绩 | 东方财富 |
| 基金评级 | 多机构评级数据 | 东方财富 |

---

## 环境准备

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/python -c "import akshare as ak; print(ak.__version__)"
```

### 数据文件位置

```
/home/neyo/workspace/code/study/akshare/
├── scripts/
│   ├── s2.1_test_fund.py      # 基金接口测试脚本
│   └── s2.1_demo_fund.py      # 基金数据综合示例
├── output/
│   ├── data/fund/             # 基金数据CSV文件
│   └── plots/fund/            # 基金图表PNG文件
└── docs/
    └── AkShare基金数据接口使用指南.md  # 本文件
```

---

## 基金基础信息

```python
import akshare as ak

# 获取全市场基金列表（26666只）
df_fund_list = ak.fund_name_em()
print(f"共 {len(df_fund_list)} 只基金")
print(df_fund_list.head())
```

**返回字段**:

| 字段 | 说明 |
|------|------|
| 基金代码 | 6位基金代码 |
| 拼音缩写 | 基金名称拼音首字母 |
| 基金简称 | 基金中文名称 |
| 基金类型 | 如"混合型-灵活"、"指数型-股票"等 |
| 拼音全称 | 基金名称全拼音 |

---

## 开放式基金数据

### 单只基金净值历史

```python
# 获取华夏成长混合(000001)净值历史
df_nav = ak.fund_open_fund_info_em(symbol="000001")
print(f"共 {len(df_nav)} 条净值记录")
print(df_nav.tail())
```

**参数**:
- `symbol`: 基金代码（6位数字）

**返回字段**: `净值日期`, `单位净值`, `日增长率`

### 全部基金日线

```python
# 获取所有开放基金最新净值日线
df_all = ak.fund_open_fund_daily_em()
print(f"共 {len(df_all)} 只基金")
```

### 基金排行

```python
# 获取基金排行数据
df_rank = ak.fund_open_fund_rank_em()
# 按收益率排序
top_weekly = df_rank.nlargest(10, '近1周')
print(top_weekly[['基金代码', '基金简称', '近1周', '近1月', '近1年']])
```

**返回字段**: `序号`, `基金代码`, `基金简称`, `日期`, `单位净值`, `累计净值`, `日增长率`, `近1周`, `近1月`, `近3月`, `近6月`, `近1年`, `近2年`, `近3年`, `今年来`, `成立来`

---

## ETF基金数据

### ETF实时行情

```python
# 同花顺ETF行情（1560只ETF）
df_etf = ak.fund_etf_spot_ths()

# 新浪ETF分类行情（1504只ETF）
df_etf_sina = ak.fund_etf_category_sina(symbol="ETF基金")

# 新浪LOF基金行情（382只LOF）
df_lof = ak.fund_etf_category_sina(symbol="LOF基金")

# ETF涨跌幅排行
top_etf = df_etf_sina.nlargest(10, '涨跌幅')
print(top_etf[['名称', '最新价', '涨跌幅']])
```

### ETF历史数据

```python
# 上证50ETF(510050)历史日线
# 优先使用东方财富接口
df_etf_hist = ak.fund_etf_hist_em(
    symbol="510050", period="daily",
    start_date="20250101", end_date="20260507"
)

# 若不可用，回退到股票日线接口(ETF像股票一样交易)
df_etf_hist2 = ak.stock_zh_a_daily(symbol="sh510050", adjust="qfq")
```

---

## 基金持仓分析

### 持仓明细

```python
# 获取华夏成长混合(000001)持仓明细
df_hold = ak.fund_portfolio_hold_em(symbol="000001")
print(f"共 {len(df_hold)} 条持仓记录")
print(df_hold.head())

# 获取持仓变动
df_change = ak.fund_portfolio_change_em(symbol="000001")

# 获取行业配置
df_industry = ak.fund_portfolio_industry_allocation_em(symbol="000001")
```

**返回字段（持仓明细）**:

| 字段 | 说明 |
|------|------|
| 序号 | 持仓排名 |
| 股票代码 | 持股代码 |
| 股票名称 | 持股名称 |
| 占净值比例 | 占基金净值百分比 |
| 持股数 | 持股数量（万股） |
| 持仓市值 | 持仓市值（万元） |
| 季度 | 报告期 |

---

## 基金管理人与评级

### 基金经理

```python
# 获取全部基金经理信息（34326条）
df_manager = ak.fund_manager_em()

# 按管理规模排序
top_managers = df_manager.nlargest(10, '现任基金资产总规模')
print(top_managers[['姓名', '所属公司', '现任基金资产总规模', '现任基金最佳回报']])
```

### 基金评级

```python
# 获取基金评级数据（15917只）
df_rating = ak.fund_rating_all()

# 筛选5星基金
five_star = df_rating[df_rating['5星评级家数'] >= 3]
print(f"获得3家以上5星评级的基金: {len(five_star)} 只")
```

### 基金估值

```python
# 获取基金实时估值（20000只）
df_est = ak.fund_value_estimation_em()
# 按估算增长率排序
hot_funds = df_est.nlargest(10, '2026-05-08-估算数据-估算增长率')
```

---

## 综合示例

完整示例脚本位于 `scripts/s2.1_demo_fund.py`，包含以下功能：

1. **基金总览**: 全市场基金列表及类型分布
2. **基金排行**: TOP基金筛选和可视化
3. **净值分析**: 单只基金净值走势+技术指标
4. **ETF市场**: ETF涨跌幅排行
5. **持仓分析**: 持仓饼图+柱状图
6. **基金经理**: 规模/业绩排行
7. **评级估值**: 多维度补充分析

### 运行方式

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/python scripts/s2.1_demo_fund.py
```

### 输出文件

```
output/data/fund/
├── 基金列表_*.csv
├── 基金排名_*.csv
├── 000001华夏成长净值_*.csv
├── ETF市场行情_*.csv
├── 000001华夏成长持仓_*.csv
├── 基金经理列表_*.csv
├── 基金评级_*.csv
└── 基金估值_*.csv

output/plots/fund/
├── 基金周涨幅TOP30_*.png
├── 000001华夏成长净值走势_*.png
├── ETF涨跌幅TOP30_*.png
├── 000001华夏成长持仓饼图_*.png
└── 000001华夏成长持仓柱状图_*.png
```

---

## 常见问题

### Q1: fund_etf_hist_em 获取失败？

A: 该接口依赖东方财富数据源，当前可能不可用。可回退到 `stock_zh_a_daily(symbol="sh510050", adjust="qfq")` 获取ETF历史数据。

### Q2: fund_scale_open_sina 报错？

A: 该接口存在AkShare内部列名bug，属于库本身的问题。等待库更新修复即可。

### Q3: 如何查找特定基金代码？

A: 使用 `fund_name_em()` 获取全市场基金列表后，可按基金简称搜索：
```python
df = ak.fund_name_em()
df[df['基金简称'].str.contains('沪深300')]
```

### Q4: 数据更新频率？

A: 净值数据每日更新（交易日），实时估值盘中更新，持仓数据按季度更新。

---

## 参考资料

- AkShare官方文档: https://akshare.akfamily.xyz/
- 东方财富基金: https://fund.eastmoney.com/
- 新浪基金: https://finance.sina.com.cn/fund/

---

**最后更新**: 2026-05-09
