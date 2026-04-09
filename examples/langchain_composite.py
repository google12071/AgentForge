"""
LangChain 核心技术综合示例
涵盖: LCEL, Prompts, Models, Memory, Retrieval, Tools, Chains

运行此示例可理解LangChain核心原理
"""

import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# LangChain 1.x verbose/debug 全局设置
from langchain_core.globals import set_verbose, set_debug

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI

# ============================================================
# 1. 配置 - 使用通义千问（兼容OpenAI接口）
# ============================================================

# 通义千问可以通过OpenAI兼容接口调用
# base_url: https://dashscope.aliyuncs.com/compatible-mode/v1

# 加载.env环境变量
load_dotenv()

qwen_api_key = os.getenv("QWEN_API_KEY", "")
if not qwen_api_key:
    print("错误: 请在.env文件中设置QWEN_API_KEY")
    exit(1)

os.environ["OPENAI_API_KEY"] = qwen_api_key
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

MODEL_NAME = "qwen-plus"


# ============================================================
# 2. Models - LLM抽象层
# ============================================================

def invoke_models():
    """演示: Model初始化和基本调用"""
    print("\n" + "=" * 60)
    print("【1. Models - LLM抽象层】")
    print("=" * 60)

    # 方式1：全局设置verbose（显示调用流程）
    # set_verbose(True)  # 开启后会打印链的输入输出
    # set_debug(True)    # 开启后显示更详细的内部信息

    # ChatModel - 聊天模型（推荐使用）
    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=0.7,
        max_tokens=1000,
    )

    # 基本调用（verbose在invoke中已废弃，用全局设置或callbacks）
    print("\n[开启verbose模式演示]")
    set_verbose(True)  # 全局开启
    response = llm.invoke("你是谁？介绍下你自己！")
    set_verbose(False)  # 关闭避免干扰后续输出
    print(f"\n基本调用结果:\n{response.content}")

    # 批量调用
    responses = llm.batch([
        "什么是Agent?",
        "什么是RAG?",
    ])
    print(f"\n批量调用结果 (2个问题):")
    for i, r in enumerate(responses):
        print(f"  {i + 1}. {r.content[:50]}...")

    return llm


# ============================================================
# 3. Prompts - Prompt模板管理
# ============================================================

def build_prompts():
    """演示: PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate"""
    print("\n" + "=" * 60)
    print("【2. Prompts - Prompt模板管理】")
    print("=" * 60)

    # 3.1 PromptTemplate - 简单模板
    simple_template = PromptTemplate.from_template(
        "请用{style}的风格，解释{concept}这个概念,{output_format}格式输出"
    )
    prompt = simple_template.format(style="幽默", concept="区块链", output_format="Markdown")
    print(f"\nPromptTemplate生成:\n{prompt}")

    # 3.2 ChatPromptTemplate - 聊天模板（推荐）
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，擅长{skill}"),
        ("human", "{question},{output_format}形式输出，至少包括{num}点"),
    ])
    messages = chat_template.format_messages(
        role="技术顾问",
        skill="AI技术讲解",
        question="LangChain的核心优势是什么？", output_format="表格", num=3
    )
    print(f"\nChatPromptTemplate生成:")
    for msg in messages:
        print(f"  [{msg.type}]: {msg.content}")

    # 3.3 FewShotPromptTemplate - 少样本提示
    examples = [
        {"input": "苹果", "output": "红色, 圆形, 水果"},
        {"input": "汽车", "output": "金属, 四轮, 交通工具"},
    ]
    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="输入: {input}\n输出: {output}"
    )
    fewshot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="根据示例，用简洁词语描述物品特征:",
        suffix="输入: {item}\n输出:",
        input_variables=["item"],
    )
    fewshot_prompt = fewshot_template.format(item="计算机")
    print(f"\nFewShotPromptTemplate生成:\n{fewshot_prompt}")

    # 3.4 MessagesPlaceholder - 动态消息占位（用于Memory）
    template_with_memory = ChatPromptTemplate.from_messages([
        ("system", "你是一个AI助手"),
        MessagesPlaceholder(variable_name="history"),  # 对话历史占位
        ("human", "{question}"),
    ])
    print(f"\nMessagesPlaceholder模板（用于多轮对话）:")
    print(f"  变量: history(动态), question(用户输入)")

    return chat_template


