from langchain_community.vectorstores import LanceDB
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import lancedb

DB_PATH = "./lancedb"
TABLE_NAME = "wiki_vectors"
MODEL = "mistral"

# Connect to LanceDB
conn = lancedb.connect(DB_PATH)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = LanceDB(connection=conn, table_name=TABLE_NAME, embedding=embeddings)
llm = Ollama(model=MODEL)

# Create retriever + QA chain
retriever = db.as_retriever(search_kwargs={"k": 5})
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

while True:
    q = input("\nAsk a question (or 'exit'): ")
    if q.strip().lower() in {"exit", "quit"}:
        break
    answer = qa_chain.run(q)
    print("\n--- Answer ---")
    print(answer)
    print("--------------")
