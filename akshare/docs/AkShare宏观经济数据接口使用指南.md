# AkShare 宏观经济数据接口使用指南 | 2026-05-12

## 中国宏观

| 接口 | 说明 | 数据量 |
|------|------|--------|
| `macro_china_gdp_yearly` | GDP年率 | 61行 |
| `macro_china_cpi` | 居民消费价格指数 | 220行 |
| `macro_china_ppi` | 工业生产者出厂价格指数 | 244行 |
| `macro_china_pmi` | 采购经理人指数 | 220行 |
| `macro_china_lpr` | 贷款市场报价利率 | 1571行 |
| `macro_china_m2_yearly` | M2货币供应量 | 395行 |
| `macro_china_shibor_all` | 上海银行间同业拆放利率 | 2279行 |
| `macro_china_trade_balance` | 贸易顺差 | 565行 |
| `macro_china_gdzctz` | 固定资产投资 | 200行 |
| `macro_china_reserve_requirement_ratio` | 存款准备金率 | 58行 |

## 美国宏观

| 接口 | 说明 |
|------|------|
| `macro_usa_cpi_monthly` | CPI月度(669行) |
| `macro_usa_non_farm` | 非农就业(669行) |
| `macro_usa_unemployment_rate` | 失业率(669行) |
| `macro_usa_ism_pmi` | ISM制造业PMI(671行) |

## 利率与航运

```python
# 各国央行利率
ak.macro_bank_usa_interest_rate()
ak.macro_bank_china_interest_rate()
ak.macro_bank_euro_interest_rate()
ak.macro_bank_japan_interest_rate()

# 航运指数
ak.macro_shipping_bdi()  # 波罗的海干散货指数，9451行
```