# ============================================================
# 4. LCEL - LangChain Expression Language (核心!)
# ============================================================

def run_lcel(llm):
    """演示: LCEL链式操作, Runnable接口"""
    print("\n" + "=" * 60)
    print("【3. LCEL - LangChain Expression Language】核心!")
    print("=" * 60)

    # 4.1 简单链: prompt | llm | parser
    prompt = ChatPromptTemplate.from_messages([
        ("human", "{question}")
    ])
    parser = StrOutputParser()

    # 链式组合 - 这是LCEL的核心语法
    chain = prompt | llm | parser

    print("\n简单链: prompt | llm | parser")
    result = chain.invoke({"question": "用一句话解释LCEL"})
    print(f"结果: {result}")

    # 4.2 RunnablePassthrough - 数据透传
    passthrough_chain = RunnablePassthrough.assign(
        extra_info=lambda x: {"timestamp": "2026-04-09"}
    ) | prompt | llm | parser

    print("\nRunnablePassthrough - 添加额外信息:")
    result = passthrough_chain.invoke({"question": "今天日期"})
    print(f"结果: {result}")

    # 4.3 RunnableParallel - 并行执行
    parallel_chain = RunnableParallel(
        answer=prompt | llm | parser,
        question_length=RunnableLambda(lambda x: len(x["question"])),
    )

    print("\nRunnableParallel - 并行执行多个分支:")
    result = parallel_chain.invoke({"question": "什么是Agent"})
    print(f"  answer: {result['answer'][:50]}...")
    print(f"  question_length: {result['question_length']}")

    # 4.4 复合链 - 组合使用
    complex_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}"),
        ("human", "{question}"),
    ])

    full_chain = (
            RunnablePassthrough.assign(role=lambda _: "AI技术专家")
            | complex_prompt
            | llm
            | parser
    )

    print("\n复合链: assign + prompt + llm + parser:")
    result = full_chain.invoke({"question": "LangChain vs LangGraph的区别"})
    print(f"结果: {result[:100]}...")

    return chain


# ============================================================
# 5. Memory - 对话历史管理
# ============================================================

def manage_memory(llm):
    """演示: ChatMessageHistory对话历史管理"""
    print("\n" + "=" * 60)
    print("【4. Memory - 对话历史管理】")
    print("=" * 60)

    # LangChain v1.x 推荐使用 ChatMessageHistory
    # 5.1 ChatMessageHistory - 保存所有历史
    history = ChatMessageHistory()

    # 添加历史对话
    history.add_user_message("我叫小明")
    history.add_ai_message("你好小明，很高兴认识你！")

    print("\nChatMessageHistory - 添加2轮对话:")
    print(f"  当前历史消息数: {len(history.messages)}")
    for msg in history.messages:
        print(f"  [{msg.type}]: {msg.content}")

    # 5.2 模拟滑动窗口（只保留最近N轮）
    def get_recent_messages(history: ChatMessageHistory, k: int = 2):
        """获取最近k轮对话"""
        messages = history.messages
        # 每轮包含user+ai两条消息，所以取最近k*2条
        return messages[-(k * 2):] if len(messages) > k * 2 else messages

    # 添加更多对话
    history.add_user_message("第1轮问题")
    history.add_ai_message("第1轮回答")
    history.add_user_message("第2轮问题")
    history.add_ai_message("第2轮回答")
    history.add_user_message("第3轮问题")
    history.add_ai_message("第3轮回答")

    recent = get_recent_messages(history, k=2)
    print("\n滑动窗口 (k=2, 最近2轮):")
    for msg in recent:
        print(f"  [{msg.type}]: {msg.content}")

    # 5.3 结合Memory的对话链
    memory_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    memory_chain = memory_prompt | llm | StrOutputParser()

    # 带历史的多轮对话
    print("\n带Memory的多轮对话演示:")
    result1 = memory_chain.invoke({
        "history": get_recent_messages(history, k=1),  # 只用最近1轮作为历史
        "question": "你还记得我的名字吗？"
    })
    print(f"  用户: 你还记得我的名字吗？")
    print(f"  AI: {result1}")

    return history

    return memory


