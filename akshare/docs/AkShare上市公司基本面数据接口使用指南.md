# AkShare 上市公司基本面数据接口使用指南

> **文档类型**: 使用指南
> **创建日期**: 2026-05-09
> **对应版本**: AkShare 1.18.x

---

## 目录

1. [概述](#概述)
2. [公司基本信息](#公司基本信息)
3. [财务数据](#财务数据)
4. [业绩报表与预告](#业绩报表与预告)
5. [分红送配](#分红送配)
6. [股本股东与限售](#股本股东与限售)
7. [全市场估值](#全市场估值)
8. [综合示例](#综合示例)
9. [常见问题](#常见问题)

---

## 概述

AkShare 提供 **95个** 上市公司基本面相关接口，涵盖公司信息、财务数据、业绩、分红、股东、估值等。数据源主要来自东方财富和同花顺。

### 数据源特点

| 数据源 | 优势 | 劣势 |
|--------|------|------|
| **东方财富** | 财务摘要和历史数据完整 | 三张报表接口当前有bug |
| **同花顺(THS)** | 三张报表数据稳定可用 | 字段命名较复杂 |

---

## 公司基本信息

```python
import akshare as ak

# 全部A股列表（5513只）
df_all = ak.stock_info_a_code_name()

# 沪市详情（1703只，含上市日期）
df_sh = ak.stock_info_sh_name_code()

# 深市详情（2889只，含板块/行业/股本）
df_sz = ak.stock_info_sz_name_code()
print(df_sz['所属行业'].value_counts().head(10))  # 行业分布
```

---

## 财务数据

### 财务摘要

```python
# 东方财富版本（80行指标，124个时间列）
df = ak.stock_financial_abstract(symbol="000001")
# 行：利润、营收、ROE等常用指标
# 列：各报告期数据

# 同花顺版本（121行，更详细）
df_ths = ak.stock_financial_abstract_ths(symbol="000001")
```

### 财务分析指标

```python
# 86个财务指标
df = ak.stock_financial_analysis_indicator(symbol="000001", start_year="2023")
print(df[['日期', '摊薄每股收益(元)', '加权每股收益(元)',
          '每股净资产_调整前(元)', '每股经营性现金流(元)']])
```

### 三张报表（同花顺）

```python
# 利润表（121行）
df_profit = ak.stock_financial_benefit_ths(symbol="000001")

# 资产负债表（118行）
df_balance = ak.stock_financial_debt_ths(symbol="000001")

# 现金流量表（103行）
df_cash = ak.stock_financial_cash_ths(symbol="000001")
```

---

## 业绩报表与预告

```python
# 业绩报表（5093只股票的最新业绩）
df_yjbb = ak.stock_yjbb_em()
# 按每股收益排序
top_eps = df_yjbb.nlargest(10, '每股收益')
print(top_eps[['股票简称', '每股收益', '净利润-净利润']])

# 业绩预告（2700只股票）
df_forecast = ak.stock_profit_forecast_em()
```

---

## 分红送配

```python
# 单只股票分红明细
df_fhps = ak.stock_fhps_detail_em(symbol="000001")
# 报告期、送转比例、现金分红比例

# 全市场分红列表（3859只）
df_all_fhps = ak.stock_fhps_em()
```

---

## 股本股东与限售

```python
# 限售解禁
df_restricted = ak.stock_restricted_release_queue_em()

# 股东变动
df_holder = ak.stock_shareholder_change_ths(symbol="000001")
```

---

## 全市场估值

```python
# 全市场市盈率（5176只，TTM）
df_pe = ak.stock_a_ttm_lyr()

# 全市场市净率（5174只）
df_pb = ak.stock_a_all_pb()
```

---

## 综合示例

完整示例脚本位于 `scripts/s1.3_demo_fundamental.py`：

1. **行业分布** — 深市公司行业分类饼图
2. **财务指标** — ROE+EPS趋势图
3. **净利润趋势** — 净利润走势图
4. **业绩排名** — EPS排行柱状图
5. **分红历史** — 分红送配柱状图
6. **全市场估值** — PE/PB散点图+分布图

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/python scripts/s1.3_demo_fundamental.py
```

---

**最后更新**: 2026-05-09
