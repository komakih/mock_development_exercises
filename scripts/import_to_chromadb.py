import chromadb
from chromadb.utils import embedding_functions
import docx
import os
import shutil
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("API_KEY")

if not openai_api_key:
    raise ValueError("APIキーがありません。.envを確認してください。")

# 永続化ディレクトリ（絶対パス推奨）
persist_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "manual_db"))
print(f"✅ 使用するデータ保存先: {persist_directory}")

# 古いデータを削除
if os.path.exists(persist_directory):
    shutil.rmtree(persist_directory)
    print("🗑️ 古いデータを削除しました。")

# 0.4.24ではPersistentClientを使用
client = chromadb.PersistentClient(path=persist_directory)

# 埋め込み関数（OpenAI）設定
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-ada-002"
)

# コレクションを新規作成（永続化）
collection = client.get_or_create_collection(
    "manual_documents",
    embedding_function=openai_ef
)

# docxファイルのパス指定
doc_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "documents"))
doc_paths = [os.path.join(doc_folder, f) for f in os.listdir(doc_folder) if f.endswith(".docx")]

# データを登録
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
