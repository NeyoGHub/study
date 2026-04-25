# Full Stack FastAPI Template 学习项目

## 项目概述

Full Stack FastAPI Template 是一个完整的全栈 Web 应用模板项目，包含现代化的前后端技术栈。本项目用于深入学习 FastAPI 全栈开发。

**核心理念**: 现代化的全栈开发最佳实践

## 学习目标

- [x] 理解 FastAPI 全栈架构
- [ ] 掌握 FastAPI 后端开发
- [ ] 学习 React 前端开发
- [ ] 理解 Docker Compose 部署
- [ ] 完成基于模板的实践项目

## 项目信息

- **项目名称**: Full Stack FastAPI Template
- **项目地址**: https://github.com/fastapi/full-stack-fastapi-template
- **技术栈**: FastAPI + React + PostgreSQL + Docker
- **星标数**: 76,000+
- **最后更新**: 2026-04-24

## 目录结构

```
full-stack-fastapi-template/
├── src/                           # 项目源码
│   └── full-stack-fastapi-template/  # 原始项目源码
│       ├── backend/               # FastAPI 后端
│       ├── frontend/              # React 前端
│       ├── scripts/               # 项目脚本
│       └── compose.yml            # Docker Compose 配置
├── scripts/                       # 学习脚本
│   ├── 01_basic_setup.py          # 基础环境搭建
│   ├── 02_source_study/           # 源码学习
│   │   ├── backend_study.py       # 后端源码分析
│   │   ├── frontend_study.py      # 前端源码分析
│   │   └── deployment_study.py    # 部署配置分析
│   ├── 03_practice/               # 实践项目
│   │   ├── todo_app.py            # 待办事项应用
│   │   ├── user_system.py         # 用户系统
│   │   └── api_development.py     # API开发实践
│   └── utils/                     # 项目工具
│       ├── fastapi_helper.py      # FastAPI辅助函数
│       └── db_helper.py           # 数据库辅助函数
├── tests/                         # 测试文件
│   ├── test_backend_api.py        # 后端API测试
│   ├── test_frontend_ui.py        # 前端UI测试
│   └── fixtures/                  # 测试数据
├── notebooks/                     # Jupyter笔记
│   ├── 01_exploration/            # 项目探索
│   ├── 02_study/                  # 深度学习
│   └── 03_project/                # 项目开发
├── docs/                          # 学习文档
│   ├── README.md                  # 项目说明
│   ├── 学习计划.md                # 学习计划
│   ├── 学习笔记.md                # 学习笔记
│   ├── 后端架构.md                # 后端架构分析
│   ├── 前端架构.md                # 前端架构分析
│   └── 部署指南.md                # 部署指南
├── outputs/                       # 输出结果
│   ├── data/                      # 数据文件
│   ├── plots/                     # 图表文件
│   ├── logs/                      # 日志文件
│   └── reports/                   # 分析报告
└── config/                        # 项目配置
    └── project_config.yaml        # 项目配置
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 14+

### 环境搭建

```bash
# 1. 进入项目目录
cd /home/neyo/workspace/code/study/full-stack-fastapi-template

# 2. 进入源码目录
cd src/full-stack-fastapi-template

# 3. 启动开发环境
docker compose up --build

# 4. 访问应用
# 前端: http://localhost
# 后端API: http://localhost/api/docs
# 数据库: localhost:5432
```

### 基础使用

```bash
# 进入后端目录
cd backend

# 运行后端
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
pytest
```

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动前端开发服务器
npm run dev
```

## 学习计划

### 第一阶段：环境搭建（1-2周）

- [x] 理解项目结构
- [ ] 搭建开发环境
- [ ] 启动项目并测试
- [ ] 理解技术栈

### 第二阶段：源码学习（2-4周）

- [ ] 分析后端架构
- [ ] 学习 FastAPI 核心概念
- [ ] 分析前端架构
- [ ] 学习 React 和 TypeScript
- [ ] 理解数据库设计

#### 后端学习重点

1. **FastAPI 应用结构** `backend/app/`
   - `main.py` - 应用入口
   - `api/` - API路由
   - `core/` - 核心配置
   - `models/` - 数据模型
   - `crud/` - 数据库操作

2. **SQLModel 和 Pydantic**
   - 数据模型定义
   - 数据验证
   - 序列化和反序列化

