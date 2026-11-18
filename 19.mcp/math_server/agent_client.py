"""LangChain agent that loads tools from the MCP server and uses them.

pip install langchain langchain-mcp-adapters mcp langchain-groq
export GROQ_API_KEY=...
python agent_client.py
"""
import asyncio

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    # 1. Tell the client how to reach each MCP server
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server.py"],  # use an absolute path if run elsewhere
                "transport": "stdio",
            },
            # Example of a remote server over HTTP:
            # "weather": {"url": "http://localhost:8000/mcp", "transport": "streamable_http"},
        }
    )

    # 2. MCP tools -> LangChain tools
    tools = await client.get_tools()
    print("Loaded tools:", [t.name for t in tools])

    # 3. Plug them into an agent using a Groq-hosted model (reads GROQ_API_KEY)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    agent = create_agent(llm, tools)

    # 4. Ask something that needs the tools
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is (3 + 5) x 12?"}]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
