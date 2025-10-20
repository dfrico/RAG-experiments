# Local RAG

1. Fetch wikipedia pages using their API
2. ingest those .txts into LanceDB (built-in similarity search (key) and indexing)
3. retrieval and LLM querying using mistral via ollama and a retrieval-augmented QA chain using langchain.

## TODOs:

- [ ] Add txt chunking. Current implementation makes retrieval granularity too coarse
- [ ] Use a better embedding model (`bge-base-en-v1.5`? `instructor-large`? `e5-large-v2`?)

## Dev

```bash
python -m venv .venv
pip install -r requirements.txt
```

Or using conda:

```bash
conda create -n rag python=3.13 pip
conda activate rag
conda install --file requirements.txt
```

Needs ollama with Mistral.

```bash
ollama pull mistral
sudo systemctl enable ollama
sudo systemctl start ollama
```

## Usage

```bash
python fetch_wiki.py
python ingest.py
python query_wiki.py
```
