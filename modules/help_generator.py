from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_help_message(faq_results):
    faq_pairs = ""
    for i, (question, metadata) in enumerate(zip(faq_results["documents"][0], faq_results["metadatas"][0]), start=1):
        faq_pairs += f"{i}. {question}\n"

    prompt = f"""
    ユーザーの入力が曖昧なため、以下のFAQ項目の質問例を参考に、ユーザーに質問例のリストを提示してください。

    FAQ一覧:
    {faq_pairs}

    回答メッセージ:
    """

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role":"system","content":"ユーザーに役立つ簡潔なFAQ質問例リストを提示してください。"},{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content.strip()

