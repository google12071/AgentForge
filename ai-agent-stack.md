# 2026年AI Agent应用开发技能栈

> 基于行业JD与技术趋势调研，采用二八法则筛选核心技能。
> 更新时间：2026-04-09

---

## 技能栈要求表（按重要程度逆序排列）

| 技能名称 | 技能描述 | 学习前置依赖 | 学习方式 | 验收方式 | 应用场景 | 重要程度 |
|---------|---------|-------------|---------|---------|---------|------|
| **Agent编排与工作流** | 使用LangGraph构建可控、可观测的Agent状态机：状态定义、节点设计、条件边、检查点持久化、错误恢复 | LangChain基础、Python异步编程 | 项目实战 | 能够设计并实现包含状态管理、错误处理、人工干预的生产级Agent工作流 | 多步骤任务自动化、复杂业务流程编排 | ⭐⭐⭐⭐⭐ |
| **RAG与知识检索** | 构建检索增强生成系统：向量数据库选型、Embedding策略、混合检索、重排序、文档切分优化、检索召回率优化 | Python基础、向量数学概念 | 项目实战 | 能够实现准确率>85%的文档问答，准确率>85% | 企业知识库、智能客服、文档问答 | ⭐⭐⭐⭐⭐ |
| **Prompt Engineering** | 设计高效提示词：角色设定、任务拆解、输出格式约束、Few-shot示例、思维链引导、幻觉抑制 | 无特殊前置 | 框架学习+大量实践迭代 | 能够稳定控制LLM输出格式与质量，幻觉率显著降低 | 所有LLM应用的基础能力 | ⭐⭐⭐⭐⭐ |
| **Tool Use/Function Calling** | 设计与实现Agent工具体系：工具定义、参数验证、执行安全、结果解析、错误处理、工具选择策略 | Python基础、API设计经验 | 框架文档+项目实战 | 能够构建完整的工具生态，实现安全的工具调用与结果处理 | Agent与外部系统交互、API调用、数据查询 | ⭐⭐⭐⭐⭐ |
| **Context Engineering** | 上下文管理：Token优化、历史压缩、记忆系统设计、信息窗口策略、上下文动态裁剪、Claude Code实践应用 | Prompt Engineering、理解LLM Token机制 | Claude Code实战+深度文档学习 | 能够实现长对话场景下的稳定响应，Token成本可控 | 多轮对话、长任务执行、个性化Agent | ⭐⭐⭐⭐⭐ |
| **Problem Shaping（问题塑形）** | 将模糊业务目标转化为可执行的Agent任务：需求拆解、任务原子化、执行边界定义、成功标准设定 | 业务理解能力、系统工程思维 | 项目实战+复盘总结 | 能够将模糊需求转化为清晰的Agent执行计划 | 所有Agent项目的起点，决定系统成败 | ⭐⭐⭐⭐⭐ |
| **Claude Code最佳实践** | 掌握Claude Code高效使用：CLAUDE.md项目记忆卡、Skills开发与安装、Hooks安全钩子、/.claudeignore优化、Git Worktrees并行开发、MCP服务器集成 | Python基础、命令行操作 | 实战使用+官方文档学习 | 能够高效使用Claude Code进行Agent开发，配置完整的开发环境与安全护栏 | AI辅助开发的核心工具、Context Engineering实战载体 | ⭐⭐⭐⭐⭐ |
| **Harness Engineering** | 设计Agent运行环境：约束与护栏设计、工具编排、反馈循环、记忆与状态管理、人工审批流程、可观测性与追踪、评估框架集成、Generator-Evaluator双Agent模式 | Agent编排基础、测试基础 | 深度学习+实战项目 | 能够构建让Agent从Demo升级为可靠生产系统的完整Harness，任务完成率从24%提升至90%+ | Agent可靠性的决定性因素，从Demo到生产的桥梁 | ⭐⭐⭐⭐⭐ |
| **错误处理与自纠正** | Agent运行时异常处理：工具调用失败重试、计划动态调整、无限循环检测与终止、降级策略设计 | Agent编排基础、LangGraph检查点 | 深度学习+实战积累 | 能够构建具备自我纠错能力的Agent，生产环境稳定运行率>95% | 生产级Agent必备，决定系统可靠性 | ⭐⭐⭐⭐ |
| **Agent设计模式** | 掌握核心模式：ReAct、Plan-and-Execute、Self-Reflection、Chain-of-Thought、Graph-of-Thoughts、Plan-Act-Observe循环 | Prompt Engineering基础 | 框架文档+论文阅读+实战应用 | 能够根据场景选择合适模式并正确实现 | 任务规划、自我纠错、复杂推理 | ⭐⭐⭐⭐ |
| **LangChain核心组件** | 掌握Chain、Agent、Memory、Tool四大组件的设计与使用，理解LCEL表达式语言 | Python基础 | 官方教程+项目实战 | 能够使用LangChain构建完整的LLM应用 | 通用LLM应用开发的基础框架 | ⭐⭐⭐⭐ |
| **LlamaIndex** | 使用LlamaIndex构建知识驱动Agent：数据索引、查询引擎、检索优化、与LangGraph协同使用 | Python基础、RAG概念 | 官方教程+知识库项目 | 能够构建高质量的知识检索与问答系统，可作为LangGraph工具集成 | 企业知识库、私有数据问答、文档智能处理 | ⭐⭐⭐⭐ |
| **MCP（Model Context Protocol）** | 理解并应用MCP协议：工具服务器设计、资源暴露、客户端集成、安全治理、跨框架互操作、与Claude Code集成 | Python基础、HTTP协议理解 | 官方文档+实践集成 | 能够实现自定义MCP Server并集成到Agent系统和Claude Code | 工具标准化、跨框架互操作、企业系统集成 | ⭐⭐⭐⭐ |
| **OpenClaw Skills Framework** | 掌握OpenClaw开源Agent框架：Skills开发规范、私有化部署、安全护栏配置、审计回放机制、质量效率指标体系建立 | Python基础、Agent开发经验 | 官方文档+开源社区实践 | 能够构建私有Skills、实现可审计的Agent系统、将Demo升级为可靠生产系统 | 自托管Agent、企业私有化部署、审计合规 | ⭐⭐⭐⭐ |
| **Vibe Coding最佳实践** | AI辅助开发方法论：描述→生成→测试→迭代循环、渐进式细化、人工审查要点、部署验证、何时用Vibe vs传统开发 | Claude Code使用经验 | 实战项目迭代积累 | 能够通过Vibe Coding高效完成MVP开发，理解产出代码并确保质量 | 快速原型开发、MVP验证、AI辅助迭代开发 | ⭐⭐⭐⭐ |
| **多Agent协作** | 设计与实现多Agent系统：角色分工、通信协议（A2A）、协作模式、冲突解决、结果聚合、层级Agent架构 | Agent编排基础、分布式系统思维 | 项目实战 | 能够实现2-5个Agent的高效协作，完成复杂任务拆解与执行 | 复杂业务场景、专家团队模拟、代码审查流程 | ⭐⭐⭐ |
| **向量数据库** | 选型与使用：Pinecone/Weaviate/FAISS/Qdrant/ChromaDB，理解索引策略与检索性能、混合检索实现 | 数据库基础、向量概念 | 工具文档+性能对比实验 | 能够选型合适的向量库并进行性能优化 | RAG系统、语义搜索、推荐系统 | ⭐⭐⭐  |
| **Agent评估与监控** | 实现Agent效果评估：单元测试、集成测试、对抗测试、LLM-as-a-Judge模式、影子测试，使用LangSmith/LangFuse进行可观测性建设 | 测试基础、软件工程实践 | 工具文档+测试项目实战 | 能够构建完整的评估体系并实现生产监控，建立质量/效率指标体系 | 生产级Agent的质量保障 | ⭐⭐⭐ |
| **成本优化与Token管理** | API调用成本控制：模型路由优化（按复杂度选模型）、请求批处理、缓存策略、Token预算监控、使用量分析 | LLM API集成经验 | 实战经验积累+数据驱动分析 | 能够将Agent运行成本控制在合理范围，ROI可量化 | 企业级Agent部署的商业可行性 | ⭐⭐⭐ |
| **LLM API集成** | 熟练集成主流LLM：OpenAI、Claude API、国产模型（智谱/通义/DeepSeek），理解API差异、延迟与成本权衡、模型能力边界 | Python基础、HTTP API | 各平台文档+API实践 | 能够灵活切换不同LLM并进行成本与效果平衡 | 所有LLM应用的模型层 | ⭐⭐⭐ |
| **Python AI生态** | 掌握Python核心库：FastAPI（API服务）、Pydantic（数据验证）、asyncio（异步编程）、日志与异常处理 | Python语法基础 | 项目实战+文档学习 | 能够使用Python构建生产级AI服务 | AI服务开发的标准语言生态 | ⭐⭐⭐ |
| **安全与治理** | Agent安全设计：Prompt注入防护、权限控制、审计日志、输出过滤、敏感数据处理、OWASP Agent安全Top10、OpenClaw安全护栏 | 安全基础概念 | 安全文档学习+安全测试实践 | 能够实现基本的安全防护机制，满足合规要求 | 企业级Agent部署、合规要求（EU AI Act等） | ⭐⭐⭐ |

