# AgentForge - 90天学习计划

> 渐进式通用任务Agent平台开发路线
> 更新时间：2026-04-09

---

## 项目概述

**项目名称**：AgentForge - 通用任务Agent平台

**项目愿景**：从零构建一个能够理解自然语言指令、自主规划任务、调用工具执行、反馈结果的任务自动化平台

**核心价值**：
- 覆盖AI Agent核心技能栈90%知识点
- 采用渐进式迭代，每一步都有可运行产出
- 最终产出可复用的技术资产

---

## 迭代路线总览

| Phase | 时间 | 核心目标 | 技能覆盖 | 产出 |
|-------|------|----------|----------|------|
| Phase 0 | Day 1-3 | 项目初始化 | Claude Code, Git, Python环境 | 项目骨架 |
| Phase 1 | Day 4-15 | 基础问答Agent | Prompt Engineering, LLM API | CLI问答工具 |
| Phase 2 | Day 16-30 | RAG知识库 | 向量数据库, 文档处理, 检索 | 知识问答模块 |
| Phase 3 | Day 31-50 | 工具调用Agent | Tool Use, Function Calling | 工具执行引擎 |
| Phase 4 | Day 51-70 | 工作流Agent | LangGraph, 状态管理, 错误处理 | 工作流引擎 |
| Phase 5 | Day 71-85 | Harness工程化 | 评估, 监控, 安全护栏 | 生产就绪系统 |
| Phase 6 | Day 86-90 | 平台整合 | MCP, 多Agent, 文档 | 完整平台 |

---

## Phase 0: 项目初始化 (Day 1-3)

### 目标
搭建项目骨架，配置开发环境，建立Claude Code工作流

### 技能覆盖
- Claude Code最佳实践
- Python项目结构
- Git仓库管理
- 环境配置

### 任务清单

#### Day 1: 环境准备 ✅
- [x] 项目目录已存在
- [x] 配置Python虚拟环境 (Python 3.12.12，使用 uv)
- [x] 安装核心依赖 (149 packages)
  ```
  # 使用 uv 管理依赖
  uv venv --python 3.12
  uv sync
  
  # 已安装核心包:
  # langchain 1.2.15
  # langgraph 1.1.6
  # chromadb 0.4.24 (macOS Intel 兼容)
  # llama-index 0.14.20
  # onnxruntime 1.19.2
  ```
- [ ] 配置国产模型API密钥 (已有通义千问/DeepSeek)

#### Day 2: 项目结构
- [ ] 创建项目目录结构
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
  ├── .env.example         # 环境变量模板
  ├── CLAUDE.md            # Claude Code项目记忆
  └── README.md            # 项目说明
  ```
- [ ] 编写CLAUDE.md项目记忆卡
- [ ] 配置.gitignore和.claudeignore

#### Day 3: 基础框架
- [ ] 实现配置管理模块
- [ ] 实现日志系统
- [ ] 编写Hello World测试
- [ ] 提交第一次commit

### 验收标准
- [ ] 项目结构完整
- [ ] 环境配置正确，API可调用
- [ ] Claude Code可以正常工作
- [ ] Git仓库初始化完成

---

## Phase 1: 基础问答Agent (Day 4-15)

### 目标
构建一个能够进行多轮对话的基础问答Agent

### 技能覆盖
| 技能 | 覆盖程度 | 实践内容 |
|------|---------|---------|
| Prompt Engineering | ⭐⭐⭐⭐⭐ | 角色设定、输出格式、Few-shot |
| LLM API集成 | ⭐⭐⭐⭐ | 国产模型API调用、错误处理 |
| Context Engineering | ⭐⭐⭐ | 对话历史管理、Token计数 |
| Problem Shaping | ⭐⭐⭐ | 任务边界定义 |
| Python AI生态 | ⭐⭐⭐ | Pydantic数据模型 |

### 功能规划

#### v0.1: 单轮问答 (Day 4-6)
- [ ] 实现LLM客户端封装
- [ ] 实现基础Prompt模板
- [ ] CLI单轮问答功能
- [ ] 测试与调优

#### v0.2: 多轮对话 (Day 7-10)
- [ ] 实现对话历史管理
- [ ] 实现Token计数与限制
- [ ] 多轮对话CLI
- [ ] 对话持久化(JSON)

#### v0.3: Prompt工程优化 (Day 11-13)
- [ ] 角色设定实验
- [ ] 输出格式约束(JSON输出)
- [ ] Few-shot示例设计
- [ ] 幻觉抑制策略

#### v0.4: 问题塑形实践 (Day 14-15)
- [ ] 定义Agent能力边界
- [ ] 实现任务分类器
- [ ] 未知任务友好拒绝
- [ ] 文档与测试

### 技术深度要求

**Prompt Engineering实践**：
```python
# 角色设定示例
SYSTEM_PROMPT = """
你是AgentForge助手，一个任务自动化平台。

## 能力范围
- 回答一般性问题
- 解释技术概念
- 提供任务规划建议

## 输出格式
当需要结构化输出时，使用JSON格式：
{"answer": "...", "confidence": 0.95}

## 限制
- 不执行实际操作（此阶段无工具）
- 不访问外部数据
- 明确告知能力边界
"""
```

**Context Engineering实践**：
```python
# 对话历史管理
class ConversationManager:
    def __init__(self, max_tokens: int = 4000):
        self.history = []
        self.max_tokens = max_tokens

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self._trim_if_needed()

    def _trim_if_needed(self):
        # Token超限时压缩历史
        while self._count_tokens() > self.max_tokens:
            self._summarize_old_messages()
