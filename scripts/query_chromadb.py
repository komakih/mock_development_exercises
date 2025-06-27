import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("API_KEY")

if not openai_api_key:
    raise ValueError("APIキーがありません。.envを確認してください。")

# 永続化ディレクトリを完全一致で指定
persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "manual_db"))
print(f"✅ 確認で使用するデータ保存先: {persist_directory}")

# PersistentClientを使用して読み込み
client = chromadb.PersistentClient(path=persist_directory)

# OpenAIの埋め込み関数を再設定
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
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
