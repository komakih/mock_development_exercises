import os, time
from openai import OpenAI
from app.chromadb_client import chromadb_query
from app.modules.logging.llm_request_logger import log_llm_request  # 追加

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ChatGPTまたはRAGを使用して応答を取得
def get_chatgpt_response(user_id, messages, use_rag_search=True):
    start_time = time.time()
    last_message = messages[-1]['content']
    from app.modules.rag.rag_utils import perform_vector_search

    if use_rag_search:
        rag_response, source_info = perform_vector_search(user_id, last_message)
        if rag_response:
            source = "RAG"
            rag_prompt = (
                "あなたは以下の参考情報をもとに質問に回答してください。\n"
                "注意事項:\n"
                "1. 参考情報の箇条書きは必ず箇条書きとして維持してください。\n"
                "2. 改行は元の情報のまま絶対に変更せず再現してください。\n"
                "3. 回答には追加の解説や文章を加えず、参考情報をそのまま提供してください。\n\n"
                f"---参考情報---\n{rag_response}\n---ここまで---\n"
            )
            messages.append({"role": "system", "content": rag_prompt})
        else:
            source = "GPT"
    else:
        source = "GPT"

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            max_tokens=2048  # トークン数を明示的に指定
        )
        response_time = time.time() - start_time
        token_count = response.usage.total_tokens

        log_llm_request(user_id, request_content=messages, response_time=response_time, token_count=token_count)
        return response.choices[0].message.content, source

    except Exception as e:
        response_time = time.time() - start_time
        log_llm_request(user_id, request_content=messages, response_time=response_time, token_count=0, api_error=e)
        raise e

# スレッドタイトルを生成する関数
def generate_thread_title(user_id, content):
    start_time = time.time()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": 
                    "あなたは会話内容をタイトルに要約するAIです。"
                    "以下のルールを厳密に守り、タイトルを生成してください。\n"
                    "1. タイトルは絶対に記号（『』「」\"\"''など）で囲まない。\n"
                    "2. タイトルは15文字以内で簡潔に表現する。\n"
                    "3. 句読点を使わない。\n"
                    "4. 名詞や動詞を中心としたシンプルな表現にする。"
                },
                {"role": "user", "content": content}
            ]
        )
        response_time = time.time() - start_time
        token_count = response.usage.total_tokens

        # ログ記録を追加
        log_llm_request(user_id, request_content=content, response_time=response_time, token_count=token_count)

        title = response.choices[0].message.content.strip()
        return title

    except Exception as e:
        response_time = time.time() - start_time
        log_llm_request(user_id, request_content=content, response_time=response_time, token_count=0, api_error=e)
        raise e
