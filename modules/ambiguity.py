from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_ambiguous(user_input):
    ambiguous_examples = ['こんにちは', 'こんにちわ', 'おはよう', 'こんばんは', 'わからない', '教えて', 'どうしたら']
    if user_input.strip() in ambiguous_examples:
        return True

    prompt = f"""
    次の入力が質問として具体的であるか曖昧であるかを判定してください。
    あいさつや質問として意味をなさない場合も曖昧と判定してください。
    曖昧なら「YES」、明確なら「NO」とだけ返答。

    入力: "{user_input}"

    回答:
    """
    response = openai_client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role":"system","content":"判定をYESまたはNOのみで行うこと"},{"role":"user","content":prompt}]
    )
    result = response.choices[0].message.content.strip()
    return result == "YES"
