import json
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings as ChromaSettings
from dotenv import load_dotenv
import os

load_dotenv()

faq_json_path = "./data/faq_data.json"
INDEX_DIR = "./index_storage"

def main():
    # この位置で初期化（関数内）
    client = chromadb.PersistentClient(
        path=INDEX_DIR,
        settings=ChromaSettings(anonymized_telemetry=False)
    )

    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    collection = client.get_or_create_collection(
        name="faq_collection",
        embedding_function=embedding_fn
    )

    with open(faq_json_path, "r", encoding="utf-8") as file:
        faq_data = json.load(file)

    for faq in faq_data:
        collection.add(
            documents=[faq["question"]],
            metadatas=[{"answer": faq["answer"]}],
            ids=[faq["question"]]
        )

    print("✅ FAQインデックスが正常に作成されました。")

if __name__ == "__main__":
    main()
