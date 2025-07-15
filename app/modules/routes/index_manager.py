import os
import shutil
import time
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

DOCS_DIR = 'data/docs'
TMP_INDEX_DIR = 'data/tmp_index'
PROD_INDEX_DIR = 'data/index'

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