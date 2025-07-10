import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings as ChromaSettings
from dotenv import load_dotenv
import os

load_dotenv()

INDEX_DIR = "./index_storage"
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))

client = chromadb.PersistentClient(
    path=INDEX_DIR,
    settings=ChromaSettings(anonymized_telemetry=False)
)
collection = client.get_or_create_collection("faq_collection", embedding_function=embedding_fn)

def faq_query(query, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas"]
    )
    return results