```

### 验收标准
- [ ] CLI可进行多轮对话
- [ ] 对话历史正确管理
- [ ] Token使用可控
- [ ] Prompt效果稳定
- [ ] 测试覆盖率>60%

---

## Phase 2: RAG知识库 (Day 16-30)

### 目标
为Agent添加知识检索能力，实现基于文档的问答

### 技能覆盖
| 技能 | 覆盖程度 | 实践内容 |
|------|---------|---------|
| RAG与知识检索 | ⭐⭐⭐⭐⭐ | 向量数据库、检索优化 |
| 向量数据库 | ⭐⭐⭐⭐ | ChromaDB 0.4.x (macOS Intel 兼容) |
| LlamaIndex | ⭐⭐⭐⭐ | 文档索引、查询引擎 (0.14.20) |
| 文档处理 | ⭐⭐⭐ | 文档加载、切分策略 |

### 功能规划

#### v0.5: 向量数据库集成 (Day 16-20)
- [ ] ChromaDB 0.4.x 使用 (已安装)
- [ ] 实现Embedding接口 (通义千问 text-embedding-v3)
- [ ] 文档向量化存储
- [ ] 基础检索功能

#### v0.6: 文档处理管道 (Day 21-24)
- [ ] 多格式文档加载 (PDF, Markdown, TXT)
- [ ] 文档切分策略实验
  - 固定长度切分
  - 语义切分
  - 递归切分
- [ ] 切分效果评估

#### v0.7: RAG问答集成 (Day 25-27)
- [ ] RAG Pipeline实现
- [ ] 检索结果重排序
- [ ] 上下文注入Prompt
- [ ] 问答效果优化

#### v0.8: LlamaIndex集成 (Day 28-30)
- [ ] LlamaIndex索引构建
- [ ] 查询引擎配置
- [ ] 作为工具集成到Agent
- [ ] 性能对比测试

### 技术深度要求

**RAG核心实现**：
```python
class RAGPipeline:
    def __init__(self, vector_db, embedding_model, llm):
        self.db = vector_db
        self.embedder = embedding_model
        self.llm = llm

    def query(self, question: str, top_k: int = 5):
        # 1. 问题向量化
        query_embedding = self.embedder.embed(question)

        # 2. 向量检索
        docs = self.db.search(query_embedding, top_k)

        # 3. 构建上下文
        context = self._build_context(docs)

        # 4. 生成回答
        response = self.llm.generate(
            prompt=self._build_prompt(question, context)
        )

        return response, docs  # 返回来源
```

**检索优化策略**：
- 混合检索：向量 + 关键词
- 重排序：Cross-Encoder精排
- 元数据过滤：按时间、来源过滤

### 验收标准
- [ ] 可导入多种格式文档
- [ ] 检索准确率>80%
- [ ] 问答效果可接受
- [ ] 测试覆盖率>60%

---

## Phase 3: 工具调用Agent (Day 31-50)

### 目标
为Agent添加工具调用能力，实现任务执行

### 技能覆盖
| 技能 | 覆盖程度 | 实践内容 |
|------|---------|---------|
| Tool Use/Function Calling | ⭐⭐⭐⭐⭐ | 工具定义、调用、错误处理 |
| Agent设计模式 | ⭐⭐⭐⭐ | ReAct模式实现 |
| 错误处理与自纠正 | ⭐⭐⭐ | 工具失败重试、降级 |
| 安全与治理 | ⭐⭐⭐ | 工具权限控制 |

### 功能规划

#### v0.9: 工具系统框架 (Day 31-35)
- [ ] 工具基类设计
- [ ] 工具注册机制
- [ ] 参数验证 (Pydantic)
- [ ] 工具调用抽象层

#### v1.0: 核心工具实现 (Day 36-40)
- [ ] 计算器工具
- [ ] 网络搜索工具
- [ ] 文件操作工具
- [ ] 数据查询工具

#### v1.1: ReAct模式实现 (Day 41-45)
- [ ] Thought-Action-Observation循环
- [ ] 工具选择策略
- [ ] 执行结果解析
- [ ] 多步任务执行

#### v1.2: 错误处理与安全 (Day 46-50)
- [ ] 工具调用失败重试
- [ ] 参数校验与类型转换
- [ ] 危险操作拦截
- [ ] 执行日志审计

### 技术深度要求

**工具定义规范**：
```python
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    """计算器工具输入"""
    expression: str = Field(description="数学表达式，如 '2 + 3 * 4'")

