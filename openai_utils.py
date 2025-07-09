# openai_utils.py
import openai

def generate_thread_title(question):
    prompt = f"以下の質問内容から簡潔なタイトルを生成してください: {question}"

    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )

    title = response.choices[0].message.content.strip()
    return title
