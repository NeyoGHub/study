# 学习项目目录结构

## 📁 目录结构设计

```
/home/neyo/workspace/code/study/
├── README.md                           # 学习项目总览
├── common/                             # 公共资源和工具（跨项目共享）
│   ├── scripts/                       # 公共脚本
│   │   ├── utils.py                   # 工具函数
│   │   ├── logger.py                  # 日志工具
│   │   ├── config_manager.py          # 配置管理
│   │   ├── database.py                # 数据库操作
│   │   └── plot_utils.py              # 绘图工具
│   ├── templates/                     # 模板文件
│   │   ├── python_script_template.py  # Python脚本模板
│   │   ├── jupyter_template.ipynb     # Jupyter模板
│   │   ├── markdown_template.md       # 文档模板
│   │   └── readme_template.md         # README模板
│   ├── configs/                       # 公共配置
│   │   ├── common_config.yaml         # 通用配置
│   │   ├── logging.yaml               # 日志配置
│   │   └── paths.yaml                 # 路径配置
│   ├── data/                          # 公共数据
│   │   ├── stock_data/                # 股票数据
│   │   ├── economic_data/             # 经济数据
│   │   └── reference_data/            # 参考数据
│   └── docs/                          # 公共文档
│       ├── Python编程指南.md
│       ├── 数据分析最佳实践.md
│       ├── 金融数据分析.md
│       └── 学习方法.md
├── akshare/                           # AkShare学习项目（独立空间）
│   ├── src/                           # 项目源码
│   │   └── akshare/                   # 克隆的原始源码
│   ├── scripts/                       # 学习脚本
│   │   ├── 01_basic_usage.py          # 基础使用
│   │   ├── 02_source_study/           # 源码学习
│   │   │   ├── request_analysis.py    # 请求模块分析
│   │   │   ├── data_parsing.py        # 数据解析分析
│   │   │   └── api_design.py          # API设计分析
│   │   ├── 03_practice/               # 实践项目
│   │   │   ├── stock_monitor.py       # 股票监控
│   │   │   ├── fund_analysis.py       # 基金分析
│   │   │   └── backtest_system.py     # 回测系统
│   │   └── utils/                     # 项目特定工具
│   │       ├── akshare_helper.py      # AkShare辅助函数
│   │       └── indicators.py          # 技术指标
│   ├── tests/                         # 测试文件
│   │   ├── test_api.py                # API测试
│   │   ├── test_data_quality.py       # 数据质量测试
│   │   ├── test_performance.py        # 性能测试
│   │   └── fixtures/                  # 测试数据
│   ├── notebooks/                     # Jupyter笔记
│   │   ├── 01_exploration/            # 数据探索
│   │   │   ├── stock_data.ipynb
│   │   │   └── fund_data.ipynb
│   │   ├── 02_study/                  # 深度学习
│   │   │   ├── source_code_analysis.ipynb
│   │   │   └── architecture_study.ipynb
│   │   └── 03_project/                # 项目开发
│   │       ├── trading_system.ipynb
│   │       └── backtest_framework.ipynb
│   ├── docs/                          # 项目文档
│   │   ├── README.md                  # 项目说明
│   │   ├── 学习计划.md                # 学习计划
│   │   ├── 学习笔记.md                # 学习笔记
│   │   ├── 源码分析.md                # 源码分析
│   │   ├── 接口文档.md                # 接口文档
│   │   └── 问题记录.md                # 问题记录
│   ├── outputs/                       # 输出结果
│   │   ├── data/                      # 数据文件
│   │   │   ├── stock/                 # 股票数据
│   │   │   └── fund/                  # 基金数据
│   │   ├── plots/                     # 图表文件
│   │   │   ├── technical/             # 技术分析图
│   │   │   └── backtest/              # 回测图表
│   │   ├── logs/                      # 日志文件
│   │   └── reports/                   # 分析报告
│   ├── config/                        # 项目配置
│   │   ├── project_config.yaml        # 项目配置
│   │   └── api_config.yaml            # API配置
│   └── requirements.txt               # 项目依赖
├── full-stack-fastapi-template/       # FastAPI模板学习项目
│   ├── src/                           # 项目源码
│   ├── scripts/                       # 学习脚本
│   │   ├── 01_basic_usage.py
│   │   ├── 02_source_study/
│   │   ├── 03_practice/
│   │   └── utils/
│   ├── tests/
│   ├── notebooks/
│   ├── docs/
│   ├── outputs/
│   ├── config/
│   └── requirements.txt
├── [新项目名]/                        # 其他学习项目（相同结构）
│   ├── src/                           # 项目源码
│   ├── scripts/                       # 学习脚本
│   │   ├── 01_basic_usage.py
│   │   ├── 02_source_study/
│   │   ├── 03_practice/
│   │   └── utils/
│   ├── tests/
│   ├── notebooks/
│   ├── docs/
│   ├── outputs/
│   ├── config/
│   └── requirements.txt
└── archives/                          # 归档（已完成的项目）
    ├── [完成的项目1]/
    └── [完成的项目2]/
```

