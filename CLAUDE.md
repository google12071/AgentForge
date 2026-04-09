# AgentForge 项目纲领

> 90天渐进式AI Agent平台开发计划
> 创建时间：2026-04-08

---

## 项目定位

**AgentForge** - 一个能够理解自然语言指令、自主规划任务、调用工具执行、反馈结果的通用任务Agent平台。

**学习目标**：通过项目驱动的方式，系统掌握AI Agent核心技术栈，具备设计开发工业级Agent系统能力。

---

## 核心技能栈（二八法则）

### 必修技能（前9项，解决95%问题）

| 优先级 | 技能 | 定位 | 阶段 |
|--------|------|------|------|
| 1 | Prompt Engineering | 基础层 | Phase 1 |
| 2 | Problem Shaping | 规划层 | Phase 1, 3 |
| 3 | Claude Code最佳实践 | 工具层 | Phase 0 |
| 4 | Vibe Coding最佳实践 | 方法层 | 全程 |
| 5 | LangChain核心组件 | 框架入口 | Phase 3, 4 |
| 6 | RAG与知识检索 | 核心场景 | Phase 2 |
| 7 | Tool Use/Function Calling | Agent能力 | Phase 3 |
| 8 | Agent编排与工作流(LangGraph) | 生产必备 | Phase 4 |
| 9 | Harness Engineering | 可靠性保障 | Phase 5 |

### 完整技能栈（22项）

详见 `ai-agent-stack.md`

---

## 90天迭代路线

```
Phase 0 (Day 1-3)     项目初始化
       ↓              Claude Code + Git + Python环境
Phase 1 (Day 4-15)    基础问答Agent
       ↓              Prompt Engineering + LLM API
Phase 2 (Day 16-30)   RAG知识库
       ↓              向量数据库 + 文档检索
Phase 3 (Day 31-50)   工具调用Agent
       ↓              Tool Use + ReAct模式
Phase 4 (Day 51-70)   工作流Agent
       ↓              LangGraph + 状态管理
Phase 5 (Day 71-85)   Harness工程化
       ↓              评估 + 监控 + 安全
Phase 6 (Day 86-90)   平台整合
                      MCP + 多Agent + 文档
```

详细计划见 `learning-plan.md`

---

## 技术选型（Phase 0 确定，2026-04-09）

### 核心决策

| 类别 | 选择 | 版本 | 原因 |
|------|------|------|------|
| **Python 版本** | 3.11 | - | 稳定成熟，库兼容性好，性能提升明显 |
| **LangChain** | v1.x | v1.2.0 | 重大重构版已稳定，Agent底层使用LangGraph runtime |
| **LangGraph** | v1.x | v1.1 | 首个稳定持久化Agent框架，被Uber/LinkedIn/Klarna采用 |
| **向量数据库** | ChromaDB | v0.5.x | 本地嵌入式，零配置，快速迭代 |
| **配置管理** | Pydantic Settings | v2.x | 类型安全，环境变量支持，与数据模型统一 |
| **包管理** | uv | 最新版 | 极速现代方案，依赖分组支持 |
| **代码风格** | Ruff | 最新版 | 一体化 lint + format，Rust 实现 |
| **虚拟环境** | venv | Python 3.11 内置 | Python 官方方案，轻量标准 |
| **日志系统** | Loguru | v0.7.x | 简洁易用，无需配置 |
| **测试框架** | pytest | v8.x | Python 标准，插件生态丰富 |

> **注意**：LangChain v0.3 与 v1.x 不兼容，新项目直接使用 v1.x。

### 框架选择理由

- **LangChain v1.x + LangGraph v1.x**：Agent 开发首选，已稳定，LangChain 提供高层抽象，LangGraph 提供底层编排控制。
- **不引入 LlamaIndex**：LangChain v1.x 已满足 Agent 开发需求，避免多框架复杂度。

### LLM 供应商与嵌入模型

| 类别 | 供应商 | 模型 | 说明 |
|------|--------|------|------|
| LLM | 通义千问 | qwen-plus | 主要 LLM，已有 API Key |
| LLM | DeepSeek | deepseek-chat | 对比测试，已有 API Key |
| 嵌入模型 | 通义千问 | text-embedding-v3 | 向量嵌入，与 LLM 供应商统一 |

### 核心依赖清单

```
# 核心 Agent 框架
langchain>=1.0
langgraph>=1.0
langchain-community>=1.0

# 向量数据库
chromadb>=0.5.0

# 数据验证与配置
pydantic>=2.0
pydantic-settings>=2.0

# 日志
loguru>=0.7.0

# 测试
pytest>=8.0

# LLM 供应商（按需安装）
# langchain-zhipuai  # 智谱
# 或通过 langchain-community 使用通义/DeepSeek
```

---

## 开发原则（Phase 0 确定）

| 原则 | 具体内容 |
|------|----------|
| **版本控制** | Git 管理 + GitHub 远程仓库同步 |
| **开发环境** | PyCharm IDE |
| **开发方式** | 项目驱动、迭代式开发，学中做、做中学 |
| **质量保障** | 单元测试随功能增加，逐步提升覆盖率 |
| **灵活性** | 组件、模块、结构按实际情况灵活调整 |
| **目标导向** | 学习实践为主，逐步逼近生产级 Agent 效果 |

