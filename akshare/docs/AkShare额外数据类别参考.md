# AkShare 额外数据类别 - 快速参考

> **最后更新**: 2026-05-13
> **覆盖**: 龙虎榜、融资融券、沪深港通、空气质量、汽车数据、电影票房、能源、利率、财富榜单

---

## 阶段六：龙虎榜+融资融券+沪深港通

**测试脚本**: `scripts/s6.1_test_market_micro.py`

### 龙虎榜（16个接口）

```python
df = ak.stock_lhb_detail_em()       # 龙虎榜详情（637条）
df2 = ak.stock_lhb_hyyyb_em()       # 营业部排行（276条）
df3 = ak.stock_lhb_jgstatistic_em() # 机构统计
df4 = ak.stock_lhb_ggtj_sina()      # 个股上榜统计
```

### 融资融券（11个接口）

```python
df = ak.stock_margin_sse()          # 上交所两融（2000行）
df2 = ak.stock_margin_szse()        # 深交所两融
df3 = ak.stock_margin_detail_sse()  # 上交所个股明细
df4 = ak.stock_margin_detail_szse() # 深交所个股明细
df5 = ak.stock_margin_account_info()# 信用账户信息
```

### 沪深港通（10个接口）

```python
df = ak.stock_hsgt_hist_em()        # 资金流向历史（2666行）
df2 = ak.stock_hsgt_hold_stock_em() # 持股明细
df3 = ak.stock_hsgt_individual_em() # 个股资金流向
df4 = ak.stock_hsgt_board_rank_em() # 板块排行
```

---

## 阶段七：空气质量+汽车数据+电影

**测试脚本**: `scripts/s7.1_test_alternative.py`

### 空气质量（7个接口）

```python
df = ak.air_quality_rank()          # AQI排名（168城市）
df2 = ak.air_quality_hist()         # 历史AQI
df3 = ak.air_city_table()           # 城市列表
```

### 汽车市场（13个接口）

```python
df = ak.car_sale_rank_gasgoo()      # 厂商销量排行（50条）
df2 = ak.car_market_total_cpca()    # 总销量
df3 = ak.car_market_cate_cpca()     # 按类别统计
```

### 财富榜单（6个接口）

```python
df = ak.forbes_rank()               # 福布斯排行榜
df2 = ak.hurun_rank()               # 胡润排行榜（1240条）
df3 = ak.xincaifu_rank()            # 新财富排行
```

### 电影票房（9个接口）— 全部不可用

艺恩数据源加密变更，全部 `JSONDecodeError`：

| 接口 | 状态 |
|------|:----:|
| `movie_boxoffice_realtime` | ❌ |
| `movie_boxoffice_daily` | ❌ |
| `movie_boxoffice_weekly` | ❌ |
| `movie_boxoffice_yearly` | ❌ |

> 建议: 等待AkShare库更新，或使用猫眼/灯塔API

---

## 阶段八：能源+利率

**测试脚本**: `scripts/s8.1_test_other.py`

### 能源/碳交易（11个接口）— 补充3.1期货

```python
df = ak.energy_oil_detail()         # 原油价格
df2 = ak.energy_oil_hist()          # 油价调整历史（320行）
df3 = ak.energy_carbon_bj()         # 北京碳交易
df4 = ak.energy_carbon_eu()         # 欧盟碳交易
```

### 利率/回购（14个接口）— 补充4.1宏观经济

```python
df = ak.macro_bank_usa_interest_rate()    # 美联储
df2 = ak.macro_bank_china_interest_rate() # 中国央行
df3 = ak.repo_rate_query()                # 回购利率
df4 = ak.repo_rate_hist()                 # 回购历史
df5 = ak.macro_bank_euro_interest_rate()  # 欧央行
df6 = ak.macro_bank_japan_interest_rate() # 日本央行
```

---

## 文件清单

| 脚本 | 阶段 | 说明 |
|------|:----:|------|
| `s6.1_test_market_micro.py` | 六 | 龙虎榜+融资融券+沪深港通 |
| `s7.1_test_alternative.py` | 七 | 空气质量+汽车+财富榜单+电影 |
| `s8.1_test_other.py` | 八 | 能源+利率 |
