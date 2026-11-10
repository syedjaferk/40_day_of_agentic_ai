import os

from dotenv import load_dotenv
from groq import Groq
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chroma = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma.get_or_create_collection(
    "documents"
)


history = """
User: Explain FastAPI.

Assistant:
FastAPI is a modern Python web framework.
"""

user_query = "How do I deploy it?"

rewrite_prompt = f"""
You are an expert search query optimizer.

Conversation

{history}

Current Query

{user_query}

Rewrite the query into a standalone search query.

Return only the rewritten query.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": rewrite_prompt
        }
    ],
    temperature=0
)

transformed_query = response.choices[0].message.content.strip()

print("=" * 60)
print("Transformed Query")
print(transformed_query)

expand_prompt = f"""
Generate 5 different search queries for

{transformed_query}

Return one query per line.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": expand_prompt
        }
    ],
    temperature=0.3
)

expanded_queries = [
    line.strip("-•1234567890. ")
    for line in response.choices[0].message.content.split("\n")
    if line.strip()
]

expanded_queries.insert(0, transformed_query)

print("=" * 60)
print("Expanded Queries")

for q in expanded_queries:
    print(q)

retrieved_documents = {}

for query in expanded_queries:

    embedding = embedding_model.encode(query).tolist()

    result = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    for doc in result["documents"][0]:
        retrieved_documents[doc] = True

documents = list(retrieved_documents.keys())

print("=" * 60)
print("Retrieved Documents")

for doc in documents:
    print(doc)

context = "\n".join(documents)

final_prompt = f"""
Answer ONLY using the following context.

Context

{context}

Question

{user_query}
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": final_prompt
        }
    ],
    temperature=0
)

print("=" * 60)
print("Final Answer")
print(response.choices[0].message.content)
