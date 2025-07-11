import chromadb, os

db_path = os.path.abspath("./data/document_collection")
client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection("document_collection")
print(collection.peek())