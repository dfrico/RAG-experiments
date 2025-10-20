import re
from pathlib import Path
from wikipediaapi import Wikipedia

# ---- CONFIG ----
OUT = Path("data/wiki_pages")
OUT.mkdir(parents=True, exist_ok=True)
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
# ----------------


# identify your app politely for Wikipedia API policy
WIKI = Wikipedia(
    language="en",
    user_agent="MiniWikiRAG/0.1 (https://example.com; contact: you@example.com)",
)
# ----------------


def sanitize(name: str) -> str:
    """Make a safe filename from a page title."""
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_")


for title in TOPICS:
    try:
        page = WIKI.page(title)
        if not page.exists():
            print(f"⚠️  Page not found: {title}")
            continue

        text = page.text
        (OUT / f"{sanitize(title)}.txt").write_text(text, encoding="utf-8")
        print("✅ Saved:", title)
    except Exception as e:
        print("⚠️  Skip:", title, "->", e)
