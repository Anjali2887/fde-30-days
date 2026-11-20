"""Chapter 2: turn text into vectors and compare meanings.  Run: python embed_basics.py"""
import math

import requests

from llm_config import EMBED_MODEL, OPTIONS

EMBED_URL = "http://localhost:11434/api/embed"


def embed(texts: list[str]) -> list[list[float]]:
    """Send a list of texts, get back one vector (list of floats) per text."""
    resp = requests.post(
        EMBED_URL,
        json={"model": EMBED_MODEL, "input": texts, "options": OPTIONS},
        timeout=300,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return data["embeddings"]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """1.0 = same direction (same meaning), 0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)



if __name__ == "__main__":
    sentences = [
        # Pair 1: River bank
        "search_query: I sat on the bank of the river.",
        "search_document: The river bank was covered with grass.",

        # Pair 2: Fixed deposit
        "search_query: What is the interest rate on a fixed deposit?",
        "search_document: The interest rate on a fixed deposit is 7%."
    ]

    vectors = embed(sentences)

    print(f"Each sentence became {len(vectors[0])} numbers.")

    print(
        "River bank similarity:",
        round(cosine_similarity(vectors[0], vectors[1]), 3)
    )

    print(
        "Fixed deposit similarity:",
        round(cosine_similarity(vectors[2], vectors[3]), 3)
    )