## 🎯 正在学习的项目说明

### 1. AkShare - 金融数据获取库
**项目状态**: 正在学习中
**学习阶段**: 基础使用阶段
**项目描述**: AkShare是基于Python的开源金融数据接口库，用于获取股票、基金、期货、宏观经济等金融数据。

**学习目标**:
- 掌握AkShare的基础API使用
- 学习金融数据的获取和处理
- 了解数据接口的设计模式
- 实践金融数据分析项目

**学习路径**:
- 基础使用: 熟悉常见数据接口调用
- 源码学习: 分析请求机制和数据解析
- 实践项目: 股票监控、基金分析、回测系统

### 2. Full Stack FastAPI Template - 完整Web应用模板
**项目状态**: 刚开始学习
**学习阶段**: 项目设置阶段
**项目描述**: 基于FastAPI的完整全栈Web应用模板，包含用户认证、数据库、前端等完整功能。

**学习目标**:
- 学习FastAPI最佳实践
- 掌握现代Web应用架构
- 了解前后端分离开发
- 学习Docker容器化部署

**学习路径**:
- 项目设置: 环境配置和依赖安装
- 核心功能: 用户认证、数据库操作
- 前端集成: API对接和状态管理
- 部署发布: Docker和CI/CD

## 🎯 设计理念

### 核心特点
1. **混合结构**: 结合独立性和共享性
2. **项目独立**: 每个项目有独立的空间
3. **资源共享**: 公共工具和数据统一管理
4. **灵活扩展**: 易于添加新项目

### 适用场景
- 平衡独立性和共享性
- 需要公共工具和配置
- 项目有独立的学习进度
- 希望结构清晰且易于扩展

## 📂 详细说明

### 1. common/ - 公共资源
```bash
# 跨项目共享的资源和工具
common/
├── scripts/               # 公共脚本
│   ├── utils.py          # 工具函数
│   ├── logger.py         # 日志工具
│   └── config_manager.py # 配置管理
├── templates/            # 模板文件
│   ├── python_script_template.py
│   └── jupyter_template.ipynb
├── configs/              # 公共配置
│   ├── common_config.yaml
│   └── logging.yaml
├── data/                 # 公共数据
│   ├── stock_data/
│   └── reference_data/
└── docs/                 # 公共文档
    ├── Python编程指南.md
    └── 数据分析最佳实践.md
```

### 2. 项目目录结构（每个项目）
```bash
# 每个项目都有完整的独立结构
akshare/
├── src/                  # 项目源码
├── scripts/              # 学习脚本
│   ├── 01_basic_usage.py
│   ├── 02_source_study/
│   ├── 03_practice/
│   └── utils/
├── tests/                # 测试
├── notebooks/            # Jupyter笔记
├── docs/                 # 文档
├── outputs/              # 输出
├── config/               # 配置
└── requirements.txt      # 依赖
```

