# AkShare 学习项目

## 项目概述

AkShare 是一个优雅而简单的金融数据接口库，专为 Python 用户构建！本项目用于深入学习和分析 AkShare 的源码。

**核心理念**: Write less, get more!

## 学习目标

- [x] 理解 AkShare 的核心架构和设计理念
- [ ] 掌握主要功能和使用方法
- [ ] 深入分析源码实现
- [ ] 完成基于 AkShare 的实践项目

## 项目信息

- **项目名称**: AkShare
- **项目地址**: https://github.com/akfamily/akshare
- **当前版本**: 最新
- **星标数**: 18,545
- **最后更新**: 2026-05-09

## 目录结构

```
akshare/
├── src/                           # 项目源码
│   └── akshare/                   # 克隆的原始源码
├── scripts/                       # 学习脚本（按阶段编号，14个子阶段）
│   ├── README.md                  # 脚本使用说明 ← 从这里查看
│   ├── s1.1_demo_stock.py         # 股票行情综合示例
│   ├── s1.1_demo_cross_signal.py  # 金叉死叉信号+回测
│   ├── s1.1_tool_analysis.py      # 股票分析工具
│   ├── s1.1_test_source.py        # 数据源优先级测试
│   ├── s1.2_test_index.py         # 指数接口测试
│   ├── s1.2_demo_index.py         # 指数数据综合示例
│   ├── s2.1_test_fund.py          # 基金接口测试
│   ├── s2.1_demo_fund.py          # 基金数据综合示例
│   ├── s2.2_test_bond.py          # 债券接口测试
│   ├── s2.2_demo_bond.py          # 债券数据综合示例
│   ├── s5.2_test_crypto.py        # 加密货币接口测试
│   └── s5.2_demo_crypto.py        # 加密货币综合示例
├── output/                        # 输出结果（数据+图表）
│   ├── data/                      # CSV数据文件
│   │   ├── stock/              # 股票数据
│   │   ├── index/              # 指数数据
│   │   └── ...                 # 其他类别
│   └── plots/                     # PNG图表文件
│       ├── technical/          # 技术分析图表
│       └── ...
├── docs/                          # 研究文档（每阶段3份，共16份）
│   ├── AkShare股票数据接口使用指南.md
│   ├── 股票数据接口演示总结.md
│   ├── 股票数据接口学习成果.md
│   ├── AkShare指数数据接口使用指南.md
│   ├── 指数数据接口演示总结.md
│   ├── 指数数据接口学习成果.md
│   ├── AkShare基金数据接口使用指南.md
│   ├── 基金数据接口演示总结.md
│   ├── 基金数据接口学习成果.md
│   ├── AkShare债券数据接口使用指南.md
│   ├── 债券数据接口演示总结.md
│   ├── 债券数据接口学习成果.md
│   ├── AkShare加密货币数据接口使用指南.md
│   ├── 加密货币数据接口演示总结.md
│   ├── 加密货币数据接口学习成果.md
│   └── 数据接口研究标准模板.md
├── LEARNING_ROADMAP.md            # 学习路线图（14个子阶段）
│   ├── ✅ 1.1 股票行情 / 1.2 指数
│   ├── ✅ 1.3 上市公司基本面 ← 已完成
│   ├── ✅ 2.1 基金 / 2.2 债券
│   ├── → 3.1 期货 / ⏳ 3.2 期权
│   ├── ⏳ 4.1 宏观 / 4.2 行业
│   ├── ⏳ 5.1 外汇 / ✅ 5.2 加密货币
│   └── 🆕 5.3 REITs / 5.4 QDII
├── tests/                         # 测试文件
├── config/                        # 项目配置
└── venv/                          # 虚拟环境
```

## 快速开始

### 环境搭建

```bash
# 1. 进入项目目录
cd /home/neyo/workspace/code/study/akshare

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install akshare pandas numpy matplotlib

# 4. 验证安装
python -c "import akshare as ak; print(ak.__version__)"
```

### 运行示例

