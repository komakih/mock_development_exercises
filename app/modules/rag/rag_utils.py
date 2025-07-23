from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from app.modules.logging.vector_search_logger import log_search_result
from app.openai_utils import get_chatgpt_response

documents = SimpleDirectoryReader("data/docs").load_data()
index = VectorStoreIndex.from_documents(documents)

def perform_vector_search(user_id, query, similarity_threshold=0.80):
    query_engine = index.as_query_engine(response_mode='compact', similarity_top_k=1)
    response = query_engine.query(query)

    if response and response.response.strip():
        source_info = [{
            "source": node.metadata.get('file_name', '不明な文書'),
            "similarity": node.score
        } for node in response.source_nodes]

        # 類似度が閾値を超えるかで判断
        matched = source_info[0]['similarity'] >= similarity_threshold

        # 常にログを記録する（ヒットしたかどうかも記録）
        log_search_result(
            user_id=user_id,
            query=query,
            result=source_info[0]['source'],
            similarity=source_info[0]['similarity'],
            matched=matched
        )

        if not matched:
            return None, None

        # 必要に応じて翻訳
        if not is_japanese(response.response):
            translated_response, _ = get_chatgpt_response([
                {"role": "system", "content": "以下の英文を日本語に翻訳してください。"},
                {"role": "user", "content": response.response}
            ])
            return translated_response, source_info

        return response.response, source_info
    else:
        log_search_result(
            user_id=user_id,
            query=query,
            result="該当なし",
            similarity=0.0,
            matched=False
        )
        return None, None

def is_japanese(text):
    for ch in text:
        if 0x3040 <= ord(ch) <= 0x30ff or 0x4e00 <= ord(ch) <= 0x9faf:
            return True
    return False
