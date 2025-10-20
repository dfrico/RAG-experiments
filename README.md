# RAG-experiments
Experiments with RAG + vector DBs.

## Dev
```bash
python -m venv .venv
pip install -r requirements.txt
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

