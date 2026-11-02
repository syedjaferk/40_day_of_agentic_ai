"""Indexing, the quiet half of RAG: embed every note once and keep the vectors."""

from corpus import DOCS
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def build_store():
    store = InMemoryVectorStore(embeddings)
    store.add_documents(DOCS)
    return store


if __name__ == "__main__":
    store = build_store()
    question = "How many days do I have to cancel and get my money back?"
    for doc, score in store.similarity_search_with_score(question, k=3):
        print(f"{score:.3f}  [{doc.metadata['source']}]  {doc.page_content[:60]}...")
