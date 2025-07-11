import chromadb
import os
from openai import OpenAI

# ChromaDBクライアントの設定（絶対パス）
db_path = os.path.abspath("./data/document_collection")
client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection("document_collection")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chromadb_query(query_text):
    embedding = openai_client.embeddings.create(
        input=query_text,
        model="text-embedding-3-small"
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
        include=["distances", "documents"]
    )

    if results and results['documents'] and results['documents'][0]:
        return results['documents'][0][0], results['distances'][0][0]
    else:
        return None, 0