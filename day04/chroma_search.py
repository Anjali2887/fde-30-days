"""Chapter 2: the same search with a real vector database (Chroma).
Setup once:  python -m pip install chromadb      Run: python chroma_search.py
"""
import chromadb

from embed_basics import embed
from semantic_search import POLICIES

CATEGORIES = ["cards", "payments", "deposits", "kyc", "loans", "cards", "kyc", "payments", "cards", "payments"]
RISKS = [
    "high", "low", "low", "high", "low",
    "high", "high", "low", "high", "high"
]

client = chromadb.PersistentClient(path="./chroma_db")  # saved to disk, survives restarts
collection = client.get_or_create_collection(
    name="bank_policies",
    embedding_function=None,  # we pass our own Ollama vectors
    configuration={"hnsw": {"space": "cosine"}},  # compare by cosine similarity
)

if collection.count() == 0:
    collection.add(
        ids=[f"policy-{i}" for i in range(len(POLICIES))],
        documents=POLICIES,
        embeddings=embed(POLICIES),
        metadatas=[
    {"category": c, "risk": r}
    for c, r in zip(CATEGORIES, RISKS)
],
    )

query = "someone used my card without permission, how fast must I tell the bank?"
query_vec = embed([query])[0]

print("Top 3, all categories:")
res = collection.query(query_embeddings=[query_vec], n_results=3)
for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(f"  distance {dist:.3f} | {doc[:70]}")

print("\nTop 5, only high-risk policies (metadata filter):")
res = collection.query(
    query_embeddings=[query_vec],
    n_results=5,
    where={"risk": "high"}
)
for doc, metadata in zip(
    res["documents"][0],
    res["metadatas"][0]
):
    print(
        f"  Risk: {metadata['risk']} | "
        f"Category: {metadata['category']} | "
        f"{doc[:70]}"
    )
