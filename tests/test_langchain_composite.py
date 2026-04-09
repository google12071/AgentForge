"""
LangChain 综合示例单元测试
测试 examples/langchain_composite.py 中的核心函数

运行方式:
  pytest tests/test_langchain_composite.py -v
  pytest tests/test_langchain_composite.py -v -k "test_tools"  # 只测试工具
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

# 加载环境变量
load_dotenv()

# 导入被测试的模块
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.langchain_composite import (
    invoke_models,
    build_prompts,
    run_lcel,
    manage_memory,
    run_output_parsers,
    calculator,
    get_weather,
    use_tools,
    component_integrated,
    MODEL_NAME,
)


# ============================================================
# 配置和Fixtures
# ============================================================

@pytest.fixture(scope="module")
def llm():
    """创建LLM实例供测试使用"""
    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        pytest.skip("QWEN_API_KEY not set in .env")

    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0.7,
        max_tokens=100,
    )


@pytest.fixture
def memory():
    """创建Memory实例"""
    history = ChatMessageHistory()
    history.add_user_message("测试用户消息")
    history.add_ai_message("测试AI回复")
    return history


# ============================================================
# 1. Models 测试
# ============================================================

class TestModels:
    """测试 LLM Models 相关功能"""

    def test_llm_initialization(self, llm):
        """测试LLM正确初始化"""
        assert llm.model_name == MODEL_NAME
        assert llm.temperature == 0.7
        assert llm.max_tokens == 100

    def test_llm_invoke(self, llm):
        """测试LLM基本调用"""
        response = llm.invoke("你好")
        assert response is not None
        assert hasattr(response, 'content')
        assert len(response.content) > 0

    def test_llm_batch(self, llm):
        """测试LLM批量调用"""
        responses = llm.batch(["问题1", "问题2"])
        assert len(responses) == 2
        for r in responses:
            assert hasattr(r, 'content')

    @pytest.mark.asyncio
    async def test_llm_async_invoke(self, llm):
        """测试LLM异步调用"""
        response = await llm.ainvoke("你好")
        assert response is not None
        assert hasattr(response, 'content')


# ============================================================
# 2. Prompts 测试
# ============================================================

class TestPrompts:
    """测试 Prompt 模板功能"""

    def test_simple_prompt_template(self):
        """测试简单PromptTemplate"""
        template = PromptTemplate.from_template(
            "请用{style}的风格，解释{concept}"
        )
        prompt = template.format(style="幽默", concept="AI")

        assert "幽默" in prompt
        assert "AI" in prompt
        # input_variables的顺序可能不同，使用集合比较
        assert set(template.input_variables) == {"style", "concept"}

    def test_chat_prompt_template(self):
        """测试ChatPromptTemplate"""
        chat_template = ChatPromptTemplate.from_messages([
            ("system", "你是{role}"),
            ("human", "{question}"),
        ])
        messages = chat_template.format_messages(
            role="助手",
            question="你好"
        )

        assert len(messages) == 2
        assert messages[0].type == "system"
        assert messages[1].type == "human"

    def test_build_prompts_function(self):
        """测试build_prompts函数"""
        # 该函数返回ChatPromptTemplate
        result = build_prompts()
        assert result is not None
        assert isinstance(result, ChatPromptTemplate)


# ============================================================
# 3. LCEL 测试
# ============================================================

class TestLCEL:
    """测试 LCEL 链式编排"""

    def test_simple_chain(self, llm):
        """测试简单链 prompt | llm | parser"""
        prompt = ChatPromptTemplate.from_messages([
            ("human", "{question}")
        ])
        parser = StrOutputParser()

        chain = prompt | llm | parser

        result = chain.invoke({"question": "说一个字"})
        assert isinstance(result, str)
        assert len(result) > 0

    def test_runnable_passthrough(self, llm):
        """测试RunnablePassthrough"""
        from langchain_core.runnables import RunnablePassthrough

        prompt = ChatPromptTemplate.from_messages([
            ("human", "{question}")
        ])

        chain = RunnablePassthrough.assign(
            extra=lambda x: {"added": "value"}
        ) | prompt | llm | StrOutputParser()

        result = chain.invoke({"question": "测试"})
        assert isinstance(result, str)

    def test_runnable_parallel(self, llm):
        """测试RunnableParallel"""
        from langchain_core.runnables import RunnableParallel, RunnableLambda

        prompt = ChatPromptTemplate.from_messages([
            ("human", "{question}")
        ])

        parallel_chain = RunnableParallel(
            answer=prompt | llm | StrOutputParser(),
            length=RunnableLambda(lambda x: len(x["question"])),
        )

        result = parallel_chain.invoke({"question": "测试问题"})
        assert "answer" in result
        assert "length" in result
        assert result["length"] == 4

    def test_run_lcel_function(self, llm):
        """测试run_lcel函数"""
        chain = run_lcel(llm)
        assert chain is not None


# ============================================================
# 4. Memory 测试
# ============================================================

class TestMemory:
    """测试 Memory 对话历史管理"""

    def test_chat_message_history(self):
        """测试ChatMessageHistory基本功能"""
        history = ChatMessageHistory()

        history.add_user_message("用户问题")
        history.add_ai_message("AI回复")

        assert len(history.messages) == 2
        assert history.messages[0].type == "human"
        assert history.messages[1].type == "ai"

    def test_memory_window(self):
        """测试滑动窗口功能"""
        history = ChatMessageHistory()

        # 添加多轮对话
        for i in range(5):
            history.add_user_message(f"问题{i}")
            history.add_ai_message(f"回答{i}")

        # 模拟滑动窗口，只取最近2轮
        k = 2
        recent_messages = history.messages[-(k * 2):]

        assert len(recent_messages) == 4
        assert "问题3" in recent_messages[0].content

    def test_manage_memory_function(self, llm):
        """测试manage_memory函数"""
        memory = manage_memory(llm)
        assert memory is not None
        assert isinstance(memory, ChatMessageHistory)

    def test_memory_with_chain(self, llm, memory):
        """测试Memory与链结合"""
        from langchain_core.prompts import MessagesPlaceholder

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        chain = prompt | llm | StrOutputParser()

        result = chain.invoke({
            "history": memory.messages,
            "question": "继续对话"
        })

        assert isinstance(result, str)
        assert len(result) > 0


# ============================================================
# 5. Output Parsers 测试
# ============================================================

class TestOutputParsers:
    """测试 Output Parser 结构化输出"""

    def test_str_output_parser(self, llm):
        """测试StrOutputParser"""
        prompt = ChatPromptTemplate.from_messages([
            ("human", "{question}")
        ])
        parser = StrOutputParser()

        chain = prompt | llm | parser
        result = chain.invoke({"question": "回复一个词"})

        assert isinstance(result, str)

    def test_run_output_parsers_function(self, llm):
        """测试run_output_parsers函数"""
        parser = run_output_parsers(llm)
        assert parser is not None


# ============================================================
# 6. Tools 测试
# ============================================================

class TestTools:
    """测试 Tools 工具定义"""

    def test_calculator_tool(self):
        """测试calculator工具"""
        # @tool装饰后的工具需要用invoke调用
        result = calculator.invoke("2 + 3 * 4")
        assert "计算结果" in result
        assert "14" in result

        # 另一个表达式
        result = calculator.invoke("10 - 5")
        assert "计算结果" in result
        assert "5" in result

    def test_calculator_error_handling(self):
        """测试calculator错误处理"""
        # 无效表达式
        result = calculator.invoke("invalid expression")
        assert "计算错误" in result or "Error" in result or "错误" in result

    def test_get_weather_tool(self):
        """测试get_weather工具"""
        # 已知城市
        result = get_weather.invoke("北京")
        assert "晴" in result or "18" in result

        result = get_weather.invoke("上海")
        assert "多云" in result or "22" in result

    def test_get_weather_unknown_city(self):
        """测试get_weather未知城市"""
        result = get_weather.invoke("未知城市XYZ")
        assert "未找到" in result

    def test_use_tools_function(self):
        """测试use_tools函数"""
        tools = use_tools()
        assert tools is not None
        assert len(tools) == 2
        assert tools[0].name == "calculator"
        assert tools[1].name == "get_weather"

    def test_tool_decorator(self):
        """测试@tool装饰器"""
        from langchain_core.tools import tool

        @tool
        def sample_tool(input: str) -> str:
            """示例工具"""
            return f"处理: {input}"

        assert sample_tool.name == "sample_tool"
        assert "示例工具" in sample_tool.description


# ============================================================
# 7. Integrated 测试
# ============================================================

class TestIntegrated:
    """测试综合示例"""

    def test_component_integrated(self, llm, memory):
        """测试component_integrated函数"""
        # 该函数主要是演示，测试其不报错
        component_integrated(llm, memory)

    def test_full_conversation_flow(self, llm):
        """测试完整对话流程"""
        from langchain_core.prompts import MessagesPlaceholder

        # 1. 创建Memory
        history = ChatMessageHistory()
        history.add_user_message("我叫测试用户")
        history.add_ai_message("你好测试用户！")

        # 2. 创建Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是AI助手"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        # 3. 创建Chain
        chain = prompt | llm | StrOutputParser()

        # 4. 第一轮对话
        result1 = chain.invoke({
            "history": history.messages,
            "question": "我是谁？"
        })
        assert isinstance(result1, str)

        # 5. 更新Memory
        history.add_user_message("我是谁？")
        history.add_ai_message(result1)

        # 6. 第二轮对话（带历史）
        result2 = chain.invoke({
            "history": history.messages,
            "question": "继续"
        })
        assert isinstance(result2, str)


# ============================================================
# 8. Mock测试（不依赖真实API）
# ============================================================

class TestWithMock:
    """使用Mock进行测试，不依赖真实API"""

    def test_llm_invoke_mock(self):
        """Mock测试LLM调用"""
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "模拟回复"
        mock_llm.invoke.return_value = mock_response

        result = mock_llm.invoke("测试问题")

        assert result.content == "模拟回复"
        mock_llm.invoke.assert_called_once()

    def test_chain_mock(self):
        """Mock测试链调用"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="回复")

        # 模拟链式调用
        prompt = ChatPromptTemplate.from_messages([
            ("human", "{question}")
        ])

        # 使用真实prompt，mock LLM
        messages = prompt.format_messages(question="测试")
        assert len(messages) == 1


# ============================================================
# 运行配置
# ============================================================