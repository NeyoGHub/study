# 学习项目目录结构方案 - 方案二

## 📁 目录结构设计

```
/home/neyo/workspace/code/study/
├── README.md                           # 学习项目总览
├── projects/                          # 所有项目源码
│   ├── akshare/                      # AkShare项目
│   │   ├── akshare/                  # 核心源码
│   │   ├── setup.py
│   │   └── ...
│   ├── [项目1]/
│   │   └── [源码]
│   └── [项目2]/
│       └── [源码]
├── scripts/                           # 所有学习脚本
│   ├── akshare/                      # AkShare相关脚本
│   │   ├── 01_basic_usage.py
│   │   ├── 02_source_analysis.py
│   │   └── 03_practice.py
│   ├── [项目1]/
│   │   └── [脚本]
│   └── common/                       # 公共脚本
│       ├── utils.py                  # 公共工具函数
│       ├── config.py                 # 配置管理
│       └── logger.py                 # 日志工具
├── tests/                             # 所有测试文件
│   ├── akshare/                      # AkShare测试
│   │   ├── test_api.py
│   │   └── test_data.py
│   ├── [项目1]/
│   │   └── [测试]
│   └── common/                       # 公共测试工具
│       ├── test_utils.py
│       └── fixtures/                 # 测试数据
├── notebooks/                         # 所有Jupyter笔记
│   ├── akshare/                      # AkShare笔记
│   │   ├── 01_exploration.ipynb
│   │   └── 02_study.ipynb
│   ├── [项目1]/
│   │   └── [笔记]
│   └── templates/                    # 笔记本模板
│       └── study_template.ipynb
├── docs/                              # 所有学习文档
│   ├── akshare/                      # AkShare文档
│   │   ├── 学习笔记.md
│   │   └── 源码分析.md
│   ├── [项目1]/
│   │   └── [文档]
│   └── common/                       # 公共文档
│       ├── Python基础.md
│       ├── 数据分析.md
│       └── 最佳实践.md
├── outputs/                           # 所有输出结果
│   ├── akshare/                      # AkShare输出
│   │   ├── data/
│   │   ├── plots/
│   │   └── logs/
│   ├── [项目1]/
│   │   └── [输出]
│   └── common/                       # 公共输出
│       └── exports/
└── config/                            # 全局配置
    ├── common.py                     # 公共配置
    └── paths.py                      # 路径配置
```

## 🎯 设计理念

### 核心特点
1. **功能分层**：按功能组织代码，所有项目的相同功能放在一起
2. **代码复用**：公共脚本和工具集中管理
3. **统一管理**：所有项目统一管理，便于维护
4. **跨项目协作**：便于在不同项目间共享代码和数据

### 适用场景
- 需要在多个项目间复用代码
- 希望有统一的工具和配置
- 项目间有较强的交互
- 喜欢全局管理视角

## 📂 详细说明

### 1. projects/ - 项目源码
```bash
# 所有项目的原始源码
projects/
├── akshare/              # AkShare源码
│   └── akshare/
├── [项目1]/              # 其他项目源码
└── [项目2]/              # 其他项目源码
```

### 2. scripts/ - 学习脚本
```bash
# 按项目分类，同时有公共脚本
scripts/
├── akshare/              # AkShare专用脚本
│   ├── 01_basic_usage.py
│   └── 02_study.py
├── [项目1]/              # 项目1专用脚本
└── common/              # 公共脚本
    ├── utils.py         # 工具函数
    ├── db.py            # 数据库操作
    └── api.py           # API封装
```

### 3. tests/ - 测试文件
```bash
# 测试文件，包含公共测试工具
tests/
├── akshare/              # AkShare测试
├── [项目1]/              # 项目1测试
└── common/              # 公共测试工具
    ├── fixtures/        # 测试数据
    └── helpers/         # 测试辅助函数
```

