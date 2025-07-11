import os
from openai import OpenAI
from app.chromadb_client import chromadb_query

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# RAG使用を判断する条件を設定（類似度スコアで判断）
def should_use_rag(query, threshold=0.98):
    result, score = chromadb_query(query)
    return score >= threshold, result

# ChatGPTまたはRAGを使用して応答を取得
def get_chatgpt_response(messages):
    last_message = messages[-1]['content']
    use_rag, rag_info = should_use_rag(last_message)

    if use_rag:
        source = "RAG"
        messages.append({"role": "system", "content": f"以下の情報を参考にして回答してください:\n{rag_info}"})
    else:
        source = "GPT"

    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    ).choices[0].message.content

    return response, source

def generate_thread_title(content):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "以下のメッセージから短いタイトルを生成してください。"},
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_thread_title(content):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "以下の内容から15文字以内で簡潔なタイトルを生成してください。"},
            {"role": "user", "content": content}
        ]
    )
    title = response.choices[0].message.content.strip()
    return title