---

## 项目结构

```
AgentForge/
├── src/
│   ├── agents/          # Agent实现
│   ├── tools/           # 工具定义
│   ├── memory/          # 记忆系统
│   ├── workflows/       # 工作流定义
│   ├── rag/             # RAG模块
│   ├── harness/         # Harness组件
│   └── utils/           # 工具函数
├── tests/               # 测试用例
├── docs/                # 文档
├── configs/             # 配置文件
├── data/                # 数据目录
├── ai-agent-stack.md    # 技能栈定义
├── learning-plan.md     # 学习计划
├── skill-tracking.md    # 技能追踪
├── CLAUDE.md            # 本文件
└── README.md            # 项目说明
```

---

## 编码规范

### Python规范
- 使用Pydantic进行数据验证
- 所有函数添加类型注解
- 使用logger而非print
- 测试覆盖率目标：>60%

### Git提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
test: 测试用例
refactor: 代码重构
chore: 构建/工具变动

示例：
feat(rag): 实现文档向量化和检索功能
fix(agent): 修复工具调用错误处理
```

### 分支策略
- `main`: 稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支

---

## 学习方式

### Vibe Coding原则
1. **描述** → 清晰表达需求
2. **生成** → AI生成代码
3. **测试** → 验证功能正确
4. **迭代** → 渐进式优化

### 每日工作流（2-3小时）
```
18:00 - 18:30  复盘昨日，阅读文档
18:30 - 20:00  核心开发
20:00 - 20:30  测试调试
20:30 - 21:00  提交代码，更新笔记
```

### 周末（4-6小时）
- 上午：深度开发，攻克难点
- 下午：测试优化，文档整理
- 晚上：复盘总结，规划下周

---

## 当前状态

**当前阶段**：Phase 0 - 项目初始化
**开始时间**：2026-04-09
**当前版本**：v0.0.0

### Phase 0 任务清单

#### Day 1: 环境准备
- [ ] 创建GitHub仓库 `AgentForge` (Public)
- [ ] 配置Python虚拟环境
- [ ] 安装核心依赖
- [ ] 获取国产模型API密钥

#### Day 2: 项目结构
- [ ] 创建目录结构
- [ ] 配置模块实现
- [ ] 日志系统实现

#### Day 3: 基础框架
- [ ] LLM客户端封装
- [ ] Hello World测试
- [ ] 首次Git提交

详细步骤见 `phase0-checklist.md`

---

## 文档索引

| 文档 | 用途 | 更新频率 |
|------|------|---------|
| `CLAUDE.md` | 项目总纲领（本文件） | 每阶段更新 |
| `MENTOR.md` | 技术导师系统定义 | 稳定 |
| `ai-agent-stack.md` | 技能栈定义 | 按需调整 |
| `learning-plan.md` | 学习计划 | 按需调整 |
| `skill-tracking.md` | 技能追踪 | 每阶段更新 |
| `phase0-checklist.md` | Phase 0详细步骤 | Phase 0完成后归档 |

---

## 核心概念速查

### Harness Engineering（2026核心范式）
```
前沿模型基准 90%+，真实任务完成率仅 ~24%
差距不在智能，而在 Harness（运行环境基础设施）

演进：
2022-24 Prompt Engineering → 完美指令
2025    Context Engineering → 相关信息供给
2026    Harness Engineering → 完整运行环境

核心组件：
• 约束与护栏（Claude Code Hooks）
• 反馈循环（Generator-Evaluator）
• 记忆与状态（LangGraph检查点）
• 人工审批
• 可观测性
• 评估框架
```

### Agent设计模式
```
ReAct: Thought → Action → Observation 循环
Plan-and-Execute: 先规划再执行
Self-Reflection: 自我反思纠错
```

### RAG流程
```
文档加载 → 文档切分 → 向量化 → 存储
    ↓
问题向量化 → 相似度检索 → 上下文构建 → LLM生成回答
```

---

## 关键资源

### 官方文档
- LangChain: https://python.langchain.com/
- LangGraph: https://langchain-ai.github.io/langgraph/
- 智谱AI: https://open.bigmodel.cn/dev/api
- 通义千问: https://help.aliyun.com/zh/dashscope/

### 学习资源
- DeepLearning.AI LangChain课程
- Anthropic Claude Code最佳实践
- OpenAI/Anthropic Harness Engineering博客

---

## 注意事项

1. **技能栈文档是目标**：`ai-agent-stack.md` 定义要掌握的技能，不随项目变动频繁调整
2. **学习计划是路线**：`learning-plan.md` 是执行路径，根据实际情况灵活调整
3. **技能追踪是反馈**：`skill-tracking.md` 记录进度，每阶段更新
4. **本文件是纲领**：`CLAUDE.md` 是总指挥，保持稳定但反映当前状态
5. **导师系统是风格**：`MENTOR.md` 定义技术指导风格，保持一致性

---

*最后更新：2026-04-08*
*下一里程碑：Phase 0 完成*