### 4. notebooks/ - Jupyter笔记
```bash
# 笔记本，包含模板
notebooks/
├── akshare/              # AkShare笔记
├── [项目1]/              # 项目1笔记
└── templates/           # 笔记本模板
    └── study_template.ipynb
```

### 5. docs/ - 学习文档
```bash
# 文档，包含公共知识
docs/
├── akshare/              # AkShare文档
├── [项目1]/              # 项目1文档
└── common/              # 公共知识
    ├── Python基础.md
    ├── 数据分析.md
    └── 量化交易.md
```

### 6. outputs/ - 输出结果
```bash
# 输出结果，按项目分类
outputs/
├── akshare/              # AkShare输出
│   ├── data/
│   ├── plots/
│   └── logs/
├── [项目1]/              # 项目1输出
└── common/              # 公共输出
    └── exports/         # 导出文件
```

### 7. config/ - 全局配置
```bash
# 全局配置和设置
config/
├── common.py            # 公共配置
├── paths.py             # 路径配置
└── logging.yaml         # 日志配置
```

## ✅ 优点

1. **代码复用高效**
   - 公共脚本和工具集中管理
   - 避免代码重复
   - 便于维护公共功能

2. **统一管理**
   - 所有项目统一视角
   - 便于查看整体学习进度
   - 集中式配置管理

3. **跨项目协作**
   - 便于在不同项目间共享代码
   - 公共数据和工具可跨项目使用
   - 统一的测试和文档标准

4. **节省空间**
   - 公共库和工具只需一份
   - 减少重复依赖安装
   - 优化磁盘使用

5. **一致性高**
   - 统一的代码风格和规范
   - 一致的工具和配置
   - 标准化的开发流程

## ❌ 缺点

1. **项目边界模糊**
   - 项目间的代码混合在一起
   - 难以区分哪些代码属于哪个项目
   - 可能出现依赖混乱

2. **权限管理复杂**
   - 需要处理跨项目的权限问题
   - 公共代码的修改可能影响多个项目

3. **独立性差**
   - 无法独立管理单个项目
   - 项目间耦合度较高
   - 难以单独分发项目

4. **版本控制复杂**
   - 需要处理多个项目的版本控制
   - 公共代码的版本管理复杂
   - 难以为单个项目创建独立分支

5. **学习曲线较陡**
   - 需要理解整个目录结构
   - 新项目学习需要了解全局配置
   - 结构相对复杂

## 🚀 使用建议

### 适合使用方案二的情况
- 需要在多个项目间复用大量代码
- 希望有统一的工具和配置
- 项目间有较强的交互
- 喜欢全局管理视角

### 不适合使用方案二的情况
- 主要专注于单个项目的学习
- 项目间交互较少
- 希望每个项目完全独立
- 需要独立版本控制

## 📝 快速开始

### 创建新学习项目
```bash
# 1. 添加新项目源码
cd /home/neyo/workspace/code/study/projects
git clone https://github.com/user/repo.git 新项目名

# 2. 创建项目相关目录
cd /home/neyo/workspace/code/study/scripts
mkdir 新项目名

# 3. 复制公共脚本模板
cp common/utils.py 新项目名/

# 4. 创建学习脚本
cd 新项目名
vi 01_basic_usage.py

# 5. 在公共配置中添加项目路径
cd /home/neyo/workspace/code/study/config
vi paths.py
```

### 使用公共工具
```python
# 在任何项目的脚本中都可以使用公共工具
import sys
sys.path.append('/home/neyo/workspace/code/study/scripts/common')

from utils import setup_logger, parse_config
from db import Database

# 使用公共工具
logger = setup_logger('my_project')
config = parse_config('my_config.yaml')
db = Database(config)
```

## 🎯 总结

**方案二适合**：需要跨项目复用代码，希望统一管理和配置

**核心优势**：代码复用高效、统一管理、跨项目协作

**最佳场景**：同时学习3-5个项目，需要复用公共代码和工具

**注意**：适合有一定经验的开发者，需要仔细设计公共接口和依赖关系