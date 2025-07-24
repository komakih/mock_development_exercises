from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from app.modules.logging.vector_search_logger import log_search_result
from app.openai_utils import get_chatgpt_response

documents = SimpleDirectoryReader("data/docs").load_data()
index = VectorStoreIndex.from_documents(documents)

def perform_vector_search(user_id, query, similarity_threshold=0.85):
    query_engine = index.as_query_engine(response_mode='compact', similarity_top_k=1)
    response = query_engine.query(query)

    if response and response.response.strip():
        source_info = [{
            "source": node.metadata.get('file_name', '不明な文書'),
            "similarity": node.score
        } for node in response.source_nodes]

        matched = float(source_info[0]['similarity']) >= float(similarity_threshold)

        log_search_result(
            user_id=user_id,
            query=query,
            result=source_info[0]['source'],
            similarity=source_info[0]['similarity'],
            matched=matched
        )

        if not matched:
            external_response, _ = get_chatgpt_response(user_id, [
                {"role": "user", "content": query}
            ])
            fixed_response = (
                "マニュアルに該当する情報がありませんので外部からの検索結果を返答します:\n" + external_response
            ).replace('\n', '<br>')  # ここで改行適用
            return fixed_response, source_info

        if not is_japanese(response.response):
            translated_response, _ = get_chatgpt_response(user_id, [
                {"role": "system", "content": "以下の英文を日本語に翻訳してください。"},
                {"role": "user", "content": response.response}
            ])
            return translated_response.replace('\n', '<br>'), source_info  # ここも改行適用

        # RAGのレスポンスも改行を適用するように修正
        return response.response.strip().replace('\n', '<br>'), source_info
    else:
        log_no_result_search(user_id, query)
        external_response, _ = get_chatgpt_response(user_id, [
            {"role": "user", "content": query}
        ])
        fixed_response = (
            "マニュアルに該当する情報がありませんので外部からの検索結果を返答します:\n" + external_response
        ).replace('\n', '<br>')  # ここも改行適用
        return fixed_response, None

def is_japanese(text):
    for ch in text:
        if 0x3040 <= ord(ch) <= 0x30ff or 0x4e00 <= ord(ch) <= 0x9faf:
            return True
    return False
