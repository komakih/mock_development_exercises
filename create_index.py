import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_DIR = "./data"
INDEX_DIR = "./index_storage"

documents = SimpleDirectoryReader(DATA_DIR).load_data()

chroma_client = chromadb.PersistentClient(path=INDEX_DIR)
chroma_collection = chroma_client.get_or_create_collection("document_collection")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

print("インデックス作成完了")
