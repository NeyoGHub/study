# AkShare 期货数据接口使用指南

> **文档类型**: 使用指南
> **创建日期**: 2026-05-12
> **对应版本**: AkShare 1.18.x

---

## 目录

1. [概述](#概述)
2. [期货品种与主力合约](#期货品种与主力合约)
3. [历史行情](#历史行情)
4. [外盘期货](#外盘期货)
5. [期现价差与库存](#期现价差与库存)
6. [能源与生猪](#能源与生猪)
7. [综合示例](#综合示例)
8. [常见问题](#常见问题)

---

## 概述

AkShare 提供 **121个** 期货相关接口，覆盖国内商品期货、金融期货、外盘期货、期现价差、库存、能源碳交易等。数据源主要来自新浪财经和东方财富。

### 品种代码规则

主力合约代码格式：`品种代码 + 0`，如：
- `RB0` — 螺纹钢主力
- `CU0` — 沪铜主力
- `V0` — PVC主力
- `C0` — 玉米主力

---

## 期货品种与主力合约

```python
import akshare as ak

# 获取品种列表
df_symbols = ak.futures_display_main_sina()

# 主力合约日线
df_rb = ak.futures_main_sina(symbol="RB0")  # 螺纹钢
df_cu = ak.futures_main_sina(symbol="CU0")  # 沪铜
```

**返回字段**: `日期`, `开盘价`, `最高价`, `最低价`, `收盘价`, `成交量`, `持仓量`, `动态结算价`

---

## 历史行情

```python
# 日线数据（新浪）
df_daily = ak.futures_zh_daily_sina(symbol="RB0")

# 分钟数据（5分钟）
df_min = ak.futures_zh_minute_sina(symbol="RB0", period="5")

# 手续费信息
df_fees = ak.futures_comm_js()
```

---

## 外盘期货

```python
# 外盘实时行情
df_cl = ak.futures_foreign_commodity_realtime(symbol="CL")  # 原油
df_gc = ak.futures_foreign_commodity_realtime(symbol="GC")  # 黄金
df_si = ak.futures_foreign_commodity_realtime(symbol="SI")  # 白银

# 外盘合约详情
df_detail = ak.futures_foreign_detail(symbol="ZSD")
```

---

## 期现价差与库存

```python
# 期现价差（282个品种-合约组合）
df_basis = ak.futures_spot_price_daily()

# 交易所库存
df_inv = ak.futures_inventory_em(symbol="a")  # 大豆
df_inv2 = ak.futures_inventory_em(symbol="cu")  # 沪铜
```

---

## 能源与生猪

```python
# 原油价格
df_oil = ak.energy_oil_detail()

# 油价调整历史
df_oil_hist = ak.energy_oil_hist()

# 生猪数据
df_hog = ak.futures_hog_core()
df_hog_cost = ak.futures_hog_cost()
```

---

## 常见问题

### Q1: 如何查找品种代码？

A: `futures_display_main_sina()` 返回所有品种的 symbol/exchange/name。

### Q2: 主力合约代码规则？

A: 品种代码 + 数字0，如RB0(螺纹钢主力)、CU0(沪铜主力)。查询单个合约用具体代码如RB2505。

### Q3: futures_hist_em 连接失败？

A: 该接口依赖东方财富，当前不可用。用 `futures_main_sina`(新浪) 替代。

---

**最后更新**: 2026-05-12
