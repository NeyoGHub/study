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

## 阶段5.2 - 加密货币数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s5.2_test_crypto.py` | 加密货币接口测试 | `./venv/bin/python scripts/s5.2_test_crypto.py` |
| `s5.2_demo_crypto.py` | 加密货币数据演示（行情+持仓报告） | `./venv/bin/python scripts/s5.2_demo_crypto.py` |

---

## 规划中的阶段（脚本待创建）

| 阶段 | 内容 | 脚本命名 |
|:----:|------|---------|
| 1.3 | 上市公司基本面数据 | `s1.3_test_fundamental.py` / `s1.3_demo_fundamental.py` |
| 3.1 | 期货数据（含现货/能源） | `s3.1_test_futures.py` / `s3.1_demo_futures.py` |
| 3.2 | 期权数据 | `s3.2_test_option.py` / `s3.2_demo_option.py` |
| 4.1 | 宏观经济数据 | `s4.1_test_macro.py` / `s4.1_demo_macro.py` |
| 4.2 | 行业数据 | `s4.2_test_industry.py` / `s4.2_demo_industry.py` |
| 5.1 | 外汇数据 | `s5.1_test_forex.py` / `s5.1_demo_forex.py` |
| 5.3 | REITs数据 | `s5.3_test_reits.py` / `s5.3_demo_reits.py` |
| 5.4 | QDII数据 | `s5.4_test_qdii.py` / `s5.4_demo_qdii.py` |



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
