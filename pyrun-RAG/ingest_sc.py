from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import lancedb
import s3fs
import os

load_dotenv()
BUCKET = os.getenv('S3_BUCKET_NAME')
PREFIX = "data/wiki_pages/"

fs = s3fs.S3FileSystem()

def list_txt_uris(bucket: str, prefix: str):
    if not prefix.endswith("/"):
        prefix += "/"
    items = fs.ls(f"s3://{bucket}/{prefix}")  # returns keys without scheme
    uris = [(p if p.startswith("s3://") else f"s3://{p}") for p in items]
    return [u for u in uris if u.lower().endswith(".txt")]

raw_docs = []
for uri in list_txt_uris(BUCKET, PREFIX):
    with fs.open(uri, "r", encoding="utf-8") as f:
        raw_docs.append(Document(page_content=f.read(), metadata={"source": uri}))

print(f"Loaded {len(raw_docs)} files from s3://{BUCKET}/{PREFIX}")

# basic, sane defaults for prose
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
docs = splitter.split_documents(raw_docs)

emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Local dev: path DB; on AWS switch this to 's3://your-bucket/lancedb'
conn = lancedb.connect(f"s3://{BUCKET}/lancedb")
# Use create once, then .add() for incremental ingestion:
vs = LanceDB.from_documents(docs[:1], emb, connection=conn, table_name="wiki_vectors")  # bootstrap
vs.add_documents(docs[1:])
print(f"Indexed {len(docs)} chunks into LanceDB.")
