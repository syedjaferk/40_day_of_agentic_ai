import asyncio

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        groq_api_key="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",
    )

    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["./local_mcp.py"],
            },
            "search": {
                "transport": "http",
                "url": "https://mcp.tavily.com/mcp/?tavilyApiKey=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",
            },
        }
    )

    tools = await client.get_tools()

    for tool in tools:
        print("Tool:", tool)
        input()

    agent = create_agent(
        llm,
        tools,
        system_prompt="""
            You are a helpful AI assistant.

            When a math calculation is required:
            - ALWAYS use the appropriate tool.
            - Do NOT write the answer yourself.
            """,
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Do a summation of 2, 4 and 3"}]}
    )

    search_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Give me details on Iran News"}]}
    )

    print("Math Response:", math_response)
    print("Search Response:", search_response)


if __name__ == "__main__":
    asyncio.run(main())
