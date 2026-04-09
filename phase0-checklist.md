# Phase 0: 项目初始化检查清单

> 执行时间：Day 1-3
> 目标：搭建项目骨架，配置开发环境，建立Claude Code工作流

---

## Day 1: 环境准备

### 1.1 GitHub仓库创建

- [ ] 登录GitHub，创建新仓库
  - 仓库名：`AgentForge`
  - 描述：`A progressive AI Agent platform for task automation`
  - 可见性：Public
  - 勾选：Add a README file
  - 勾选：Add .gitignore (Python模板)
  - License：MIT

- [ ] 克隆仓库到本地
  ```bash
  cd /Users/lfq/file
  git clone https://github.com/[你的用户名]/AgentForge.git
  cd AgentForge
  ```

### 1.2 Python环境配置

- [ ] 检查Python版本 (需要3.10+)
  ```bash
  python --version
  ```

- [ ] 创建虚拟环境
  ```bash
  python -m venv venv
  source venv/bin/activate  # macOS/Linux
  ```

- [ ] 创建requirements.txt
  ```
  # Core
  langchain>=0.3.0
  langgraph>=0.2.0
  langchain-openai>=0.2.0
  langchain-community>=0.3.0

  # RAG
  chromadb>=0.5.0
  faiss-cpu>=1.8.0
  llama-index>=0.11.0
  pypdf>=4.0.0

  # LLM API (国产模型)
  zhipuai>=2.0.0
  dashscope>=1.14.0
  openai>=1.0.0  # 兼容OpenAI API格式

  # Utils
  python-dotenv>=1.0.0
  pydantic>=2.0.0
  pydantic-settings>=2.0.0
  rich>=13.0.0
  typer>=0.9.0

  # Dev
  pytest>=8.0.0
  pytest-asyncio>=0.23.0
  black>=24.0.0
  ruff>=0.3.0
  ```

- [ ] 安装依赖
  ```bash
  pip install -r requirements.txt
  ```

### 1.3 API密钥配置

- [ ] 选择国产模型，获取API密钥
  - 智谱AI: https://open.bigmodel.cn/
  - 通义千问: https://dashscope.console.aliyun.com/
  - DeepSeek: https://platform.deepseek.com/

- [ ] 创建.env文件
  ```bash
  cp .env.example .env
  ```

- [ ] 编辑.env文件，填入API密钥
  ```
  # 选择一个即可，后续可配置多模型切换
  ZHIPU_API_KEY=your_zhipu_api_key
  # DASHSCOPE_API_KEY=your_dashscope_api_key
  # DEEPSEEK_API_KEY=your_deepseek_api_key
  ```

---

## Day 2: 项目结构

### 2.1 创建目录结构

```bash
mkdir -p src/{agents,tools,memory,workflows,rag,harness,utils}
mkdir -p tests/{unit,integration}
mkdir -p docs
mkdir -p configs
mkdir -p data/{documents,vectors,logs}
touch src/__init__.py
touch src/agents/__init__.py
touch src/tools/__init__.py
touch src/memory/__init__.py
touch src/workflows/__init__.py
touch src/rag/__init__.py
touch src/harness/__init__.py
touch src/utils/__init__.py
```

### 2.2 核心配置文件

- [ ] 创建 `configs/config.yaml`
  ```yaml
  project:
    name: AgentForge
    version: 0.1.0
    description: A progressive AI Agent platform for task automation

  llm:
    provider: zhipu  # zhipu | dashscope | deepseek
    model: glm-4-flash
    temperature: 0.7
    max_tokens: 4096

  rag:
    vector_db: chroma
    embedding_model: text-embedding-3-small
    chunk_size: 500
    chunk_overlap: 50

  agent:
    max_iterations: 10
    timeout: 300

  harness:
    enable_guardrails: true
    enable_evaluation: true
    enable_monitoring: true
  ```

- [ ] 创建 `src/utils/config.py`
  ```python
  from pathlib import Path
  from typing import Optional
  from pydantic_settings import BaseSettings
  from pydantic import Field
  import yaml

  class LLMConfig(BaseSettings):
      provider: str = "zhipu"
      model: str = "glm-4-flash"
      temperature: float = 0.7
      max_tokens: int = 4096

      # API Keys
      zhipu_api_key: Optional[str] = None
      dashscope_api_key: Optional[str] = None
      deepseek_api_key: Optional[str] = None

      class Config:
          env_file = ".env"
          env_prefix = ""

  class RAGConfig(BaseSettings):
      vector_db: str = "chroma"
      embedding_model: str = "text-embedding-3-small"
      chunk_size: int = 500
      chunk_overlap: int = 50

  class AgentConfig(BaseSettings):
      max_iterations: int = 10
      timeout: int = 300

  class Config:
      """全局配置"""
      def __init__(self, config_path: str = "configs/config.yaml"):
          self.config_path = Path(config_path)
          self._load_config()
          self.llm = LLMConfig()
          self.rag = RAGConfig()
          self.agent = AgentConfig()

      def _load_config(self):
          if self.config_path.exists():
              with open(self.config_path) as f:
                  self._raw = yaml.safe_load(f)

  config = Config()
  ```

