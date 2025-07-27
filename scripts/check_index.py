from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir='data/index')
index = load_index_from_storage(storage_context)

docs = index.docstore.docs
for doc_id, doc in docs.items():
    print(f'Doc ID: {doc_id}')
    print(f'Content: {doc.get_text()[:200]}...\n\n')  # 文書の冒頭200文字程度を表示