class CalculatorTool:
    name = "calculator"
    description = "执行数学计算"
    input_schema = CalculatorInput

    def execute(self, expression: str) -> dict:
        try:
            result = eval(expression)  # 实际使用ast.literal_eval
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

**ReAct循环实现**：
```python
class ReActAgent:
    def run(self, task: str):
        while not self._is_complete():
            # Thought: 思考下一步
            thought = self._think(task)

            # Action: 选择并执行工具
            action, args = self._select_action(thought)
            observation = self._execute_action(action, args)

            # 更新记忆
            self.memory.add(thought, action, observation)

            # 检查是否完成
            if self._should_finish(observation):
                break

        return self._generate_final_answer()
```

### 验收标准
- [ ] 至少4个工具可用
- [ ] ReAct循环正确执行
- [ ] 错误处理完善
- [ ] 测试覆盖率>70%

---

## Phase 4: 工作流Agent (Day 51-70)

### 目标
使用LangGraph构建可控、可观测的Agent工作流

### 技能覆盖
| 技能 | 覆盖程度 | 实践内容 |
|------|---------|---------|
| Agent编排与工作流 | ⭐⭐⭐⭐⭐ | LangGraph状态图设计 |
| LangChain核心组件 | ⭐⭐⭐⭐⭐ | LCEL、组件集成 |
| 错误处理与自纠正 | ⭐⭐⭐⭐ | 检查点、状态恢复 |
| 多Agent协作 | ⭐⭐⭐ | 简单的多Agent协同 |

### 功能规划

#### v1.3: LangGraph基础 (Day 51-55)
- [ ] LangGraph状态定义
- [ ] 节点函数实现
- [ ] 条件边设计
- [ ] 基础工作流运行

#### v1.4: 完整任务工作流 (Day 56-60)
- [ ] 任务理解节点
- [ ] 规划节点
- [ ] 执行节点
- [ ] 反馈节点
- [ ] 错误处理节点

#### v1.5: 状态管理与检查点 (Day 61-65)
- [ ] 状态持久化
- [ ] 检查点机制
- [ ] 中断恢复
- [ ] 人工干预点

#### v1.6: 多Agent协作初步 (Day 66-70)
- [ ] 规划Agent + 执行Agent
- [ ] Agent间通信
- [ ] 结果聚合
- [ ] 测试与文档

### 技术深度要求

**LangGraph工作流定义**：
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    task: str
    plan: list
    current_step: int
    results: list
    errors: list

def build_workflow():
    graph = StateGraph(AgentState)

    # 添加节点
    graph.add_node("understand", understand_task)
    graph.add_node("plan", create_plan)
    graph.add_node("execute", execute_step)
    graph.add_node("reflect", reflect_result)

    # 添加边
    graph.set_entry_point("understand")
    graph.add_edge("understand", "plan")
    graph.add_edge("plan", "execute")
    graph.add_conditional_edges(
        "execute",
        should_continue,
        {"continue": "execute", "reflect": "reflect", "error": "handle_error"}
    )
    graph.add_edge("reflect", END)

    return graph.compile()
