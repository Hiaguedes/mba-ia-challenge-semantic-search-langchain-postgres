# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

MBA challenge: PDF ingestion + semantic search CLI. Pipeline: load PDF → chunk → embed → store in pgVector → CLI retrieves top-10 chunks → LLM answers only from context.

Supports OpenAI or Gemini (whichever API key is set in `.env`).

## Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then fill in API key

# Run
docker compose up -d        # start postgres+pgvector
python src/ingest.py        # ingest document.pdf (run once)
python src/chat.py          # start CLI chat
```

## Architecture

```
chat.py  →  search.py::search_prompt()  →  PGVector.similarity_search_with_score(k=10)  →  LLM
ingest.py  →  PyPDFLoader  →  RecursiveCharacterTextSplitter(1000, 150)  →  PGVector.add_documents()
config.py  →  shared env loading + get_embeddings() + get_llm()
```

**Provider selection** (in `config.py`): checks `OPENAI_API_KEY` first, falls back to `GOOGLE_API_KEY`. Same logic in both embeddings and LLM.

**`search_prompt(question=None)`** — called with no args from `chat.py` to return a reusable `ask(q) → str` callable. Called with a question to return the answer directly.

## Key Constraints

- Chunks: 1000 chars, 150 overlap — do not change
- Retrieval: `k=10` — do not change
- LLM must answer **only from retrieved context** — `PROMPT_TEMPLATE` in `search.py` enforces this
- Out-of-context response must be: `"Não tenho informações necessárias para responder sua pergunta."`

## Environment Variables

| Variable | Default |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME` | `documents` |
| `PDF_PATH` | `document.pdf` |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` |
| `OPENAI_LLM_MODEL` | `gpt-4o-mini` |
| `GOOGLE_EMBEDDING_MODEL` | `models/embedding-001` |
| `GOOGLE_LLM_MODEL` | `gemini-2.0-flash-lite` |

## Stack

- `langchain-postgres` (`PGVector`) — vector store
- `langchain-openai` / `langchain-google-genai` — embeddings + LLM
- `psycopg` v3 — DB driver (use `postgresql+psycopg://` not `psycopg2` in `DATABASE_URL`)
- Docker image: `pgvector/pgvector:pg17` — pgvector extension bootstrapped automatically by `bootstrap_vector_ext` service
