# Day 04 — Embeddings and Semantic Search

## Overview

This project explores how text can be converted into numerical vectors (embeddings) and how these vectors can be used to find information based on meaning.

The project covers:

- Generating text embeddings using Ollama and `nomic-embed-text`.
- Calculating cosine similarity between text embeddings.
- Understanding Keyword Search vs Semantic Search.
- Implementing semantic search using ChromaDB.
- Using metadata filters to retrieve specific documents.
- Comparing search results for exact values and natural-language queries.

## Project Files

| File | Description |
|---|---|
| `embed_basics.py` | Converts sentences into embeddings and calculates cosine similarity. |
| `semantic_search.py` | Demonstrates semantic search using text meaning rather than exact keyword matching. |
| `chroma_search.py` | Implements vector search using ChromaDB, including metadata filtering. |
| `llm_config.py` | Contains Ollama embedding model and configuration settings. |

## Technologies Used

- Python
- Ollama
- nomic-embed-text
- ChromaDB
- Requests
- Vector Embeddings
- Cosine Similarity

## How to Run

### Prerequisites

1. Python installed.
2. Git installed.
3. Ollama installed and running.
4. Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

### Option 1: Windows

Open PowerShell and navigate to the project directory:

```powershell
cd C:\Users\dell\fde-30-days\day04
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install requests chromadb
```

Run the scripts:

```powershell
python embed_basics.py
python semantic_search.py
python chroma_search.py
```

**Note:** On some Windows environments, enterprise application-control policies may block ChromaDB dependencies. WSL is an alternative if this happens.

### Option 2: WSL (Ubuntu)

Start Ubuntu and navigate to the project directory:

```bash
cd /mnt/c/Users/dell/fde-30-days/day04
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Check Ollama connectivity:

```bash
curl http://localhost:11434/api/tags
```

Ensure Ollama is running on Windows and accessible from WSL. The WSL configuration used for this setup is:

Windows file: `%UserProfile%\.wslconfig`

```ini
[wsl2]
networkingMode=mirrored
```

After saving the configuration, run this in PowerShell:

```powershell
wsl --shutdown
```

If Ollama needs to be exposed to WSL, start its server from Windows PowerShell with:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
ollama serve
```

Keep the Ollama server terminal running.

Run the Python scripts from Ubuntu:

```bash
python embed_basics.py
python semantic_search.py
python chroma_search.py
```

## Lab 3 — Keyword Search vs Semantic Search

The objective was to compare exact keyword matching with meaning-based search using three banking-related queries.

| Query | Keyword Search — Rank 1 | Semantic Search — Rank 1 |
|---|---|---|
| Someone took money from my account without asking me. How quickly should I inform the bank? | Unrelated document | Unauthorised card transactions policy |
| I sent money electronically, but it did not reach the receiver. When will I get it back? | Unrelated document | NEFT policy |
| I need my deposited money back before the agreed end date. Will I lose anything? | FD premature closure policy | FD premature closure policy |

### Lab 3 Observations

- Keyword Search works well when the query contains exact words or identifiers.
- Semantic Search understands the intent and meaning of natural-language queries.
- Semantic Search retrieved the correct policies for the unauthorised transaction and NEFT queries.
- Both approaches retrieved the correct fixed deposit policy for the third query.
- Combining Keyword Search and Semantic Search through Hybrid Search can improve retrieval.

## Key Learnings

1. Embeddings convert text into fixed-length numerical vectors.
2. Cosine similarity measures the similarity between vectors.
3. Documents and queries should use the same embedding model.
4. Chunking large documents improves retrieval precision.
5. Chunk overlap helps preserve context between chunks.
6. Metadata filtering helps restrict results based on category, risk, and access permissions.
7. ANN search trades some exactness for faster retrieval.
8. Changing an embedding model requires re-embedding documents and rebuilding the vector index.
9. Hybrid Search combines keyword and semantic retrieval.

## Conclusion

Day 04 provided hands-on experience with embeddings, cosine similarity, semantic search, ChromaDB, and metadata filtering.

These concepts form the foundation for building Retrieval-Augmented Generation (RAG) applications.