# ============================================================
# 6. Output Parsers - 结构化输出
# ============================================================

class AnalysisResult(BaseModel):
    """分析结果结构"""
    topic: str = Field(description="主题")
    confidence: float = Field(description="置信度 0-1")
    keywords: List[str] = Field(description="关键词列表")
    summary: str = Field(description="一句话总结")


def run_output_parsers(llm):
    """演示: PydanticOutputParser - 强制结构化输出"""
    print("\n" + "=" * 60)
    print("【5. Output Parsers - 结构化输出】")
    print("=" * 60)

    parser = PydanticOutputParser(pydantic_object=AnalysisResult)

    # 自动生成格式说明
    format_instructions = parser.get_format_instructions()
    print(f"\nParser自动生成的格式说明:")
    print(format_instructions[:200] + "...")

    prompt = ChatPromptTemplate.from_messages([
        ("human", "{question}\n\n{format_instructions}")
    ])

    chain = prompt | llm | parser

    print("\n结构化输出演示:")
    result = chain.invoke({
        "question": "分析这句话：LangChain是一个强大的AI应用开发框架",
        "format_instructions": format_instructions,
    })

    print(f"  topic: {result.topic}")
    print(f"  confidence: {result.confidence}")
    print(f"  keywords: {result.keywords}")
    print(f"  summary: {result.summary}")

    return parser


# ============================================================
# 7. Tools - 工具定义 (Phase 3深入)
# ============================================================

@tool
def calculator(expression: str) -> str:
    """计算数学表达式

    Args:
        expression: 数学表达式，如 '2 + 3 * 4'
    """
    try:
        # 安全计算（实际生产用ast.literal_eval）
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"


@tool
def get_weather(city: str) -> str:
    """获取城市天气（模拟）

    Args:
        city: 城市名称
    """
    # 模拟天气数据
    weather_data = {
        "北京": "晴，温度18°C",
        "上海": "多云，温度22°C",
        "广州": "雨，温度25°C",
    }
    return weather_data.get(city, f"未找到{city}的天气数据")


def use_tools():
    """演示: Tool定义和基本使用"""
    print("\n" + "=" * 60)
    print("【6. Tools - 工具定义】(Phase 3深入)")
    print("=" * 60)

    print("\n工具定义示例:")
    print(f"  calculator: {calculator.name}")
    print(f"    描述: {calculator.description}")
    print(f"  get_weather: {get_weather.name}")
    print(f"    描述: {get_weather.description}")

    # 直接调用工具
    print("\n直接调用工具:")
    print(f"  calculator('2 + 3 * 4'): {calculator.invoke('2 + 3 * 4')}")
    print(f"  get_weather('北京'): {get_weather.invoke('北京')}")

    print("\n注: Agent自动选择工具调用将在Phase 3实现")

    return [calculator, get_weather]


# ============================================================
# 8. Retrieval - RAG检索 (Phase 2深入)
# ============================================================