```bash
# 激活虚拟环境
source venv/bin/activate

# 快速查看所有脚本说明
cat scripts/README.md

# 运行数据源测试（查看可用数据源优先级）
./venv/bin/python scripts/s1.1_test_source.py

# 运行股票行情综合示例
./venv/bin/python scripts/s1.1_demo_stock.py

# 运行指数数据综合示例
./venv/bin/python scripts/s1.2_demo_index.py

# 运行基金数据综合示例
./venv/bin/python scripts/s2.1_demo_fund.py

# 运行债券数据综合示例
./venv/bin/python scripts/s2.2_demo_bond.py
```

### 基础使用

```python
import akshare as ak

# 获取股票历史数据（推荐使用新浪数据源）
stock_df = ak.stock_zh_a_daily(
    symbol="sz002624",
    start_date="20240101",
    end_date="20260430",
    adjust="qfq"  # 前复权
)
print(stock_df.head())

# 获取实时行情
spot_df = ak.stock_zh_a_spot()
print(f"共获取 {len(spot_df)} 只股票的实时数据")

# 获取指数数据
index_df = ak.stock_zh_index_spot_sina()
print(index_df.head())
```

### 输出文件说明

所有脚本产生的文件都统一存放在 `outputs/` 目录：

- **数据文件**：`outputs/data/stock/`, `outputs/data/index/`, `outputs/data/market/`
- **图表文件**：`outputs/plots/technical/`, `outputs/plots/overview/`
- **日志文件**：`outputs/logs/`
- **分析报告**：`outputs/reports/`

详见 [outputs/README.md](outputs/README.md)

## 学习计划

### 第一阶段：基础使用（1-2周）

- [x] 安装和配置环境
- [x] 运行示例代码
- [x] 理解基本功能
- [x] 测试核心数据源
- [x] 完成基础练习

### 第二阶段：源码学习（2-4周）

- [x] 分析项目架构
- [x] 阅读核心模块源码
- [x] 理解关键算法
- [x] 总结学习笔记

#### 源码学习重点

1. **核心工具模块** `akshare/utils/`
   - `request.py` - HTTP请求封装
   - `multi_decrypt.py` - 数据解密
   - `context.py` - 上下文管理

2. **数据接口模块** `akshare/stock/`
   - `stock_zh_a_sina.py` - 新浪A股数据（推荐）
   - `stock_zh_a_spot.py` - A股实时数据
   - API设计和实现模式

3. **数据处理流程**
   - 网络请求 → 数据解析 → 清洗处理 → DataFrame转换

### 第三阶段：实践项目（4-8周）

- [x] 设计实践项目
- [x] 开发功能模块
- [x] 测试和优化
- [x] 文档整理

#### 实践项目

1. **股票数据监控工具** ✅
   - 实时监控指定股票
   - 价格提醒功能
   - 技术指标计算

2. **基金筛选工具** ⚪
   - 获取所有基金数据
   - 按收益率排序
   - 风险评估

3. **经济数据分析平台** ⚪
   - 获取经济指标数据
   - 数据趋势分析
   - 图表展示

## 核心技术点

### 1. HTTP请求机制
- 重试机制（3次重试 + 随机延迟）
- 超时控制
- 错误处理

### 2. 数据解析技术
- HTML解析（BeautifulSoup）
- JSON数据处理
- Excel文件读取
- DataFrame转换

### 3. API设计规范
- 统一的接口命名
- 参数验证
- 错误处理
- 文档规范

## 学习资源

### 官方资源
- **官方文档**: https://akshare.akfamily.xyz/
- **GitHub仓库**: https://github.com/akfamily/akshare
- **微信公众号**: 数据科学实战
- **知识社区**: https://t.zsxq.com/ZCxUG

### 相关技术
- **Pandas**: https://pandas.pydata.org/docs/
- **Requests**: https://docs.python-requests.org/
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/

## 进度追踪

| 阶段 | 任务 | 状态 | 完成时间 |
|------|------|------|----------|
| 基础使用 | 环境搭建 | ✅ | 2026-04-24 |
| 基础使用 | 运行示例 | ✅ | 2026-04-25 |
| 基础使用 | 核心数据源测试 | ✅ | 2026-04-25 |
| 源码学习 | 项目架构分析 | ✅ | 2026-04-25 |
| 源码学习 | 核心模块分析 | ✅ | 2026-04-25 |
| 实践项目 | 股票监控工具 | ✅ | 2026-04-26 |
| 实践项目 | 基金筛选工具 | ⚪ | 待完成 |
| 实践项目 | 经济数据分析平台 | ⚪ | 待完成 |

