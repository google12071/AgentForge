# AgentForge

> AI Agent Platform - 90天渐进式开发实践项目

## 项目定位

构建一个能够理解自然语言指令、自主规划任务、调用工具执行、反馈结果的通用任务 Agent 平台。

**学习目标**：通过项目驱动的方式，系统掌握 AI Agent 核心技术栈，具备设计开发工业级 Agent 系统能力。

## 技术栈

| 类别 | 选择 | 版本 |
|------|------|------|
| Python | 3.11 | - |
| Agent 框架 | LangChain + LangGraph | v1.x |
| 向量数据库 | ChromaDB | v0.5.x |
| LLM | 通义千问 / DeepSeek | - |
| 嵌入模型 | 通义千问 text-embedding | - |
| 配置管理 | Pydantic Settings | v2.x |
| 日志 | Loguru | v0.7.x |
| 测试 | pytest | v8.x |

## 项目结构

```
AgentForge/
├── src/
│   ├── agents/          # Agent 实现
│   ├── tools/           # 工具定义
│   ├── memory/          # 记忆系统
│   ├── workflows/       # 工作流定义 (LangGraph)
│   ├── rag/             # RAG 模块
│   ├── harness/         # Harness 组件（评估、监控、安全）
│   └── utils/           # 工具函数（配置、日志）
├── tests/               # 测试用例
├── docs/                # 文档
├── configs/             # 配置文件
├── data/                # 数据目录
├── pyproject.toml       # 项目配置
├── .env.example         # 环境变量示例
└── CLAUDE.md            # 项目纲领
```

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/lfq/AgentForge.git
cd AgentForge

# 创建虚拟环境
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -e ".[dev]"
```

### 2. 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，填入实际的 API Key
# QWEN_API_KEY=xxx
# DEEPSEEK_API_KEY=xxx
```

### 3. 运行测试

```bash
pytest tests/
```

## 开发阶段

| 阶段 | 时间 | 内容 |
|------|------|------|
| Phase 0 | Day 1-3 | 项目初始化 |
| Phase 1 | Day 4-15 | 基础问答 Agent |
| Phase 2 | Day 16-30 | RAG 知识库 |
| Phase 3 | Day 31-50 | 工具调用 Agent |
| Phase 4 | Day 51-70 | 工作流 Agent |
| Phase 5 | Day 71-85 | Harness 工程化 |
| Phase 6 | Day 86-90 | 平台整合 |

## 许可证

MIT License