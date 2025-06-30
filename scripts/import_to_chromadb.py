import chromadb
from chromadb.utils import embedding_functions
import docx
import os
from dotenv import load_dotenv
from openai import OpenAI
import shutil

# 環境変数の読み込み
load_dotenv()
openai_api_key = os.getenv("API_KEY")

if not openai_api_key:
    raise ValueError("APIキーがありません。.envを確認してください。")

# 新しいOpenAIクライアント作成（1.x対応）
openai_client = OpenAI(api_key=openai_api_key)

# ChromaDB永続化の設定
persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "manual_db"))
print(f"✅ データ保存先: {persist_directory}")

# 古いデータ削除
if os.path.exists(persist_directory):
    shutil.rmtree(persist_directory)
    print("🗑️ 古いデータを削除しました。")

# ChromaDBクライアント作成（0.4.24利用時）
client = chromadb.PersistentClient(path=persist_directory)

# 新OpenAIクライアントを利用した埋め込み関数を作成
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,  # 必ずキー指定を継続
    model_name="text-embedding-ada-002"
)

# コレクション作成
collection = client.get_or_create_collection(
    "manual_documents",
    embedding_function=openai_ef
)

# docxファイルのパス取得
doc_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "documents"))
doc_paths = [os.path.join(doc_folder, f) for f in os.listdir(doc_folder) if f.endswith(".docx")]

# ドキュメント登録
for path in doc_paths:
    doc = docx.Document(path)
    full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    title = os.path.basename(path).replace(".docx", "")

    collection.add(
        documents=[full_text],
        metadatas=[{"title": title, "path": path}],
        ids=[title]
    )

print(f"✅ 再登録完了しました。文書数: {collection.count()}")
