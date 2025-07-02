from fastapi import APIRouter
from chromadb.utils import embedding_functions
import chromadb
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

router = APIRouter()

load_dotenv()
openai_api_key = os.getenv("API_KEY")
persist_directory = os.path.abspath("./manual_db")

# ChromaDBの設定
client = chromadb.PersistentClient(path=persist_directory)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-ada-002"
)

# コレクション取得
collection = client.get_or_create_collection(
    "manual_documents", embedding_function=openai_ef
)

# リクエスト・レスポンスのスキーマ定義
class QueryRequest(BaseModel):
    query_text: str
    n_results: int = 3

class DocumentResult(BaseModel):
    id: str
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    results: List[DocumentResult]

# ドキュメント検索API
@router.post("/search", response_model=QueryResponse)
def search_documents(query: QueryRequest):
    results = collection.query(
        query_texts=[query.query_text],
        n_results=query.n_results
    )

    documents = []
    for doc_id, content, metadata in zip(results['ids'][0], results['documents'][0], results['metadatas'][0]):
        documents.append(DocumentResult(
            id=doc_id,
            content=content,
            metadata=metadata
        ))

    return QueryResponse(results=documents)
