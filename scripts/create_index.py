import os
import glob
import chromadb
import docx
from openai import OpenAI

# OpenAI API設定
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ChromaDBの永続化クライアントを設定（絶対パス指定）
db_path = os.path.abspath("./data/document_collection")
client = chromadb.PersistentClient(path=db_path)

# コレクションを作成または取得
collection_name = "document_collection"
collection = client.get_or_create_collection(collection_name)

# 現在のコレクション内の既存のIDを取得して重複を防ぐ
existing_ids = set(collection.get().get('ids', []))  # ←これを追加

# docxファイルの場所を指定
docx_files = glob.glob("./data/*.docx")

for docx_file in docx_files:
    doc = docx.Document(docx_file)
    texts = [para.text for para in doc.paragraphs if para.text.strip() != ""]

    for idx, text in enumerate(texts):
        embedding_id = f"{os.path.basename(docx_file)}_{idx}"

        if embedding_id not in existing_ids:
            embedding = openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            ).data[0].embedding

            collection.add(
                ids=[embedding_id],
                embeddings=[embedding],
                documents=[text]
            )

print("インデックス作成完了")
