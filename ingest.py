from langchain_community.vectorstores import LanceDB
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
import lancedb

loader = DirectoryLoader("data/wiki_pages", glob="*.txt", loader_cls=TextLoader)
docs = loader.load()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
conn = lancedb.connect("./lancedb")
db = LanceDB.from_documents(docs, embeddings, connection=conn, table_name="wiki_vectors")

print("✅ Indexed", len(docs), "documents into LanceDB.")
