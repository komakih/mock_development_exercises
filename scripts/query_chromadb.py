import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("API_KEY")

if not openai_api_key:
    raise ValueError("APIキーがありません。.envを確認してください。")

# OpenAIクライアント作成（最新版対応）
openai_client = OpenAI(api_key=openai_api_key)

# 永続化データの場所を指定
persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "manual_db"))
print(f"✅ 確認用データ保存先: {persist_directory}")

# ChromaDBクライアント作成（0.4.24利用時）
client = chromadb.PersistentClient(path=persist_directory)

# 新OpenAIクライアントを利用した埋め込み関数を再設定
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,  # ここもAPIキーを再設定
    model_name="text-embedding-ada-002"
)

# コレクションを取得
collection = client.get_or_create_collection(
    "manual_documents",
    embedding_function=openai_ef
)

print(f"✅ コレクション取得完了。文書数: {collection.count()}")

# 検索実行
query_text = "返品方法について教えてください"
result = collection.query(
    query_texts=[query_text],
    n_results=2
)

print("🔍 検索結果:")
print(result)
