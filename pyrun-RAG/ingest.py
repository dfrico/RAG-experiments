# embed_fanout.py
import itertools, s3fs, lithops, lancedb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

def run_ingest(input_prefix: str, lancedb_uri: str, table_name: str,
               model: str = "all-MiniLM-L6-v2") -> dict:
    fs = s3fs.S3FileSystem()
    inputs = [f"s3://{p}" for p in fs.ls(input_prefix) if p.endswith(".txt")]

    def embed_file(s3_uri):
        with fs.open(s3_uri, "rb") as f:
            text = f.read().decode("utf-8")
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        docs = splitter.create_documents([text], metadatas=[{"source": s3_uri}])
        emb = HuggingFaceEmbeddings(model_name=model)
        vecs = emb.embed_documents([d.page_content for d in docs])
        # Keep schema compatible with LangChain's LanceDB wrapper:
        return [{"vector": v, "text": d.page_content, "metadata": d.metadata}
                for v, d in zip(vecs, docs)]

    fexec = lithops.FunctionExecutor()
    fexec.map(embed_file, inputs)
    batches = fexec.get_result()

    conn = lancedb.connect(lancedb_uri)
    tbl = (conn.open_table(table_name)
           if table_name in conn.table_names()
           else conn.create_table(table_name, data=None))
    records = list(itertools.chain.from_iterable(batches))
    if records:
        tbl.add(records)
    return {"files": len(inputs), "records": len(records)}

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-prefix", required=True, help="s3://bucket/prefix/")
    ap.add_argument("--lancedb-uri", required=True, help="s3://bucket/lancedb or ./lancedb")
    ap.add_argument("--table-name", default="wiki_vectors")
    ap.add_argument("--model", default="all-MiniLM-L6-v2")
    args = ap.parse_args()
    stats = run_ingest(args.input_prefix, args.lancedb_uri, args.table_name, args.model)
    print(f"Ingested {stats['records']} vectors from {stats['files']} files.")