```

### 验收标准
- [ ] 工作流可视化
- [ ] 状态正确流转
- [ ] 检查点可用
- [ ] 测试覆盖率>70%

---

## Phase 5: Harness工程化 (Day 71-85)

### 目标
构建完整的Harness，让Agent从Demo升级为生产就绪系统

### 技能覆盖
| 技能 | 覆盖程度 | 实践内容 |
|------|---------|---------|
| Harness Engineering | ⭐⭐⭐⭐⭐ | 约束、反馈、评估完整实践 |
| Agent评估与监控 | ⭐⭐⭐⭐ | 测试框架、可观测性 |
| 成本优化与Token管理 | ⭐⭐⭐⭐ | Token预算、模型路由 |
| 安全与治理 | ⭐⭐⭐⭐ | 安全护栏、审计 |

### 功能规划

#### v1.7: 评估框架 (Day 71-75)
- [ ] 测试用例设计
- [ ] LLM-as-a-Judge实现
- [ ] 自动化测试流水线
- [ ] 质量指标看板

#### v1.8: 监控与可观测 (Day 76-80)
- [ ] 执行追踪 (LangSmith集成)
- [ ] 性能指标收集
- [ ] 错误告警
- [ ] 日志聚合

#### v1.9: 安全护栏 (Day 81-83)
- [ ] Prompt注入检测
- [ ] 敏感信息过滤
- [ ] 操作审计日志
- [ ] 权限控制

#### v2.0: Harness整合 (Day 84-85)
- [ ] Generator-Evaluator模式
- [ ] 完整Harness配置
- [ ] 性能基准测试
- [ ] 文档更新

### 技术深度要求

**Harness核心组件**：
```python
class AgentHarness:
    """Agent Harness - 约束、监控、评估一体化"""

    def __init__(self):
        self.guardrails = GuardrailSystem()
        self.evaluator = EvaluatorSystem()
        self.monitor = MonitorSystem()
        self.cost_tracker = CostTracker()

    def run(self, task: str):
        # 1. 安全检查
        if not self.guardrails.is_safe(task):
            return {"error": "任务不安全，已拒绝执行"}

        # 2. 执行任务
        with self.monitor.trace(task) as trace:
            result = self.agent.execute(task)
            trace.record(result)

        # 3. 评估结果
        evaluation = self.evaluator.evaluate(task, result)

        # 4. 成本记录
        self.cost_tracker.record(trace.token_usage)

        return result, evaluation
```

### 验收标准
- [ ] 评估框架可用
- [ ] 监控指标完整
- [ ] 安全护栏生效
- [ ] 测试覆盖率>80%

---

## Phase 6: 平台整合 (Day 86-90)

### 目标
完成平台整合，产出完整文档

### 技能覆盖
| 技能 | 覆盖程度 | 实践内容 |
|------|---------|---------|
| MCP协议 | ⭐⭐⭐⭐ | MCP Server实现 |
| OpenClaw Skills | ⭐⭐⭐⭐ | Skills规范实践 |
| 多Agent协作 | ⭐⭐⭐⭐ | 完整多Agent系统 |

### 功能规划

#### v2.1: MCP集成 (Day 86-87)
- [ ] 实现MCP Server
- [ ] 工具标准化暴露
- [ ] Claude Code集成测试

#### v2.2: 多Agent完善 (Day 88-89)
- [ ] 规划Agent专业化
- [ ] 执行Agent专业化
- [ ] 评估Agent专业化
- [ ] 协作模式优化

#### v2.3: 文档与发布 (Day 90)
- [ ] 完整README
- [ ] API文档
- [ ] 架构设计文档
- [ ] 部署指南
- [ ] GitHub Release

### 验收标准
- [ ] MCP Server可用
- [ ] 多Agent协作正常
- [ ] 文档完整
- [ ] 可演示运行

---

## 技能覆盖矩阵

| Phase | 覆盖技能 | 覆盖程度 |
|-------|---------|---------|
| Phase 0 | Claude Code, Git, Python环境 | 基础实践 |
| Phase 1 | Prompt Engineering, LLM API, Context Engineering | ⭐⭐⭐ |
| Phase 2 | RAG, 向量数据库, LlamaIndex, 文档处理 | ⭐⭐⭐⭐ |
| Phase 3 | Tool Use, Function Calling, ReAct, 错误处理 | ⭐⭐⭐⭐ |
| Phase 4 | LangGraph, 工作流编排, 状态管理, 多Agent | ⭐⭐⭐⭐⭐ |
| Phase 5 | Harness Engineering, 评估, 监控, 安全 | ⭐⭐⭐⭐⭐ |
| Phase 6 | MCP, OpenClaw, 多Agent协作, 文档 | ⭐⭐⭐⭐ |

---

## 每日工作流建议

### 工作日 (2-3小时)
```
18:00 - 18:30  复盘昨日进度，阅读文档
18:30 - 20:00  核心开发时间
20:00 - 20:30  测试与调试
20:30 - 21:00  提交代码，更新笔记
```

### 周末 (4-6小时)
```
上午: 深度开发，攻克难点
下午: 测试优化，文档整理
晚上: 复盘总结，规划下周
```

---

## Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
test: 测试用例
refactor: 代码重构
chore: 构建/工具变动

示例:
feat(rag): 实现文档向量化和检索功能
fix(agent): 修复工具调用错误处理
docs(readme): 更新安装说明
```

---

*本文档将随项目进展持续更新。*