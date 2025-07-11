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

# docxファイルの場所を指定
docx_files = glob.glob("./data/*.docx")

for docx_file in docx_files:
    doc = docx.Document(docx_file)
    texts = [para.text for para in doc.paragraphs if para.text.strip() != ""]

    for idx, text in enumerate(texts):
        # Embedding生成（OpenAIを使用）
        embedding = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        ).data[0].embedding

        # ChromaDBに挿入
        collection.add(
            ids=[f"{os.path.basename(docx_file)}_{idx}"],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"source": os.path.basename(docx_file)}]
        )

# 挿入件数を表示
print("ドキュメント数:", collection.count())
print("コレクション名:", collection.name)
print("保存パス:", db_path)
