import os
import shutil
import time
import hashlib
import json
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

DOCS_DIR = 'data/docs'
TMP_INDEX_DIR = 'data/tmp_index'
PROD_INDEX_DIR = 'data/index'
HASH_FILE = 'data/index/docs_hashes.json'

class IndexManager:
    @staticmethod
    def create_index(doc_dir, index_dir):
        documents = SimpleDirectoryReader(doc_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=index_dir)
        return len(documents)

    @staticmethod
    def update_index():
        start_time = time.time()
        try:
            if os.path.exists(TMP_INDEX_DIR):
                shutil.rmtree(TMP_INDEX_DIR)
            os.makedirs(TMP_INDEX_DIR, exist_ok=True)
            doc_count = IndexManager.create_index(DOCS_DIR, TMP_INDEX_DIR)
            if os.path.exists(PROD_INDEX_DIR):
                shutil.rmtree(PROD_INDEX_DIR)
            shutil.move(TMP_INDEX_DIR, PROD_INDEX_DIR)
            elapsed_time = time.time() - start_time
            return {'success': True, 'document_count': doc_count, 'time': elapsed_time}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def file_hash(filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    @staticmethod
    def get_current_hashes(doc_dir):
        hashes = {}
        for root, _, files in os.walk(doc_dir):
            for file in files:
                path = os.path.join(root, file)
                hashes[path] = IndexManager.file_hash(path)
        return hashes

    @staticmethod
    def save_hashes(hashes):
        with open(HASH_FILE, 'w') as f:
            json.dump(hashes, f)

    @staticmethod
    def load_hashes():
        if not os.path.exists(HASH_FILE):
            return {}
        with open(HASH_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_changed_files(current_hashes, previous_hashes):
        changed_files = [file for file, hash in current_hashes.items() if previous_hashes.get(file) != hash]
        return changed_files