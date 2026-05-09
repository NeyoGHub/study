# AkShare 学习脚本目录

脚本按研究阶段编号，格式：`s[阶段编号]_[类型]_[名称].py`

---

## 阶段1.1 - 股票数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s1.1_demo_stock.py` | 股票数据综合演示（历史+实时+分钟+技术指标+可视化） | `./venv/bin/python scripts/s1.1_demo_stock.py` |
| `s1.1_demo_cross_signal.py` | 金叉死叉信号识别+策略回测 | `./venv/bin/python scripts/s1.1_demo_cross_signal.py` |
| `s1.1_tool_analysis.py` | 股票综合分析工具 | `./venv/bin/python scripts/s1.1_tool_analysis.py` |
| `s1.1_test_source.py` | 核心数据源可用性测试 | `./venv/bin/python scripts/s1.1_test_source.py` |

## 阶段1.2 - 指数数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s1.2_test_index.py` | 指数接口可用性测试 | `./venv/bin/python scripts/s1.2_test_index.py` |
| `s1.2_demo_index.py` | 指数数据综合演示（技术分析+走势对比+行业分析） | `./venv/bin/python scripts/s1.2_demo_index.py` |

## 阶段5.2 - 加密货币数据（已完成）

| 脚本 | 说明 | 运行方式 |
|------|------|---------|
| `s5.2_test_crypto.py` | 加密货币接口测试 | `./venv/bin/python scripts/s5.2_test_crypto.py` |
| `s5.2_demo_crypto.py` | 加密货币数据演示（行情+持仓报告） | `./venv/bin/python scripts/s5.2_demo_crypto.py` |

---

## 运行说明

```bash
# 1. 进入项目目录
cd /home/neyo/workspace/code/study/akshare

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 运行脚本（推荐直接用venv的python）
./venv/bin/python scripts/<脚本名>.py
```

## 输出文件

所有脚本的输出文件统一保存到 `output/` 目录：
- `output/data/` - CSV数据文件
- `output/plots/` - PNG图表文件

## 命名规范

- `s[阶段]_demo_[类别].py` - 综合演示脚本（含数据获取+分析+可视化）
- `s[阶段]_test_[类别].py` - 接口测试脚本（验证可用性）
- `s[阶段]_tool_[名称].py` - 工具类脚本（多阶段通用）

---

最后更新: 2026-05-08