### 3. scripts/ 详细结构
```bash
# 学习脚本按阶段组织
scripts/
├── 01_basic_usage.py     # 基础使用（学习项目的基本用法）
├── 02_source_study/      # 源码学习（深入分析项目源码）
│   ├── request_analysis.py   # 分析HTTP请求模块
│   ├── data_parsing.py       # 分析数据解析模块
│   └── api_design.py         # 分析API设计
├── 03_practice/          # 实践项目（基于项目的实践）
│   ├── stock_monitor.py      # 股票监控工具
│   ├── fund_analysis.py      # 基金分析工具
│   └── backtest_system.py    # 回测系统
└── utils/                # 项目特定工具
    ├── akshare_helper.py     # 项目辅助函数
    └── indicators.py         # 技术指标计算
```

## ✅ 结构优势

1. **平衡性好**
   - 项目既独立又有公共资源共享
   - 兼顾了独立性和复用性
   - 灵活性高

2. **结构清晰**
   - 每个项目结构统一且完整
   - 公共资源明确分离
   - 层次分明

3. **易于扩展**
   - 添加新项目很简单
   - 模板化创建项目
   - 公共资源可复用

4. **管理便捷**
   - 可以独立管理每个项目
   - 公共资源统一维护
   - 便于查看整体进度

5. **版本控制友好**
   - 每个项目可以有独立的git仓库
   - 公共代码也可以独立版本控制
   - 便于团队协作

6. **学习友好**
   - 新项目学习可参考模板
   - 公共工具降低学习成本
   - 文档和模板齐全

## 📝 快速开始

### 1. 初始化环境
```bash
# 创建基础结构
cd /home/neyo/workspace/code/study

# 公共区域已经创建
# common/scripts/
# common/templates/
# common/configs/

# 创建新项目
mkdir new_project
cd new_project

# 使用模板创建目录结构
cp -r ../common/templates/python_script_template.py scripts/
cp -r ../common/templates/jupyter_template.ipynb notebooks/
```

### 2. 添加新项目
```bash
# 1. 创建项目目录
mkdir /home/neyo/workspace/code/study/new_project
cd /home/neyo/workspace/code/study/new_project

# 2. 创建标准结构
mkdir -p src scripts/02_source_study scripts/03_practice scripts/utils
mkdir -p tests/fixtures
mkdir -p notebooks/01_exploration notebooks/02_study notebooks/03_project
mkdir -p docs outputs/{data/{stock,fund},plots/{technical,backtest},logs,reports}
mkdir -p config

# 3. 克隆项目源码
cd src
git clone https://github.com/user/repo.git

# 4. 从公共区域复制模板
cp ../../common/templates/python_script_template.py ../scripts/01_basic_usage.py
cp ../../common/templates/jupyter_template.ipynb ../notebooks/01_exploration/template.ipynb
cp ../../common/templates/readme_template.md ../README.md

# 5. 创建项目配置
cp ../../common/configs/common_config.yaml ../config/project_config.yaml

# 6. 创建依赖文件
touch ../requirements.txt
```

### 3. 使用公共工具
```python
# 在项目脚本中导入公共工具
import sys
sys.path.append('/home/neyo/workspace/code/study/common/scripts')

from utils import setup_logger, parse_config
from logger import get_logger
from plot_utils import plot_stock_data

# 使用公共工具
logger = get_logger('my_project')
config = parse_config('config/project_config.yaml')

# 项目特定代码
project_data = get_project_data()
plot_stock_data(project_data, logger=logger)
```

### 4. 项目开发流程
```bash
# 1. 基础使用阶段
cd scripts
python 01_basic_usage.py

# 2. 源码学习阶段
cd 02_source_study
python request_analysis.py
python data_parsing.py

# 3. 实践项目阶段
cd 03_practice
python stock_monitor.py

# 4. 测试和调试
cd ../tests
pytest test_api.py -v

# 5. 文档整理
cd ../docs
vim 学习笔记.md
```

## 🎯 总结

这个目录结构适合大多数学习场景，平衡了独立性和共享性。

**核心优势**:
- 平衡了独立性和共享性
- 每个项目有独立空间
- 公共工具统一管理
- 易于扩展新项目
- 模板化开发

**最佳场景**:
- 同时学习2-5个相关项目
- 需要公共工具和配置
- 希望有清晰的目录结构
- 计划长期学习和开发