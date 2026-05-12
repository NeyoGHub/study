# AkShare 额外数据类别参考（路线图之外）

按用户需求研究以下9类数据，验证其可用性和数据量。

---

## 1. 龙虎榜数据（16个接口）

| 接口 | 功能 | 数据量 | 状态 |
|------|------|:------:|:----:|
| `stock_lhb_detail_em` | 龙虎榜详情 | 637条 | ✅ |
| `stock_lhb_hyyyb_em` | 营业部排行 | 276条 | ✅ |
| `stock_lhb_jgstatistic_em` | 机构统计 | — | ✅ |
| `stock_lhb_ggtj_sina` | 个股上榜统计 | — | ✅ |
| `stock_lhb_jgmx_sina` | 机构买卖明细 | — | ✅ |

```python
# 龙虎榜当日上榜股票
df = ak.stock_lhb_detail_em()
print(df[['代码', '名称', '上榜日', '上榜原因']].head(10))
```

---

## 2. 融资融券数据（11个接口）

| 接口 | 功能 | 数据量 | 状态 |
|------|------|:------:|:----:|
| `stock_margin_sse` | 上交所融资融券 | 2000行 | ✅ |
| `stock_margin_szse` | 深交所融资融券 | — | ✅ |
| `stock_margin_detail_sse` | 上交所个股明细 | — | ✅ |
| `stock_margin_detail_szse` | 深交所个股明细 | — | ✅ |
| `stock_margin_account_info` | 信用账户信息 | — | ✅ |

```python
# 上交所融资余额历史
df = ak.stock_margin_sse()
print(df[['信用交易日期', '融资余额', '融资买入额']].tail())
```

---

## 3. 沪深港通数据（10个接口）

| 接口 | 功能 | 数据量 | 状态 |
|------|------|:------:|:----:|
| `stock_hsgt_hist_em` | 沪深港通历史 | 2666行 | ✅ |
| `stock_hsgt_sh_hk_spot_em` | 沪股通实时 | — | ✅ |
| `stock_hsgt_hold_stock_em` | 持股明细 | — | ✅ |
| `stock_hsgt_individual_em` | 个股资金流向 | — | ✅ |
| `stock_hsgt_board_rank_em` | 板块排行 | — | ✅ |

```python
# 沪深港通资金流向历史
df = ak.stock_hsgt_hist_em()
print(f'共 {len(df)} 条记录')
```

---

## 4. 能源数据（11个接口）

已在阶段3.1期货中覆盖，核心接口：

| 接口 | 功能 | 状态 |
|------|------|:----:|
| `energy_oil_detail` | 原油价格（31行） | ✅ |
| `energy_oil_hist` | 油价调整历史（320行） | ✅ |
| `energy_carbon_bj` | 北京碳交易 | ✅ |
| `energy_carbon_domestic` | 全国碳交易 | ✅(慢) |
| `energy_carbon_eu` | 欧盟碳交易 | ✅ |

---

## 5. 利率数据（12个接口）

已在阶段4.1宏观经济中覆盖大部分：

| 接口 | 功能 | 状态 |
|------|------|:----:|
| `macro_bank_usa_interest_rate` | 美联储利率 | ✅ 294行 |
| `macro_bank_china_interest_rate` | 中国基准利率 | ✅ 218行 |
| `macro_bank_euro_interest_rate` | 欧央行利率 | ✅ 279行 |
| `macro_bank_japan_interest_rate` | 日本利率 | ✅ |
| `repo_rate_hist` | 回购利率历史 | ✅ |
| `repo_rate_query` | 回购利率查询 | ✅ |

---

## 6. 空气质量数据（7个接口）

| 接口 | 功能 | 数据量 | 状态 |
|------|------|:------:|:----:|
| `air_quality_rank` | AQI排名 | 168城市 | ✅ |
| `air_quality_hist` | 历史AQI | — | ✅ |
| `air_quality_hebei` | 河北空气质量 | — | ✅ |
| `air_city_table` | 城市列表 | — | ✅ |
| `air_quality_watch_point` | 监测点数据 | — | ✅ |

```python
# 全国空气质量排名
df = ak.air_quality_rank()
print(df.head(10))
```

---

## 7. 汽车市场数据（13个接口）

| 接口 | 功能 | 数据量 | 状态 |
|------|------|:------:|:----:|
| `car_sale_rank_gasgoo` | 厂商销量排行 | 50条 | ✅ |
| `car_market_total_cpca` | 总销量 | — | ✅ |
| `car_market_cate_cpca` | 按类别 | — | ✅ |
| `car_market_country_cpca` | 按国别 | — | ✅ |
| `car_market_segment_cpca` | 按细分市场 | — | ✅ |

```python
# 汽车厂商销量排行
df = ak.car_sale_rank_gasgoo()
print(df.head())
```

---

## 8. 财富榜单数据（6个接口）

| 接口 | 功能 | 状态 |
|------|------|:----:|
| `forbes_rank` | 福布斯排行 | ⏳ |
| `hurun_rank` | 胡润排行 | ⏳ |
| `xincaifu_rank` | 新财富排行 | ⏳ |
| `index_bloomberg_billionaires` | 彭博富豪榜 | ⏳ |

> 注：财富榜单接口数据源较慢，部分需要网络重试

---

## 9. 电影票房数据（9个接口）

| 接口 | 功能 | 状态 |
|------|------|:----:|
| `movie_boxoffice_realtime` | 实时票房 | ❌ 解密失败 |
| `movie_boxoffice_daily` | 日票房 | ❌ 解密失败 |
| `movie_boxoffice_weekly` | 周票房 | ❌ 解密失败 |
| `movie_boxoffice_yearly` | 年票房 | ❌ 解密失败 |

> 注：艺恩数据源加密方式变更，所有 movie_boxoffice_* 接口当前不可用

---

## 总结

| 类别 | 接口数 | 可用状态 | 推荐度 |
|------|:------:|:--------:|:------:|
| 龙虎榜 | 16 | ✅ 全部可用 | ⭐⭐⭐⭐⭐ |
| 融资融券 | 11 | ✅ 全部可用 | ⭐⭐⭐⭐⭐ |
| 沪深港通 | 10 | ✅ 全部可用 | ⭐⭐⭐⭐⭐ |
| 能源/碳 | 11 | ✅ 可用（部分慢） | ⭐⭐⭐⭐ |
| 利率/回购 | 14 | ✅ 全部可用 | ⭐⭐⭐⭐ |
| 空气质量 | 7 | ✅ 全部可用 | ⭐⭐⭐ |
| 汽车市场 | 13 | ✅ 全部可用 | ⭐⭐⭐ |
| 财富榜单 | 6 | ⏳ 可用但慢 | ⭐⭐ |
| 电影票房 | 9 | ❌ 艺恩加密变更 | ⭐ |

> 行情/龙虎榜/融资融券/沪深港通主要为东方财富数据源，当前行情接口可用，部分分析接口可能存在连接问题。具体以实际测试为准。

**最后更新**: 2026-05-13
