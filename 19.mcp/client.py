import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_rag_client(user_query: str):
    # Configure connection parameters for the MCP RAG server process
    server_params = StdioServerParameters(command="python", args=["rag_server.py"])

    # Establish the stdio transport and client session
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Negotiate capabilities with the server
            await session.initialize()

            # 1. Fetch relevant knowledge chunks from the MCP tool
            tool_response = await session.call_tool(
                "retrieve_context", arguments={"query": user_query}
            )
            retrieved_context = tool_response.content[0].text

            # 2. Build the RAG augmented prompt
            augmented_prompt = (
                f"Use the following context to answer the user's question:\n\n"
                f"--- CONTEXT ---\n{retrieved_context}\n---------------\n\n"
                f"Question: {user_query}\n"
                f"Answer:"
            )

            # 3. Forward the augmented prompt to your preferred LLM provider
            # response = openai_client.chat.completions.create(...)
            print(augmented_prompt)


if __name__ == "__main__":
    asyncio.run(run_rag_client("Tell me about FastMCP"))
