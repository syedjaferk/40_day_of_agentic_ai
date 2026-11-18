from mcp.server.fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("RAG-Provider")

# Vector Database placeholder (e.g., ChromaDB, Pinecone, FAISS)
DOCUMENTS = [
    "Model Context Protocol (MCP) standardizes context sharing between LLMs and data sources.",
    "RAG enhances LLM prompts using vector database semantic search.",
    "FastMCP allows rapid development of Python-based MCP servers."
]

@mcp.tool()
def retrieve_context(query: str) -> str:
    """Retrieves relevant document snippets from the knowledge base for RAG."""
    # Replace this block with your actual vector DB query: embeddings.search(query)
    results = [doc for doc in DOCUMENTS if any(term.lower() in doc.lower() for term in query.split())]

    if not results:
        return "No relevant context found."

    return "\n".join(f"- {doc}" for doc in results)

if __name__ == "__main__":
    mcp.run()
