import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import openai

# 環境変数を読み込み
load_dotenv()

# APIキーを明示的に取得し設定
openai_api_key = os.getenv("OPENAI_API_KEY").strip()
openai.api_key = openai_api_key  # openaiライブラリ側で明示的に指定

# llama-index側のEmbedding設定（最新版に完全対応）
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=openai_api_key,
    timeout=60,
    max_retries=2
)

DATA_DIR = "./data"
INDEX_DIR = "./index_storage"

# 文書の読み込み
documents = SimpleDirectoryReader(DATA_DIR).load_data()

# ChromaDB設定（テレメトリー無効化）
chroma_client = chromadb.PersistentClient(
    path=INDEX_DIR,
    settings=chromadb.config.Settings(anonymized_telemetry=False)
)

chroma_collection = chroma_client.get_or_create_collection("document_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# インデックス作成と保存
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

print("インデックス作成完了")
