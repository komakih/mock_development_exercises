import os, time
from openai import OpenAI
from app.chromadb_client import chromadb_query
from app.modules.logging.llm_request_logger import log_llm_request  # 追加

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# RAG使用を判断する条件を設定（類似度スコアで判断）
def should_use_rag(user_id, query, threshold=0.9):
    result, score = chromadb_query(user_id, query)
    return score >= threshold, result

# ChatGPTまたはRAGを使用して応答を取得
def get_chatgpt_response(user_id, messages):
    start_time = time.time()  # 開始時刻を記録
    last_message = messages[-1]['content']
    use_rag, rag_info = should_use_rag(user_id, last_message)

    if use_rag:
        source = "RAG"
        messages.append({"role": "system", "content": f"以下の情報を参考にして回答してください:\n{rag_info}"})
    else:
        source = "GPT"

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )
        response_time = time.time() - start_time  # レスポンスタイムを計算
        token_count = response.usage.total_tokens

        # ログ記録を追加
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
