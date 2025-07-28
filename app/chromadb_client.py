import chromadb, os
import time
from openai import OpenAI
from app.modules.logging.llm_request_logger import log_llm_request  # 追加

db_path = os.path.abspath("./data/document_collection")
# ChromaDBの初期化を環境変数で制御
if not os.environ.get("SKIP_CHROMADB_INIT"):
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection("document_collection")
else:
    client = None
    collection = None

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chromadb_query(user_id, query_text):
    if not collection:
        raise RuntimeError("ChromaDBは初期化されていません。")

    start_time = time.time()
    try:
        response = openai_client.embeddings.create(
            input=query_text,
            model="text-embedding-3-small"
        )
        response_time = time.time() - start_time
        token_count = response.usage.total_tokens
        embedding = response.data[0].embedding

        log_llm_request(user_id, request_content=query_text, response_time=response_time, token_count=token_count)

        results = collection.query(
            query_embeddings=[embedding],
            n_results=1,
            include=["distances", "documents"]
        )

        if results and results['documents'] and results['documents'][0]:
            return results['documents'][0][0], results['distances'][0][0]
        else:
            return None, 0

    except Exception as e:
        response_time = time.time() - start_time
        log_llm_request(user_id, request_content=query_text, response_time=response_time, token_count=0, api_error=e)
        raise e
