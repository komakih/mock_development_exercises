# list_collections.py
import chromadb

client = chromadb.PersistentClient(path="/Users/hkomaki/Downloads/mock_development_exercises/data/document_collection")
collections = client.list_collections()
print("存在するコレクション一覧:", collections)
