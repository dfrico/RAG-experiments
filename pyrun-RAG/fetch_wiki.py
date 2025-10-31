import os
import re
import s3fs
from wikipediaapi import Wikipedia

TOPICS = [
    "Retrieval-augmented generation",
    "Large language model",
    "Vector database",
    "LangChain",
    "LlamaIndex",
    "Embeddings (machine learning)",
    "Transformer (machine learning model)",
    "Natural language processing",
    "Semantic search",
    "OpenAI",
    "Knowledge graph",
    "Neural network",
    "Deep learning",
    "Artificial intelligence"
]

Wiki = Wikipedia(
    language="en",
    user_agent="MiniWikiRAG/0.1 (https://example.com; contact: you@example.com)",
)

S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_PREFIX = "data/wiki_pages"
fs = s3fs.S3FileSystem()

def sanitize(name: str) -> str:
    """Make a safe filename from a page title."""
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_")

def s3_key_for_title(title: str) -> str:
    return f"{S3_PREFIX}/{sanitize(title)}.txt"

for title in TOPICS:
    try:
        page = Wiki.page(title)
        if not page.exists():
            print(f"Page not found: {title}")
            continue

        text = page.text

        key = s3_key_for_title(title)
        with fs.open(f"s3://{S3_BUCKET}/{key}", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: s3://{S3_BUCKET}/{key}")
    except Exception as e:
        print("Skip:", title, "->", e)
