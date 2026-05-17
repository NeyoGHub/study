# AkShare 学习脚本目录

脚本按研究阶段编号，格式：`s[阶段编号]_[类型]_[名称].py`

完整学习路线图（14个子阶段）见 `LEARNING_ROADMAP.md`

---

## 阶段1.1 - 股票行情数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s1.1_demo_stock.py` | 股票行情综合演示（历史+实时+分钟+技术指标+可视化） | `./venv/bin/python scripts/s1.1_demo_stock.py` |
| `s1.1_demo_cross_signal.py` | 金叉死叉信号识别+策略回测 | `./venv/bin/python scripts/s1.1_demo_cross_signal.py` |
| `s1.1_tool_analysis.py` | 股票综合分析工具（支持命令行参数指定股票代码） | `./venv/bin/python scripts/s1.1_tool_analysis.py [股票代码]` |
| `s1.1_test_source.py` | 核心数据源可用性测试 | `./venv/bin/python scripts/s1.1_test_source.py` |

## 阶段1.2 - 指数数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s1.2_test_index.py` | 指数接口可用性测试（含东方财富→新浪回退） | `./venv/bin/python scripts/s1.2_test_index.py` |
| `s1.2_demo_index.py` | 指数数据综合演示（技术分析+走势对比+行业分析） | `./venv/bin/python scripts/s1.2_demo_index.py` |

## 阶段1.3 - 上市公司基本面数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s1.3_test_fundamental.py` | 上市公司基本面测试（财务/业绩/分红/股东/估值） | `./venv/bin/python scripts/s1.3_test_fundamental.py` |
| `s1.3_demo_fundamental.py` | 基本面综合演示（行业分布+财务指标+业绩排名+估值） | `./venv/bin/python scripts/s1.3_demo_fundamental.py` |

## 阶段2.1 - 基金数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s2.1_test_fund.py` | 基金接口测试（净值/排行/ETF/持仓/经理/评级） | `./venv/bin/python scripts/s2.1_test_fund.py` |
| `s2.1_demo_fund.py` | 基金数据综合演示（净值分析+排行+ETF+持仓可视化） | `./venv/bin/python scripts/s2.1_demo_fund.py` |

## 阶段2.2 - 债券数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s2.2_test_bond.py` | 债券接口测试（收益率/指数/可转债/中美利率） | `./venv/bin/python scripts/s2.2_test_bond.py` |
| `s2.2_demo_bond.py` | 债券数据综合演示（收益率曲线+指数+可转债+期货对比） | `./venv/bin/python scripts/s2.2_demo_bond.py` |

## 阶段5.2 - 加密货币数据（CoinGecko API）

⚠ 注: 原AkShare自带的crypto接口仅有3个（crypto_js_spot/持仓报告/CME），数据量极少。已替换为 CoinGecko API，覆盖30+端点。

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s5.2_test_crypto.py` | CoinGecko API完全测试（30+端点，含OHLCV/技术分析/可视化） | `./venv/bin/python scripts/s5.2_test_crypto.py` |

## 阶段5.4 - QDII数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s5.4_test_qdii.py` | QDII接口测试 | `./venv/bin/python scripts/s5.4_test_qdii.py` |
| `s5.4_demo_qdii.py` | QDII综合演示（三大类涨幅排行） | `./venv/bin/python scripts/s5.4_demo_qdii.py` |

## 阶段六 - 龙虎榜+融资融券+沪深港通（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s6.1_test_market_micro.py` | 龙虎榜/两融/沪深港通测试 | `./venv/bin/python scripts/s6.1_test_market_micro.py` |
| `s6.1_demo_market_micro.py` | 市场微观综合演示（含3张图表） | `./venv/bin/python scripts/s6.1_demo_market_micro.py` |

## 阶段七 - 空气质量+汽车数据+电影（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s7.1_test_alternative.py` | 空气/汽车/财富/电影测试 | `./venv/bin/python scripts/s7.1_test_alternative.py` |
| `s7.1_demo_alternative.py` | 另类数据综合演示（含3张图表） | `./venv/bin/python scripts/s7.1_demo_alternative.py` |

## 阶段八 - 能源+利率（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s8.1_test_other.py` | 能源/利率扩展测试 | `./venv/bin/python scripts/s8.1_test_other.py` |
| `s8.1_demo_energy_rate.py` | 能源+利率综合演示（含2张图表） | `./venv/bin/python scripts/s8.1_demo_energy_rate.py` |

|---

## 全部阶段已完成

所有18阶段均已研究完成。详见 `LEARNING_ROADMAP.md`。

| `s7.2_test_movie_boxoffice.py` | 电影票房数据接口测试（AkShare原生+替代数据源）
| `s7.2_demo_movie_boxoffice.py` | 电影票房综合演示（小尘API+猫眼排行+可视化） | `./venv/bin/python scripts/s7.2_demo_movie_boxoffice.py` |

## 运行说明

```bash
cd /home/neyo/workspace/code/study/akshare
./venv/bin/python scripts/<脚本名>.py
```

## 输出文件

所有脚本的输出文件统一保存到 `output/` 目录：
- `output/data/[类别]/` - CSV数据文件
- `output/plots/[类别]/` - PNG图表文件

## 命名规范

- `s[阶段]_demo_[类别].py` — 综合演示脚本（含数据获取+分析+可视化）
- `s[阶段]_test_[类别].py` — 接口测试脚本（验证可用性）
- `s[阶段]_tool_[名称].py` — 工具类脚本（支持命令行参数）

---

最后更新: 2026-05-09