3. **认证和安全**
   - JWT认证
   - 密码加密
   - 权限管理

#### 前端学习重点

1. **React 应用结构** `frontend/src/`
   - `App.tsx` - 应用入口
   - `components/` - 组件
   - `hooks/` - 自定义Hooks
   - `routes/` - 路由配置

2. **TypeScript**
   - 类型定义
   - 接口和类型
   - 泛型使用

3. **状态管理**
   - React Context
   - 状态管理模式
   - 数据流

### 第三阶段：实践项目（4-8周）

- [ ] 设计全栈应用
- [ ] 开发后端API
- [ ] 开发前端界面
- [ ] 实现认证系统
- [ ] 部署和优化

#### 实践项目

1. **待办事项应用**
   - 用户认证
   - 任务管理
   - 数据持久化
   - 实时更新

2. **博客系统**
   - 文章管理
   - 评论系统
   - 标签分类
   - 搜索功能

3. **用户管理系统**
   - 用户注册登录
   - 角色权限
   - 个人资料
   - 系统设置

## 核心技术点

### 1. FastAPI 后端
- 现代化的 API 框架
- 自动文档生成
- 异步支持
- 数据验证

### 2. React 前端
- 组件化开发
- TypeScript 类型安全
- Hooks API
- 状态管理

### 3. SQLModel 数据库
- ORM 模型
- 数据库迁移
- 关系映射
- 查询优化

### 4. Docker 部署
- 容器化应用
- 服务编排
- 环境隔离
- 一键部署

## 学习资源

### 官方资源
- **FastAPI文档**: https://fastapi.tiangolo.com/
- **React文档**: https://react.dev/
- **SQLModel文档**: https://sqlmodel.tiangolo.com/
- **Docker文档**: https://docs.docker.com/

### 推荐阅读
- 《FastAPI实战》
- 《React权威指南》
- 《Docker实战》
- 《TypeScript入门》

## 进度追踪

| 阶段 | 任务 | 状态 | 完成时间 |
|------|------|------|----------|
| 环境搭建 | 项目迁移 | ✅ | 2026-04-24 |
| 环境搭建 | 环境配置 | ⚪ | 待完成 |
| 源码学习 | 后端架构分析 | ⚪ | 待完成 |
| 源码学习 | 前端架构分析 | ⚪ | 待完成 |
| 实践项目 | 待办应用 | ⚪ | 待完成 |
| 实践项目 | 博客系统 | ⚪ | 待完成 |

## 常见问题

### Q1: 如何启动开发环境？

A: 使用 Docker Compose：
```bash
cd src/full-stack-fastapi-template
docker compose up --build
```

### Q2: 如何查看API文档？

A: 访问 http://localhost/api/docs 查看 FastAPI 自动生成的文档。

### Q3: 如何进行数据库迁移？

A:
```bash
cd backend
alembic upgrade head
```

## 技术栈详情

### 后端技术栈
- **FastAPI**: 现代化的 Python Web 框架
- **SQLModel**: 基于 Pydantic 和 SQLAlchemy 的 ORM
- **PostgreSQL**: 关系型数据库
- **Pydantic**: 数据验证和设置管理
- **Alembic**: 数据库迁移工具
- **Pytest**: 测试框架
- **Playwright**: 端到端测试

### 前端技术栈
- **React**: 用户界面库
- **TypeScript**: JavaScript 的超集
- **Vite**: 前端构建工具
- **Tailwind CSS**: 实用优先的 CSS 框架
- **shadcn/ui**: React 组件库
- **Playwright**: 端到端测试

## 贡献指南

如果你在学习过程中发现问题或有改进建议，欢迎：

1. 提交Issue到本项目
2. 参与FastAPI社区贡献
3. 分享学习心得

## 许可证

MIT License

## 联系方式

- **作者**: Adams (CTO)
- **团队**: AI一人公司 (CEO旺哥 + CTO Adams + COO Neyo + CCO Brain)
- **学习位置**: /home/neyo/workspace/code/study/full-stack-fastapi-template

---

**学习开始时间**: 2026-04-24
**最后更新**: 2026-04-24
**学习状态**: 🟡 进行中

## 相关文档

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [React文档](https://react.dev/)
- [Docker文档](https://docs.docker.com/)