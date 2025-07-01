from fastapi import APIRouter, Depends
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("API_KEY"))

router = APIRouter()

@router.post("/query")
def chat_query(message: str):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    answer = response.choices[0].message.content
    return {"response": answer}
