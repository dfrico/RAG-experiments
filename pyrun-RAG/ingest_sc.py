# ingest.py
from langchain_community.vectorstores import LanceDB
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import lancedb
import os

load_dotenv()
LOADER = DirectoryLoader("data/wiki_pages", glob="*.txt", loader_cls=TextLoader)
raw_docs = LOADER.load()
bucket_name = os.getenv('S3_BUCKET_NAME')

# basic, sane defaults for prose
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
docs = splitter.split_documents(raw_docs)

emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Local dev: path DB; on AWS switch this to 's3://your-bucket/lancedb'
conn = lancedb.connect(f"s3://{bucket_name}/lancedb")
# Use create once, then .add() for incremental ingestion:
vs = LanceDB.from_documents(docs[:1], emb, connection=conn, table_name="wiki_vectors")  # bootstrap
vs.add_documents(docs[1:])
print(f"Indexed {len(docs)} chunks into LanceDB.")