- [ ] 创建 `src/utils/logger.py`
  ```python
  import logging
  import sys
  from pathlib import Path
  from rich.logging import RichHandler

  def setup_logger(name: str = "AgentForge", log_file: str = None):
      logger = logging.getLogger(name)
      logger.setLevel(logging.DEBUG)

      # Console handler with rich formatting
      console_handler = RichHandler(rich_tracebacks=True)
      console_handler.setLevel(logging.INFO)

      # File handler
      if log_file:
          Path(log_file).parent.mkdir(parents=True, exist_ok=True)
          file_handler = logging.FileHandler(log_file)
          file_handler.setLevel(logging.DEBUG)
          file_formatter = logging.Formatter(
              '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
          )
          file_handler.setFormatter(file_formatter)
          logger.addHandler(file_handler)

      logger.addHandler(console_handler)
      return logger

  logger = setup_logger(log_file="data/logs/agentforge.log")
  ```

---

## Day 3: CLAUDE.md与基础框架

### 3.1 创建CLAUDE.md

在项目根目录创建 `CLAUDE.md`，这是Claude Code的项目记忆卡：

```markdown
# AgentForge 项目记忆

## 项目概述
AgentForge 是一个渐进式AI Agent平台，用于任务自动化。

## 技术栈
- 语言：Python 3.10+
- 框架：LangChain, LangGraph
- 向量数据库：ChromaDB/FAISS
- LLM：智谱AI / 通义千问 / DeepSeek

## 项目结构
```
src/
├── agents/      # Agent实现
├── tools/       # 工具定义
├── memory/      # 记忆系统
├── workflows/   # 工作流
├── rag/         # RAG模块
├── harness/     # Harness组件
└── utils/       # 工具函数
```

## 编码规范
- 使用Pydantic进行数据验证
- 所有函数添加类型注解
- 使用logger而非print
- 测试覆盖率目标：>60%

## Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- test: 测试用例
- refactor: 代码重构

## 当前阶段
Phase 0: 项目初始化

## 下一步任务
- [ ] 完成基础配置模块
- [ ] 实现LLM客户端封装
- [ ] 编写Hello World测试
```

### 3.2 基础模块实现

- [ ] 创建 `src/utils/llm_client.py`
  ```python
  from typing import Optional, List, Dict
  from zhipuai import ZhipuAI
  from .config import config
  from .logger import logger

  class LLMClient:
      """LLM客户端封装"""

      def __init__(self):
          self.config = config.llm
          self._init_client()

      def _init_client(self):
          if self.config.provider == "zhipu":
              self.client = ZhipuAI(api_key=self.config.zhipu_api_key)
          else:
              raise ValueError(f"Unsupported provider: {self.config.provider}")

      def chat(
          self,
          messages: List[Dict],
          temperature: Optional[float] = None,
          max_tokens: Optional[int] = None
      ) -> str:
          """发送对话请求"""
          try:
              response = self.client.chat.completions.create(
                  model=self.config.model,
                  messages=messages,
                  temperature=temperature or self.config.temperature,
                  max_tokens=max_tokens or self.config.max_tokens
              )
              return response.choices[0].message.content
          except Exception as e:
              logger.error(f"LLM API调用失败: {e}")
              raise

  # 单例
  llm_client = LLMClient()
  ```

- [ ] 创建 `tests/test_hello.py`
  ```python
  import pytest
  from src.utils.llm_client import llm_client

  def test_llm_connection():
      """测试LLM连接"""
      response = llm_client.chat([
          {"role": "user", "content": "你好，请回复'Hello AgentForge'"}
      ])
      assert response is not None
      assert len(response) > 0
      print(f"LLM响应: {response}")
  ```

- [ ] 运行测试
  ```bash
  pytest tests/test_hello.py -v
  ```

### 3.3 Git提交

- [ ] 检查文件状态
  ```bash
  git status
  ```

- [ ] 添加文件
  ```bash
  git add .
  ```

- [ ] 提交
  ```bash
  git commit -m "feat: 项目初始化，搭建基础框架"
  ```

- [ ] 推送
  ```bash
  git push origin main
  ```

---

## Phase 0 验收清单

- [ ] GitHub仓库创建完成
- [ ] Python虚拟环境配置完成
- [ ] 依赖安装成功
- [ ] API密钥配置正确
- [ ] 项目目录结构完整
- [ ] 配置模块可运行
- [ ] 日志系统可使用
- [ ] LLM客户端可调用API
- [ ] Hello World测试通过
- [ ] 首次Git提交完成

---

## 常见问题

### Q: 如何选择国产模型？
A: 建议从智谱AI开始，GLM-4-flash性价比高，API兼容OpenAI格式。

### Q: 虚拟环境激活后如何退出？
A: 运行 `deactivate` 命令。

### Q: 如何查看已安装的包？
A: 运行 `pip list` 或 `pip freeze`。

---

*准备完毕，明天开始执行！*