from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from app.modules.logging.vector_search_logger import log_search_result
from app.openai_utils import get_chatgpt_response

documents = SimpleDirectoryReader("data/docs").load_data()
index = VectorStoreIndex.from_documents(documents)

def perform_vector_search(user_id, query, similarity_threshold=0.85):
    query_engine = index.as_query_engine(response_mode='compact', similarity_top_k=1)
    response = query_engine.query(query)

    if response and response.response.strip() and response.source_nodes:
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

        rag_response = response.response.strip()

        # ↓ matchedのチェックの前に英語翻訳を行うように変更
        if not is_japanese(rag_response):
            translated_response, _ = get_chatgpt_response(
                user_id,
                [
                    {"role": "system", "content": "以下の英文を日本語に翻訳してください。"},
                    {"role": "user", "content": rag_response}
                ],
                use_rag_search=False  # 翻訳時に再帰を防ぐために必要
            )
            rag_response = translated_response  # 翻訳した日本語を使う

        if matched:
            return rag_response, source_info
        else:
            external_response, _ = get_chatgpt_response(
                user_id,
                [{"role": "user", "content": query}],
                use_rag_search=False
            )
            fixed_response = "マニュアルに該当する情報がありませんので外部からの検索結果を返答します:\n" + external_response
            return fixed_response, source_info
    else:
        log_no_result_search(user_id, query)
        external_response, _ = get_chatgpt_response(
            user_id,
            [{"role": "user", "content": query}],
            use_rag_search=False
        )
        fixed_response = "マニュアルに該当する情報がありませんので外部からの検索結果を返答します:\n" + external_response
        return fixed_response, None

def is_japanese(text):
    for ch in text:
        if 0x3040 <= ord(ch) <= 0x30ff or 0x4e00 <= ord(ch) <= 0x9faf:
            return True
    return False