## 项目成果

### 已完成的脚本

| 脚本 | 阶段 | 说明 |
|------|:----:|------|
| `s1.1_test_source.py` | 1.1 | 核心数据源可用性测试（新浪/腾讯/东方财富） |
| `s1.1_demo_stock.py` | 1.1 | 股票行情综合演示：历史+实时+分钟+技术指标+可视化 |
| `s1.1_demo_cross_signal.py` | 1.1 | 金叉死叉信号识别 + 均线策略回测 |
| `s1.1_tool_analysis.py` | 1.1 | 股票综合分析工具（多维度分析，支持命令行参数） |
| `s1.2_test_index.py` | 1.2 | 指数接口可用性验证（A股/港股/行业/成分股） |
| `s1.2_demo_index.py` | 1.2 | 指数数据综合演示：技术分析+走势对比+行业分析+可视化 |
| `s1.3_test_fundamental.py` | 1.3 | 上市公司基本面测试（财务/业绩/分红/股东/估值） |
| `s1.3_demo_fundamental.py` | 1.3 | 基本面综合演示：行业分布+财务指标+业绩排名+估值 |
| `s2.1_test_fund.py` | 2.1 | 基金接口测试（净值/排行/ETF/持仓/经理/评级） |
| `s2.1_demo_fund.py` | 2.1 | 基金数据综合演示：净值分析+排行+ETF+持仓可视化 |
| `s2.2_test_bond.py` | 2.2 | 债券接口测试（收益率/指数/可转债/中美利率） |
| `s2.2_demo_bond.py` | 2.2 | 债券数据综合演示：收益率曲线+指数+可转债+期货对比 |
| `s5.2_test_crypto.py` | 5.2 | 加密货币接口测试 |
| `s5.2_demo_crypto.py` | 5.2 | 加密货币数据演示：行情+持仓报告+可视化 |

> 所有脚本的详细说明见 `scripts/README.md`
> 完整路线图（14个子阶段）见 `LEARNING_ROADMAP.md`

### 数据源研究结论

经过测试验证，**新浪财经**是当前环境下最稳定可靠的数据源：

1. **stock_zh_a_daily** - 新浪A股历史K线（✅ 稳定）
2. **stock_zh_a_spot** - 新浪A股实时行情（✅ 稳定）
3. **stock_zh_index_spot_sina** - 新浪指数实时（✅ 稳定）
4. **stock_zh_a_hist_tx** - 腾讯A股历史（⚪ 备用）
5. **东方财富网** - ❌ 当前不可用

所有脚本已配置多数据源容错机制，自动按优先级切换。

## 常见问题

### Q1: 如何处理网络请求超时？

A: AkShare 内置了重试机制，如果还是超时，可以尝试：
```python
# 增加超时时间
ak.stock_zh_a_hist(symbol="000001", period="daily", timeout=30)
```

### Q2: 如何获取最新的接口列表？

A: 访问官方文档或使用：
```python
import akshare as ak
print(ak.__version__)
```

## 贡献指南

如果你在学习过程中发现问题或有改进建议，欢迎：

1. 提交Issue到本项目
2. 参与AkShare社区贡献
3. 分享学习心得

## 许可证

MIT License

## 联系方式

- **作者**: Adams (CTO)
- **团队**: AI一人公司 (CEO旺哥 + CTO Adams + COO Neyo + CCO Brain)
- **学习位置**: /home/neyo/workspace/code/study/akshare

---

**学习开始时间**: 2026-04-24
**最后更新**: 2026-05-09
**学习状态**: 🟡 进行中

## 相关文档

- [AkShare项目研究](/home/neyo/workspace/ObsidianNotes/GitHub项目研究/AkShare项目研究.md)
- [AkShare学习行动计划](/home/neyo/workspace/ObsidianNotes/GitHub项目研究/AkShare学习行动计划.md)