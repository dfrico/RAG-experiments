# Pyrun-lithops RAG

1. Install ollama

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

2. Fetch wiki pages and store them in S3 (`python fetch_wiki.py`).

3. Build the index **once** (ingest the documents into lanceDB).

```bash
python ingest.py \
  --input-prefix s3://my-bucket/wiki_pages/ \
  --lancedb-uri s3://my-bucket/lancedb \
  --table-name wiki_vectors
```

TODO: right now on ... I get an OOM error (`Exception: MemoryError - Function exceeded maximum memory and was killed`) :(

Optionally for a faster run (not parallelized), run `python ingest.py` instead.

4. Run the parallel multi-query retriever (needs ollama - `ollama serve`)

```bash
python query_wiki.py \
  --lancedb-uri s3://my-bucket/lancedb \
  --table-name wiki_vectors \
  --llm-model mistral \
  --paraphrases 3 --k 5 --per-query-k 8
```