def retrieval_mock():
    """演示: RAG概念（Phase 2将完整实现）"""
    print("\n" + "=" * 60)
    print("【7. Retrieval - RAG检索】(Phase 2深入)")
    print("=" * 60)

    print("""
RAG流程概念:
  1. DocumentLoader - 加载文档 (PDF, Markdown, TXT)
  2. TextSplitter - 文档切分 (按长度/语义)
  3. Embeddings - 文本向量化
  4. VectorStore - 向量存储 (ChromaDB/FAISS)
  5. Retriever - 相似度检索

LCEL RAG链:
  retriever | prompt | llm | parser

示例代码结构:
  from langchain_community.document_loaders import TextLoader
  from langchain_text_splitters import RecursiveCharacterTextSplitter
  from langchain_community.embeddings import DashScopeEmbeddings
  from langchain_community.vectorstores import Chroma

  # 加载文档
  loader = TextLoader("docs/readme.md")
  docs = loader.load()

  # 切分
  splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
  chunks = splitter.split_documents(docs)

  # 向量化存储
  vectorstore = Chroma.from_documents(chunks, embeddings)

  # 检索器
  retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

  # RAG链
  rag_chain = (
      {"context": retriever, "question": RunnablePassthrough()}
      | prompt
      | llm
      | parser
  )
""")

    print("\nPhase 2将完整实现此功能")


# ============================================================
# 9. 综合示例 - 整合所有组件
# ============================================================

def component_integrated(llm, memory):
    """演示: 整合所有组件的完整流程"""
    print("\n" + "=" * 60)
    print("【8. 综合示例 - 整合所有组件】")
    print("=" * 60)

    # 完整的对话Agent示例
    system_prompt = """你是一个AI技术助手，具备以下能力：
1. 解释AI相关概念
2. 提供技术建议
3. 记住用户信息

请用简洁专业的语言回答。"""

    full_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    # 完整链
    full_chain = full_prompt | llm | StrOutputParser()

    print("\n多轮对话演示（带Memory）:")

    # 第一轮
    question1 = "LangChain的核心组件有哪些？"
    answer1 = full_chain.invoke({"history": memory.messages, "question": question1})

    print(f"\n[用户]: {question1}")
    print(f"[AI]: {answer1[:1000]}...")

    # 更新Memory
    memory.add_user_message(question1)
    memory.add_ai_message(answer1)

    # 第二轮（带历史）
    question2 = "刚才提到的Memory组件有什么作用？"
    answer2 = full_chain.invoke({"history": memory.messages, "question": question2})

    print(f"\n[用户]: {question2}")
    print(f"[AI]: {answer2[:1000]}...")

    print("\n✅ 综合示例完成！")


# ============================================================
# 主程序
# ============================================================

def main():
    """运行所有演示"""
    print("=" * 60)
    print("LangChain 核心技术综合示例")
    print("=" * 60)
    print("\n涵盖: Models, Prompts, LCEL, Memory, OutputParser, Tools, Retrieval")
    print("建议: 逐个运行demo_xxx()函数理解每个概念\n")

    try:
        # 1. Models
        llm = invoke_models()

        # 2. Prompts
        build_prompts()

        # 3. LCEL
        run_lcel(llm)

        # 4. Memory
        memory = manage_memory(llm)

        # 5. Output Parsers
        run_output_parsers(llm)

        # 6. Tools
        use_tools()

        # 7. Retrieval (概念)
        retrieval_mock()

        # 8. 综合示例
        component_integrated(llm, memory)

        print("\n" + "=" * 60)
        print("🎉 所有演示完成！")
        print("=" * 60)
        print("""
核心原理总结:
  1. LangChain = 可组合的原子组件
  2. LCEL = 组件编排DSL (prompt | llm | parser)
  3. Runnable = 统一接口 (invoke/batch/stream)
  4. Memory = 对话历史管理
  5. Tools = Function Calling封装
  6. Retrieval = RAG检索链

下一步学习:
  - Phase 2: RAG完整实现 (VectorStore, Retriever)
  - Phase 3: Agent Tool Use (ReAct循环)
  - Phase 4: LangGraph工作流编排
""")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("请确保QWEN_API_KEY已正确设置在.env文件中")


if __name__ == "__main__":
    # 1. Models
    llm = invoke_models()

    # 2. Prompts
    build_prompts()