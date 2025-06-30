from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("API_KEY")

if not openai_api_key:
    raise ValueError("APIキーがありません。.envファイルを確認してください。")

# 新しいクライアントインスタンスを作成
client = OpenAI(api_key=openai_api_key)

# クエリを実行（新しいAPI）
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, world!"}]
    )
    print("✅ OpenAI APIが正常に動作しました。")
    print(response.choices[0].message.content)
except Exception as e:
    print("❌ OpenAI APIの動作でエラーが発生しました:", e)
