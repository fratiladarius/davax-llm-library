# davax-llm-library

a tiny book recommender.  
embeddings + chromadb retrieval.  
llm picks the single best match.  
returns: Title / Why / Summary.

## quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
```

install dependencies manually **or** create your own `requirements.txt`:

```bash
pip install openai chromadb python-dotenv tqdm
```

## features

- ingest JSON book summaries  
- chromadb persistent store (cosine)  
- openai embeddings + chat  
- tool call: fetch full summary by title  
- shortlist formatter, llm reranking  
- optional offensive-language guard  

create a `.env` file:

```
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small
```

## usage

- ask: `books about memory & freedom`  
- bot prints shortlist (by vector similarity)  
- bot returns 3 lines:  
  - `Title: …`    
  - `Why: …`  
  - `Summary: …` (from local data)

## commands cheat sheet

```bash
# ingest books
python3 -m scripts.ingest

# query manually
python3 -m scripts.query "books about memory"

# chatbot interface
python3 -m services.chatbot
```

## data format

`data/book_summaries.json`:

```json
[
  {
    "title": "1984",
    "themes": ["freedom vs control", "surveillance", "truth"],
    "short_summary": "A dystopia where Big Brother controls truth.",
    "long_summary": "Orwell's vision of a totalitarian regime..."
  }
]
```