---

## 二八法则核心技能

**Phase 1必修（前9项，解决95%问题）**：

| 优先级 | 技能名称 | 学习路径定位 |
|--------|---------|-------------|
| 1 | Prompt Engineering | 基础层，无前置 |
| 2 | Problem Shaping | 规划层，决定成败 |
| 3 | Claude Code最佳实践 | 工具层，学习载体 |
| 4 | Vibe Coding最佳实践 | 方法层，迭代开发 |
| 5 | LangChain核心组件 | 框架入口 |
| 6 | RAG与知识检索 | 最核心应用场景 |
| 7 | Tool Use/Function Calling | Agent能力边界 |
| 8 | Agent编排与工作流(LangGraph) | 生产级必备 |
| 9 | Harness Engineering | 可靠性保障，Demo→生产 |

---

## 技能依赖关系图

```
┌─────────────────────────────────────────────────────────────┐
│                    基础层 (Foundation)                        │
│  Prompt Engineering ──────────────────────────────────────► │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    工具与方法层 (Tools & Methods)            │
│  Claude Code最佳实践 ◄────────────► Vibe Coding最佳实践     │
│  (Context Engineering载体)          (迭代开发方法论)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    规划层 (Planning)                          │
│  Problem Shaping ──────────────────► Agent设计模式(ReAct等)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    框架层 (Framework)                         │
│  LangChain核心组件                                            │
│       ├──► Tool Use/Function Calling                         │
│       ├──► RAG与知识检索                                      │
│       │       ├──► 向量数据库                                 │
│       │       └──► LlamaIndex                                 │
│       └──► Agent编排与工作流(LangGraph)                       │
│               ├──► 错误处理与自纠正                           │
│               ├──► 检查点与状态持久化                         │
│               ├──► 多Agent协作                                │
│               └──► MCP协议 ──────► OpenClaw Skills Framework │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Harness层 (Reliability)                    │
│  Harness Engineering                                          │
│       ├──► 约束与护栏 (Claude Code Hooks)                     │
│       ├──► 反馈循环 (Generator-Evaluator)                     │
│       ├──► 成本优化与Token管理                                │
│       ├──► Agent评估与监控                                    │
│       └──► 安全与治理                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 学习资源推荐

| 技能类别 | 推荐资源 |
|---------|---------|
| LangChain/LangGraph | 官方文档 + DeepLearning.AI课程 |
| RAG | LlamaIndex官方教程 + Pinecone文档 |
| Agent模式 | LangGraph教程 + 相关论文（ReAct等） |
| MCP | Anthropic MCP官方文档 |
| Claude Code | Anthropic官方最佳实践文档 |
| Harness Engineering | OpenAI/Anthropic官方博客 + Martin Fowler文章 |
| Python生态 | FastAPI官方文档 + Pydantic文档 |

---

## 核心概念说明

### Harness Engineering（2026年核心范式）

**背景问题**：前沿模型基准测试得分 90%+，但真实任务完成率仅 ~24%。差距不在智能，而在 Harness。

**演进路径**：
- 2022-24: Prompt Engineering → 关注"完美指令"
- 2025: Context Engineering → 关注"相关信息供给"
- 2026: Harness Engineering → 关注"完整运行环境"

**行业验证**：
- Vercel 移除80%工具，准确率 80%→100%，速度提升3.5倍
- LangChain 仅改Harness不改模型，排名 Top30→Top5
- OpenAI 用Harness构建100万行代码，零人工编写

**核心组件**：
| 组件 | 说明 | 对应实践 |
|------|------|---------|
| 约束与护栏 | 定义Agent行为边界 | Claude Code Hooks、OpenClaw安全护栏 |
| 工具编排 | 提供原子工具，让模型做计划 | Tool Use、MCP Server |
| 反馈循环 | Generator-Evaluator双Agent模式 | Self-Reflection、LLM-as-Judge |
| 记忆与状态 | 跨会话持久化 | LangGraph检查点、Context Engineering |
| 人工审批 | 关键决策点人工介入 | Human-in-the-Loop |
| 可观测性 | Step-Level Tracing | LangSmith、LangFuse |
| 评估框架 | 自动化测试与回归检测 | Harbor、DeepEval |

---

## 暂时移除的技能（进阶选修）

| 技能 | 移除原因 | 后续计划 |
|------|---------|---------|
| 微调与模型优化 | 90天聚焦应用层，API调用覆盖90%场景 | 第二阶段进阶 |
| 语音/多模态 | 非核心必修，特定场景才需要 | 特定项目选修 |
| 生产部署与运维 | 已被Harness Engineering覆盖 | 整合到Harness |

---

*本文档将随学习进展持续更新。*