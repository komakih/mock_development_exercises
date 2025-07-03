import os
import chromadb
from chromadb.utils import embedding_functions
import docx
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("API_KEY")
persist_directory = os.path.abspath("./manual_db")
doc_folder = os.path.abspath("./documents")

def rebuild_chromadb_index():
    try:
        # ChromaDBクライアントを作成（PersistentClient利用）
        client = chromadb.PersistentClient(path=persist_directory)

        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-ada-002"
        )

        # コレクションが存在すれば削除（再構築のため）
        collection_name = "manual_documents"
        if collection_name in [col.name for col in client.list_collections()]:
            client.delete_collection(collection_name)

        # コレクションを新規作成
        collection = client.create_collection(collection_name, embedding_function=openai_ef)

        # ドキュメントを再登録
        doc_paths = [os.path.join(doc_folder, f) for f in os.listdir(doc_folder) if f.endswith(".docx")]

        for path in doc_paths:
            doc = docx.Document(path)
            full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            title = os.path.basename(path).replace(".docx", "")

            collection.add(
                documents=[full_text],
                metadatas=[{"title": title, "path": path}],
                ids=[title]
            )

        return {"status": "success", "message": "インデックス更新完了"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
