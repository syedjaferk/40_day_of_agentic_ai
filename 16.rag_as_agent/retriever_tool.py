"""Wrap the retriever as a TOOL. The model decides when to search, and what to search for."""

from build_index import build_store
from langchain_core.tools import tool

store = build_store()


@tool(response_format="content_and_artifact")
def search_handbook(query: str):
    """Search the academy handbook. Use it for any question about fees, refunds, classes,
    certificates, mentoring, placement or portal errors. Pass a short, specific search query."""
    docs = store.similarity_search(query, k=3)
    text = "\n\n".join(f"[{d.metadata['source']}] {d.page_content}" for d in docs)
    return (
        text,
        docs,
    )  # text goes to the model; the Document objects ride along as an artifact


if __name__ == "__main__":
    print(search_handbook.name, "->", search_handbook.args)
    print(search_handbook.invoke({"query": "refund deadline"}))
