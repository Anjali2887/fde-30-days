"""Chapter 2: semantic search vs keyword search over bank policy snippets.  Run: python semantic_search.py"""
from embed_basics import cosine_similarity, embed

# Practice snippets written for this course (not real bank policy).
POLICIES = [
    "Customers must report unauthorised card transactions within 3 working days to get full liability protection.",
    "NEFT transfers are processed in half-hourly batches; failed transfers are credited back within 2 hours.",
    "A fixed deposit can be closed before maturity, but a penalty of 1% on the interest rate applies.",
    "KYC documents must be updated every 2 years for high-risk accounts and every 10 years for low-risk ones.",
    "Home loan customers may prepay any amount at any time without a prepayment charge on floating rates.",
    "Debit card daily withdrawal limit at ATMs is Rs 50,000; it can be changed in the mobile app.",
    "Dormant accounts with no customer-initiated transaction for 2 years are frozen until KYC is refreshed.",
    "Cheque deposits made after 3 PM are sent for clearing on the next working day.",
    "Credit card disputes are acknowledged within 24 hours and resolved within 30 days.",
    "UPI transaction limit is Rs 1 lakh per day per account for most payee types.",
]


def keyword_search(query: str, docs: list[str], k: int = 3) -> list[tuple[int, str]]:
    """Old-style search: counts shared words. Misses synonyms."""
    q_words = set(query.lower().split())
    scored = [(len(q_words & set(d.lower().split())), d) for d in docs]
    return sorted(scored, key=lambda s: s[0], reverse=True)[:k]


def semantic_search(query: str, docs: list[str], doc_vectors: list[list[float]], k: int = 3) -> list[tuple[float, str]]:
    """Meaning-based search: compares vectors."""
    q_vec = embed([query])[0]
    scored = [(cosine_similarity(q_vec, v), d) for v, d in zip(doc_vectors, docs)]
    return sorted(scored, key=lambda s: s[0], reverse=True)[:k]


if __name__ == "__main__":
    doc_vectors = embed(POLICIES)  # embed all documents once, like building an index
    query = "Rs 50,000"

    print("KEYWORD search:")
    for score, doc in keyword_search(query, POLICIES):
        print(f"  {score} words | {doc[:70]}")

    print("\nSEMANTIC search:")
    for score, doc in semantic_search(query, POLICIES, doc_vectors):
        print(f"  {score:.3f} | {doc[:70]}")
